#!/bin/bash

set -o errexit
LOG=/var/log/crlpost.log
exec 3>&2
trap "cat $LOG >&3" ERR
exec &>$LOG

cd /root/CA
/usr/bin/openssl ca -gencrl -out crl.pem -config openssl.conf
/usr/bin/openssl crl -in crl.pem -out crl.crl -outform DER
/usr/bin/scp -p -o BatchMode=yes crl.crl vvc@chepkov.com:/var/www/vvc/vvc-ca.crl 
