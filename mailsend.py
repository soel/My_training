#!/usr/bin/env python
# coding: utf-8

import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

if __name__ == "__main__":
    from_address = ""
    to_address   = ["", ""] #複数に送る場合はリスト型

    charset = "ISO-2022-JP"
    subject = u"メールの件名です"
    text    = u"メールの本文です"

    msg = MIMEText(text.encode(charset),"plain",charset)
    msg["Subject"] = Header(subject,charset)
    msg["From"]    = from_address
    msg["To"]      = ",".join(to_address) #ここは "," 区切りでひとつに
    msg["Date"]    = formatdate(localtime=True)

    smtp = smtplib.SMTP()
    smtp.connect()
    smtp.sendmail(from_address, to_address, msg.as_string())
    smtp.close()
