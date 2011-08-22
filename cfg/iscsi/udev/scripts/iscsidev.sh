#!/bin/sh
 
BUS=${1}
HOST=${BUS%%:*}
LUN=`echo ${BUS} | cut -d":" -f4`
 
[ -e /sys/class/iscsi_host ] || exit 1
 
file="/sys/class/iscsi_host/host${HOST}/device/session*/iscsi_session*/targetname"
target_name=$(cat ${file} | cut -d":" -f2 | sed 's/\./_/')
 
logger "iscsidev called with $1 and returned ${target_name} ${LUN}"
echo "${target_name} ${LUN}"
