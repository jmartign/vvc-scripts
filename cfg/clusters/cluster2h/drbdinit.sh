#!/bin/bash

set -e
dd if=/dev/zero of=/dev/xvda3 bs=4k count=1
dd if=/dev/zero of=/dev/xvda5 bs=4k count=1
sync
drbdadm -- --force create-md all
modprobe -s drbd
drbdadm up all
case `hostname` in
  c20) resource=u00 ;;
  c21) resource=u01 ;;
  *) echo "Unknown host" >&2
     exit 1 ;;
esac
drbdadm -- --overwrite-data-of-peer primary $resource
sleep 5
mkfs -j /dev/drbd/by-res/$resource
tune2fs -e continue -i 0 -c 0 /dev/drbd/by-res/$resource
