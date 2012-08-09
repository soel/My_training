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
<input type="radio" name="cust" value="%s" />%s <br>
"""

content ="""
<form method="POST" action="/cgi-bin/content2.py">
"""


req = Request()

con = MySQLdb.connect(host = 'localhost', db = 'usermanage', user = 'python',
        passwd = 'python', charset = 'utf8')
cur = con.cursor(MySQLdb.cursors.DictCursor)

str = req.form.getvalue('custname', '')
radio = req.form.getvalue('cust', '')

if radio == "custini":
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
        #result = (get_htmltemplate() % body).encode('utf-8')
        #print result
    else:
        body = u"該当がありません"
        res = Response()
        res.set_body(get_htmltemplate() % body)
        print res

else:
    cur.execute("""SELECT * FROM main WHERE customer LIKE '%%%s%%' """ %
            (MySQLdb.escape_string(str)))
    temp = cur.fetchall()
    if temp:
        for item in temp:
            content += radio_parts % (item['customer'], item['customer'])
        content += """<input type="submit" name="submit" value="OK" />"""
        res = Response()
        res.set_body(get_htmltemplate() % content)
        print res
    else:
        body = u"該当がありません"
        res = Response()
        res.set_body(get_htmltemplate() % body)
        print res
