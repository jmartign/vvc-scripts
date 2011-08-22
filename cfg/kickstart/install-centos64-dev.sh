#!/bin/sh

lvcreate --size 10G --name centos64-dev vg0
virsh undefine centos64-dev
virt-install --name=centos64-dev --ram=512 --vcpus=2 -p --disk=path=/dev/vg0/centos64-dev --nographics --location=http://t100.chepkov.lan/linux/centos/5/x86_64/os --extra-args="selinux=0 noipv6 headless clocksource=jiffies ks=http://chepkov.com/svn/cfg/kickstart/centos64-dev.cfg"
