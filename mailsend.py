#!/usr/bin/env python
# coding: utf-8

import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

if __name__ == "__main__":
    from_address = ""
    to_address   = ["", ""] #複数に送る場合はリスト型
    cc_address   = ["", ""]
    bcc_address  = ["", ""]

    charset = "ISO-2022-JP"
    subject = u"メールの件名です"
    text    = u"メールの本文です"

    msg = MIMEText(text.encode(charset),"plain",charset)
    msg["Subject"] = Header(subject,charset)
    msg["From"]    = from_address
    msg["To"]      = ",".join(to_address) #ここは "," 区切りでひとつに
    msg["cc"]      = ",".join(cc_address) #ccの場合も区切りでひとつに
    #bcc についてはメールヘッダに記述しないので項目なし
    msg["Date"]    = formatdate(localtime=True)

    to_addrs = to_address + cc_address + bcc_address
    #メールの送信先を一つのリスト型にまとめる bcc
    #は宛先にのみに含めヘッダに入れない

    smtp = smtplib.SMTP() #引数を省略すると localhost:25
    smtp.connect()
    #上記コマンドの引数を省略した場合初期化を明示する必要がある
    smtp.sendmail(from_address, to_addrs, msg.as_string())
    smtp.close()
