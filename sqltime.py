#!/usr/bin/python
# coding: utf-8

import MySQLdb
import datetime

d = datetime.datetime.today()
t = "%s.%s.%s.%s.%s.%s" % (d.year, d.month, d.day, d.hour, d.minute, d.second)

con = MySQLdb.connect(host = 'localhost', db = 'time', user = 'root',
        passwd = 'P@ssw0rd', charset = 'utf8')
cur = con.cursor(MySQLdb.cursors.DictCursor)

cur.execute("""INSERT INTO time VALUES('%s')""" % t)

con.commit()

cur.close()
con.close()
