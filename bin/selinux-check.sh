#!/bin/bash
TMPFILE=/var/tmp/selinux-check.$$
trap "rm -f $TMPFILE" EXIT
set -o noclobber

/sbin/ausearch -m avc -ts yesterday --input-logs 2>&1|grep -v 'no matches' > $TMPFILE

if [ -s $TMPFILE ] ; then
	if [ -t 1 ] ; then
 		cat $TMPFILE 
	else
		mail -s "SELINUX Denials on `hostname`" root < $TMPFILE
    fi
fi

