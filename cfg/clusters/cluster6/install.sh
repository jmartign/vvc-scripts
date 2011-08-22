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

virsh destroy $VHOST
virsh undefine $VHOST
lvremove -f /dev/vg0/$VHOST
lvcreate --size 4G --name $VHOST vg0
virt-install --name=$VHOST --ram=512 --vcpus=1 --network bridge=br0 -p --disk=path=/dev/vg0/$VHOST \
--nographics --location=http://t100.chepkov.lan/linux/redhat/6/x86_64/os \
--extra-args="selinux=0 noipv6 headless \
ip=$ADDR netmask=255.255.255.0 gateway=10.10.10.250 dns=10.10.10.100,10.10.10.9 ks=http://chepkov.com/svn/cfg/clusters/cluster6/kickstart.cfg"
