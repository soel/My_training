#!/usr/bin/env python
# coding: utf-8

import MySQLdb
from httphandler import Request, Response, get_htmltemplate
import cgitb; cgitb.enable()
import cgi

html_body_result = u"""
<table border="1" width="750" cellspacing="0" cellpadding="5" bordercolor="#333333">
<tr>
<td width = "150">システムID</td>
<td>%s</td>
</tr>
<tr>
<td>顧客頭文字</td>
<td>%s</td>
</tr>
<tr>
<td>顧客名</td>
<td>%s</td>
</tr>
<tr>
<td>メールアドレス</td>
<td>%s</td>
</tr>
<tr>
<td>住所</td>
<td>%s</td>
</tr>
<tr>
<td>タイプ</td>
<td>%s</td>
</tr>
<tr>
<td>備考</td>
<td>%s</td>
</tr>
</table>
"""
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

if str == "none":
    body = u"テキストフィールドに検索する文字を入力してください"
    res = Response()
    res.set_body(get_htmltemplate() % body)
    print res

elif radio == "custini":
    cur.execute("""SELECT * FROM main WHERE custini = '%s' """ % str)
    temp = cur.fetchall()
    if temp:
        item = temp[0]
        body = html_body_result % (item['sysID'], item['custini'],
                item['customer'], item['mail'], item['addr'],
                item['type'],item['etc'])
        res = Response()
        res.set_body(get_htmltemplate() % body)
        print res
    else:
        notapplicable()

elif radio == "customer":
    cur.execute("""SELECT * FROM main WHERE customer LIKE '%%%s%%' """ %
            (MySQLdb.escape_string(str)))
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
    cur.execute("""SELECT * FROM main WHERE customer = '%s' """ % str)
    temp = cur.fetchall()
    item = temp[0]
    body = html_body_result % (item['sysID'], item['custini'],
            item['customer'], item['mail'], item['addr'],
            item['type'],item['etc'])
    res = Response()
    res.set_body(get_htmltemplate() % body)
    print res

else:
    body = u"規定外のエラー"
    res = Response()
    res.set_body(get_htmltemplate() % body)
    print res

