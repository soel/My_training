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


req = Request()

con = MySQLdb.connect(host = 'localhost', db = 'usermanage', user = 'python',
        passwd = 'python', charset = 'utf8')
cur = con.cursor()

str = req.form.getvalue('custname', '')
radio = req.form.getvalue('cust', '')

if radio == "custini":
    test = u"頭文字です"
    cur.execute("""SELECT * FROM main WHERE custini = '%s' """ % str)
    for item in cur.fetchall():
        obj = item

#body = html_body_result % (obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6])
body = html_body_result % (item[0], item[1], item[2], item[3], item[4], item[5],
        item[6])
result = (get_htmltemplate() % body).encode('utf-8')
print result
