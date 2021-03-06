#!/bin/bash

UCBMAIL=/bin/mail
TMP=/tmp
LOGFILE=/var/log/named/log.0
NOTIFY="," #mail address
BODY="DNSサーバーのログファイル内でエラーを確認しましたので調査してください"

cat ${LOGFILE} | grep "failed to connect" > ${TMP}/failed_to_connect.txt

if [ -s ${TMP}/failed_to_connect.txt ]; then
  sed -i '1s/^/'${BODY}'\n\n/' ${TMP}/failed_to_connect.txt #先頭に文章を追加
  cat ${TMP}/failed_to_connect.txt | ${UCBMAIL} -s "named failed to connect" ${NOTIFY}
fi
