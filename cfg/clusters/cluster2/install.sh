#!/bin/sh

VHOST=$1

if [ -z "$VHOST" ] ; then
  echo "Usage: $0 name" >&2
  exit 1
fi

VHOST=${VHOST#.}

set -- $(host $VHOST|grep address|tail -1)

HOSTNAME=$1
ADDR=$4

if [ -z "$HOSTNAME" -o -z "$ADDR" ] ; then
  echo "$VHOST not found in DNS" >&2
  exit 1
fi

lvcreate --size 3G --name $VHOST vg0
virsh destroy $VHOST
virsh undefine $VHOST
virt-install --name=$VHOST --ram=256 --vcpus=1 --network bridge=xenbr0 --network bridge=xenbr1 -p --disk=path=/dev/vg0/$VHOST --nographics --location=http://hut.chepkov.lan/iso/centos64 --extra-args="selinux=0 noipv6 headless ip=$ADDR netmask=255.255.255.0 gateway=10.10.10.250 dns=10.10.10.100 ks=http://chepkov.com/svn/cfg/cluster/kickstart.cfg ksdevice=eth0"
