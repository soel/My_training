#!/usr/bin/python
# coding: utf-8

import sqlite3

class BaseMapper(object):
    """
    シンプルな O/R マッパーのベースクラス
    """
    rows = ()

    connection = sqlite3.connect(':memory:')

    @classmethod
    def setconnection(cls, con):
        cls.connection = con

    @classmethod
    def getconnection(cls):
        return cls.connection

    def __init__(self, **kws):
        """
        クラスの初期化
        id を引数に渡された場合は、既存データを返す
        その他のキーワードの場合はデータをインサートする
        """
        if 'id' in kws.keys():
            rownames = [v[0] for v in self.__class__.rows]
            rownamestr = ', '.join(rownames)
            cn = self.__class__.__name__
            sql = """SELECT %s FROM %s WHERE id = ?""" % (rownamestr, cn)
            cur = self.getconnection().cursor()
            cur.execute(sql, (kws['id'],))
            for rowname, v in zip(rownames, cur.fetchone()):
                setattr(self, rowname, v)
            self.id = kws['id']
            cur.close()
        elif kws:
            self.id = self.insert(**kws)
            rownames = [v[0] for v in self.__class__.rows]
            for k in kws.keys():
                if k in rownames:
                    setattr(self, k, kws[k])

    def update(self):
        """
        データの更新
        """
        sql = """UPDATE %s SET %s WHERE id=?"""
        rownames = [v[0] for v in self.__class__.rows]
        holders = ', '.join(['%s = ?' % v for v in rownames])
        sql = sql % (self.__class__.__name__, holders)
        values = [getattr(self, n) for n in rownames]
        values.append(self.id)
        cur = self.getconnection().cursor()
        cur.execute(sql, values)
        self.getconnection().commit()
        cur.close()

    where_conditions = {
            '_gt' : '>', '_lt' : '<',
            '_gte' : '>=', '_lte' : '<=',
            '_like' : 'LIKE' }

    @classmethod
    def select(cls, **kws):
        """
        テーブルからデータを SELECT する
        """
        order = ''
        if "order_by" in kws.keys():
            order = " ORDER BY " + kws['order_by']
            del kws['order_by']
        where = []
        values = []
        for key in kws.keys():
            ct = '='
            kwkeys = cls.where_conditions.keys()
            for ckey in kwkeys:
                if key.endswith(ckey):
                    ct = cls.where_conditions[ckey]
                    kws[key.replace(ckey, '')] = kws[key]
                    del kws[key]
                    key = key.replace(ckey, '')
                    break
            where.append(' '.join((key, ct, '? ')))
            values.append(kws[key])
        wherestr = 'AND '.join(where)
        sql = "SELECT id FROM " + cls.__name__
        if wherestr:
            sql += " WHERE " + wherestr
        sql += order
        cur = cls.getconnection().cursor()
        cur.execute(sql, values)
        for item in cur.fetchall():
            ins = cls(id = item[0])
            yield ins
        cur.close()

    def __repr__(self):
        """
        オブジェクトの文字表記の定期
        """
        rep = str(self.__class__.__name__) + ':'
        rownames = [v[0] for v in self.__class__.rows]
        rep += ', '.join(["%s = %s" % (x, repr(
            getattr(self, x))) for x in rownames])
        return "<%s>" % rep

    @classmethod
    def createtable(cls, ignore_error = False):
        """
        定義に基いてテーブルを作る
        """
        sql = """CREATE TABLE %s (
             id INTEGER PRIMARY KEY, %s);""" #sql定義文
        #cls.rows の内容を k,v に展開し , 区切りで join
        columns = ', '.join(["%s %s" % (k, v) for k, v in cls.rows])
        #sql の定義文にクラス名と、columns の値を挿入
        sql = sql % (cls.__name__, columns)
        cur = cls.getconnection().cursor()
        try:
            #SQL の実行
            cur.execute(sql)
        except Exception, e:
            if not ignore_error:
                raise e
        cur.close()
        cls.getconnection().commit()

    @classmethod
    def insert(cls, **kws):
        """
        データを追加し, IDを返す
        """
        sql = """INSERT INTO %s(%s) VALUES(%s)"""
        rownames = ', '.join([v[0] for v in cls.rows])
        holders = ', '.join(['?' for v in cls.rows])
        sql = sql % (cls.__name__, rownames, holders)
        values = [kws[v[0]] for v in cls.rows]
        cur = cls.getconnection().cursor()
        cur.execute(sql, values)
        cur.execute("SELECT max(id) FROM %s" % cls.__name__)
        newid = cur.fetchone()[0]
        cls.getconnection().commit()
        cur.close()
        return newid



