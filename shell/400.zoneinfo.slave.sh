#!/bin/sh

HOST= #hostname
TYPE=slave
CONF=/var/named/chroot/etc/conf/slave
UCBMAIL=/bin/mail
TMP=/tmp
STATEDIR=/var/log/named/slave
NOTIFY="" #mail address

main()
{
        if [ -f ${STATEDIR}/zoneinfo ]; then
                cp ${STATEDIR}/zoneinfo ${STATEDIR}/zoneinfo.yesterday
        fi

        while read LINE; do
                echo $LINE | sed -ne 's/^zone \"\(..*\)\" IN .*/\1/p' >> ${TMP}/zoneinfo.$$
        done < $CONF

        sort ${TMP}/zoneinfo.$$ > ${STATEDIR}/zoneinfo

        rm -rf ${TMP}/zoneinfo.$$

        if [ -f ${STATEDIR}/zoneinfo.yesterday ]; then
                diff ${STATEDIR}/zoneinfo.yesterday ${STATEDIR}/zoneinfo | sed -n -e '/^>/s/>/+/p' -e '/^</s/</-/p' > ${STATEDIR}/zoneinfo.diff
        fi

        if [ -s ${STATEDIR}/zoneinfo.diff ]; then
                result | $UCBMAIL -s "${HOST} ${TYPE} zoneinfo" $NOTIFY
        fi

        exit 0
}

result()
{
        echo "${HOST} ${TYPE} zoneinfo"
        echo ""

        echo "##### diff from yesterday"
        echo ""

        cat ${STATEDIR}/zoneinfo.diff
        echo ""

        echo "##### ${HOST} ${TYPE} zone"
        cat ${STATEDIR}/zoneinfo
}


main $*

