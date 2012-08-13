#!/usr/bin/env python
# coding: utf-8

import MySQLdb
from httphandler import Request, Response, get_htmltemplate
import cgitb; cgitb.enable()
import cgi
from simpletemplate import SimpleTemplate
from os import path

radio_parts = u"""
<input type="radio" %s name="custname" value="%s" />%s <br>
"""

content ="""
<form method="POST" action="/cgi-bin/content.py">
"""
def notapplicable():
    body = u"該当がありません"
    res = Response()
    res.set_body(get_htmltemplate() % body)
    print res

req = Request()

con = MySQLdb.connect(host = 'localhost', db = 'usermanage', user = 'python',
        passwd = 'python', charset = 'utf8')
cur = con.cursor(MySQLdb.cursors.DictCursor)

str = req.form.getvalue('custname', 'none')
radio = req.form.getvalue('cust', 'none')

template_path = '/var/www/html/cpy/result.html'

if str == "none":
    body = u"テキストフィールドに検索する文字を入力してください"
    res = Response()
    res.set_body(get_htmltemplate() % body)
    print res

elif radio == "custini":
    cur.execute("""SELECT * FROM main WHERE custini = '%s' FOR UPDATE""" % str)
    con.commit()
    temp = cur.fetchall()
    if temp:
        item = temp[0]
        t = SimpleTemplate(file_path = template_path)
        body = t.render(item)
        res = Response()
        res.set_body(body)
        print res
    else:
        notapplicable()

elif radio == "customer":
    cur.execute("""SELECT * FROM main WHERE customer LIKE '%%%s%%' FOR UPDATE""" %
            (MySQLdb.escape_string(str)))
    con.commit()
    temp = cur.fetchall()
    if temp:
        radio_check = "checked"
        for item in temp:
            content += radio_parts % (radio_check, item['customer'], item['customer'])
            radio_check = ""
        content += """<input type="submit" name="submit" value="OK" />"""
        res = Response()
        res.set_body(get_htmltemplate() % content)
        print res
    else:
        body = u"該当がありません"
        res = Response()
        res.set_body(get_htmltemplate() % body)
        print res

elif str:
    cur.execute("""SELECT * FROM main WHERE customer = '%s' FOR UPDATE""" % str)
    con.commit()
    temp = cur.fetchall()
    item = temp[0]
    t = SimpleTemplate(file_path = template_path)
    body = t.render(item)
    res = Response()
    res.set_body(body)
    print res

else:
    body = u"規定外のエラー"
    res = Response()
    res.set_body(get_htmltemplate() % body)
    print res

cur.close()
con.close()
