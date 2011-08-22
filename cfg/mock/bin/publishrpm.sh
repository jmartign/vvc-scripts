#!/bin/bash

REPOHOST=hut
REPOROOT=/var/www/vvc/rpms/redhat/5

#publish src rpm first
cd /var/lib/mock/epel-5-i386/result
rpm-sign *.src.rpm
scp -p *.src.rpm ${REPOHOST}:${REPOROOT}/SRPMS/
ssh ${REPOHOST} createrepo --checksum sha ${REPOROOT}/SRPMS/

for arch in i386 x86_64
do
  cd /var/lib/mock/epel-5-${arch}/result
  rm -f *.src.rpm
  rm -f *debuginfo*.rpm
  rpm-sign *.rpm
  scp -p *.rpm ${REPOHOST}:${REPOROOT}/${arch}/
  ssh ${REPOHOST} createrepo --checksum sha -g repodata/comps.xml ${REPOROOT}/${arch}/
done
