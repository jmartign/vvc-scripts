%define	_libexecdir	%{_libdir}/amanda
%{!?defconfig:%define defconfig vvc}
%{!?indexserver:%define indexserver amandahost}
%{!?tapeserver:%define tapeserver %{indexserver}}
%{!?amanda_user:%define amanda_user amanda}
%{!?amanda_group:%define amanda_group disk}

# XXX append lib to current _localstatedir setting
%{expand: %%define	_localstatedir	%{_localstatedir}/lib}

Summary: A network-capable tape backup solution
Name: amanda
Version: 2.5.2p1
Release: 8.vvc.2%{?dist}
Source: http://download.sourceforge.net/amanda/amanda-%{version}.tar.gz
Source1: amanda.crontab
Source4: disklist
Source5: amanda-xinetd
Source8: amandahosts
Patch1: amanda-2.5.2p1-pie.patch
Patch3: amanda-2.5.2p1-ylwrapNotFound.patch
Patch4: amanda-2.5.2p1-undefSymbols.patch
#Patch5: amanda-2.5.2p1-xattrs.patch
Patch6: amanda-2.5.2p1-typo_chg_multi.patch
License: BSD
Group: Applications/System
URL: http://www.amanda.org
Prereq: fileutils grep initscripts
BuildRequires: dump gnuplot cups samba-client tar grep fileutils
BuildRequires: libtool automake autoconf gcc-c++ readline-devel /usr/bin/Mail
BuildRequires: krb5-devel rsh openssh-clients ncompress mtx mt-st
Requires: tar /usr/bin/Mail
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%description 
AMANDA, the Advanced Maryland Automatic Network Disk Archiver, is a
backup system that allows the administrator of a LAN to set up a
single master backup server to back up multiple hosts to one or more
tape drives or disk files.  AMANDA uses native dump and/or GNU tar
facilities and can back up a large number of workstations running
multiple versions of Unix.  Newer versions of AMANDA (including this
version) can use SAMBA to back up Microsoft(TM) Windows95/NT hosts.
The amanda package contains the core AMANDA programs and will need to
be installed on both AMANDA clients and AMANDA servers.  Note that you
will have to install the amanda-client and/or amanda-server packages as
well.

%package client
Summary: The client component of the AMANDA tape backup system.
Group: Applications/System
Prereq: fileutils grep /sbin/service xinetd
Requires(pre): amanda = %{version}

%description client
The Amanda-client package should be installed on any machine that will
be backed up by AMANDA (including the server if it also needs to be
backed up).  You will also need to install the amanda package on each
AMANDA client machine.

%package server
Summary: The server side of the AMANDA tape backup system.
Group: Applications/System
Requires: gnuplot
Prereq: fileutils grep /sbin/service
Requires(pre): amanda = %{version}

%description server
The amanda-server package should be installed on the AMANDA server,
the machine attached to the device(s) (such as a tape drive) where backups
will be written. You will also need to install the amanda package on
the AMANDA server machine.  And, if the server is also to be backed up, the
server also needs to have the amanda-client package installed.

%package devel
Summary: Libraries and documentation of the AMANDA tape backup system.
Group: Development/Libraries
Requires(pre): amanda = %{version}

%description devel
The amanda-devel package should be installed on any machine that will
be used to develop amanda applications.

%prep
%setup -q
%patch1 -p1 -b .pie
%patch3 -p1 -b .ylwrapNotFound
%patch4 -p1 -b .undefSymbols
# %patch5 -p1 -b .xattrs
%patch6 -p1 -b .typo_chg_multi
./autogen

%build
export CFLAGS="-g -m32 -march=i386 -mtune=generic -D_FILE_OFFSET_BITS=64 -D_GNU_SOURCE"
export SED=sed

%configure --enable-shared \
	--disable-static \
	--disable-dependency-tracking \
	--with-index-server=%{indexserver} \
	--with-tape-server=%{tapeserver} \
	--with-config=%{defconfig} \
	--with-gnutar-listdir=%{_localstatedir}/amanda/gnutar-lists \
	--with-smbclient=%{_bindir}/smbclient \
	--with-dumperdir=%{_libdir}/amanda/dumperdir \
  --with-tcpportrange=49100,49199 \
  --with-udpportrange=850,859 \
	--with-amandahosts \
	--with-user=%amanda_user \
	--with-group=%amanda_group \
	--with-tmpdir=/var/log/amanda \
	--with-gnutar=/bin/tar \
	--with-ssh-security \
	--with-rsh-security \
	--with-bsdtcp-security \
	--with-bsdudp-security \
	--with-krb5-security
	
make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
export SED=sed

make install BINARY_OWNER=%(id -un) SETUID_GROUP=%(id -gn) DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/xinetd.d
perl -p -e "s,\@LIBDIR\@,%{_libexecdir},g" < %SOURCE5 > $RPM_BUILD_ROOT/etc/xinetd.d/amanda
chmod 644 $RPM_BUILD_ROOT/etc/xinetd.d/amanda
mkdir -p $RPM_BUILD_ROOT/var/log/amanda
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/amanda
install -m 600 %SOURCE8 $RPM_BUILD_ROOT%{_localstatedir}/amanda/.amandahosts

mkdir -p examples
cp example/* examples
rm -f examples/Makefile*
rm -f examples/config.site

pushd tape-src/.libs
install -m 755 amtapetype $RPM_BUILD_ROOT/%{_sbindir}
popd

rm -r ${RPM_BUILD_ROOT}%{_libdir}/amanda/dumperdir
rmdir --ignore-fail-on-non-empty ${RPM_BUILD_ROOT}%{_libdir}/amanda

pushd ${RPM_BUILD_ROOT}
  mkdir -p .%{_sysconfdir}/amanda/%defconfig
  cp ${RPM_SOURCE_DIR}/amanda.crontab .%{_sysconfdir}/amanda/crontab.sample
  cp ${RPM_SOURCE_DIR}/disklist .%{_sysconfdir}/amanda/%defconfig
  cp ${RPM_BUILD_DIR}/%{name}-%{version}/examples/amanda.conf .%{_sysconfdir}/amanda/%{defconfig}
  cp ${RPM_BUILD_DIR}/%{name}-%{version}/examples/amanda-client.conf .%{_sysconfdir}/amanda/%{defconfig}
  cp ${RPM_SOURCE_DIR}/disklist .%{_sysconfdir}/amanda/%defconfig
  touch .%{_sysconfdir}/amandates

  mkdir -p .%{_localstatedir}/amanda/gnutar-lists
  mkdir -p .%{_localstatedir}/amanda/%defconfig/index

  chmod 755 .%{_libdir}/libam*
popd
cp examples/amanda.conf $RPM_BUILD_ROOT%{_sysconfdir}/amanda/%{defconfig}
cp examples/amanda-client.conf $RPM_BUILD_ROOT%{_sysconfdir}/amanda/%{defconfig}
rm -rf $RPM_BUILD_ROOT/usr/share/amanda
rm $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean 
rm -rf ${RPM_BUILD_ROOT}

%pre
/usr/sbin/useradd -M -n -g %amanda_group -o -r -d %{_localstatedir}/amanda -s /bin/bash \
	-c "Amanda user" -u 33 %amanda_user >/dev/null 2>&1 || :



%post -p /sbin/ldconfig

%post client
/sbin/ldconfig
[ -f /var/lock/subsys/xinetd ] && /sbin/service xinetd reload > /dev/null 2>&1 || :

%post server
/sbin/ldconfig

%postun -p /sbin/ldconfig

%postun client
/sbin/ldconfig
[ -f /var/lock/subsys/xinetd ] && /sbin/service xinetd reload > /dev/null 2>&1 || :

%postun server
/sbin/ldconfig

%files
%defattr(-,root,root)
					%{_libdir}/libamanda-*.so
					%{_libdir}/libamtape-*.so
					%{_libdir}/libamserver-*.so
					%{_libdir}/librestore-*.so
					%{_libdir}/libamclient-*.so
					%{_libdir}/libamandad-*.so
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amrestore
					%{_mandir}/man8/amrestore.8*
%attr(600,%amanda_user,%amanda_group)	%config(noreplace) %{_localstatedir}/amanda/.amandahosts

%attr(02700,%amanda_user,%amanda_group) %dir /var/log/amanda
%attr(-,%amanda_user,%amanda_group)	%dir %{_localstatedir}/amanda/
%attr(-,%amanda_user,%amanda_group)	%dir %{_sysconfdir}/amanda/
%attr(-,%amanda_user,%amanda_group)	%config(noreplace) %{_sysconfdir}/amandates

%{_mandir}/man5/amanda.conf*

%files server
%defattr(-,root,root)
%doc examples COPYRIGHT* NEWS README
%attr(-,%amanda_user,%amanda_group)	%dir %{_libexecdir}/
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amidxtaped
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amindexd
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amlogroll
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amtrmidx
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amtrmlog
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/driver
%attr(4750,root,%amanda_group)	%{_libexecdir}/dumper
%attr(4750,root,%amanda_group)	%{_libexecdir}/planner
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/taper
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chunker
#%attr(-,%amanda_user,%amanda_group)	%dir %{_libdir}/amanda
#%attr(-,%amanda_user,%amanda_group)	%dir %{_libdir}/amanda/dumperdir
#%attr(-,%amanda_user,%amanda_group)	%{_libdir}/amanda/dumperdir/generic-dumper
#%attr(-,%amanda_user,%amanda_group)	%{_libdir}/amanda/dumperdir/gnutar
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amcleanupdisk
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-chio
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-chs
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-juke
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-manual
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-mcutil
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-mtx
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-multi
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-null
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-rait
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-rth
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-scsi
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-zd-mtx
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-disk
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-iomega
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/chg-lib.sh
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amcat.awk
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amplot.awk
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amplot.g
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amplot.gp

%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amaespipe
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amadmin
%attr(4750,root,%amanda_group)		%{_sbindir}/amcheck
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amcrypt
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amcrypt-ossl
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amcrypt-ossl-asym
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amflush
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amgetconf
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amlabel
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amtape
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amreport
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amcheckdb
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amcleanup
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amdump
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amoverview
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amrmtape
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amtoc
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amverify
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amstatus
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amplot
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amtapetype
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amdd
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/ammt
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amverifyrun

%attr(-,%amanda_user,%amanda_group)	%dir %{_localstatedir}/amanda/%defconfig/
%attr(-,%amanda_user,%amanda_group)	%dir %{_localstatedir}/amanda/%defconfig/index
%attr(-,%amanda_user,%amanda_group)	%dir %{_sysconfdir}/amanda
%attr(-,%amanda_user,%amanda_group)	%dir %{_sysconfdir}/amanda/%defconfig
%attr(-,%amanda_user,%amanda_group)	%config(noreplace) %{_sysconfdir}/amanda/%defconfig/amanda.conf
%attr(-,%amanda_user,%amanda_group)	%config(noreplace) %{_sysconfdir}/amanda/crontab.sample
%attr(-,%amanda_user,%amanda_group)	%config(noreplace) %{_sysconfdir}/amanda/%defconfig/disklist

%{_mandir}/man8/amadmin.8*
%{_mandir}/man8/amaespipe.8*
%{_mandir}/man8/amanda.8*
%{_mandir}/man8/amcheck.8*
%{_mandir}/man8/amcheckdb.8*
%{_mandir}/man8/amcleanup.8*
%{_mandir}/man8/amcrypt.8*
%{_mandir}/man8/amdd.8*
%{_mandir}/man8/amdump.8*
%{_mandir}/man8/amflush.8*
%{_mandir}/man8/amgetconf.8*
%{_mandir}/man8/amlabel.8*
%{_mandir}/man8/ammt.8*
%{_mandir}/man8/amoverview.8*
%{_mandir}/man8/amplot.8*
%{_mandir}/man8/amreport.8*
%{_mandir}/man8/amrmtape.8*
%{_mandir}/man8/amstatus.8*
%{_mandir}/man8/amtape.8*
%{_mandir}/man8/amtapetype.8*
%{_mandir}/man8/amtoc.8*
%{_mandir}/man8/amverify.8*
%{_mandir}/man8/amverifyrun.8*
%{_mandir}/man8/amcrypt-ossl.8*
%{_mandir}/man8/amcrypt-ossl-asym.8*

%files client
					%defattr(-,root,root)
					%config(noreplace) /etc/xinetd.d/amanda
%attr(-,%amanda_user,%amanda_group)	%dir %{_libexecdir}/
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/noop
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/amandad
%attr(4750,root,%amanda_group)		%{_libexecdir}/calcsize
%attr(4750,root,%amanda_group)		%{_libexecdir}/killpgrp
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/patch-system
%attr(4750,root,%amanda_group)		%{_libexecdir}/rundump
%attr(4750,root,%amanda_group)		%{_libexecdir}/runtar
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/selfcheck
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/sendbackup
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/sendsize
%attr(-,%amanda_user,%amanda_group)	%{_libexecdir}/versionsuffix
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amfetchdump
					%{_mandir}/man8/amfetchdump.8*
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amrecover
%attr(-,%amanda_user,%amanda_group)	%{_sbindir}/amoldrecover
					%{_mandir}/man8/amrecover.8*
					%{_mandir}/man5/amanda-client.conf.5*
%attr(-,%amanda_user,%amanda_group)	%{_localstatedir}/amanda/gnutar-lists/
%attr(-,%amanda_user,%amanda_group)	%config(noreplace) %{_sysconfdir}/amanda/%defconfig/amanda-client.conf

%files devel
%defattr(-,root,root)
%{_libdir}/libamanda.so
%{_libdir}/libamtape.so
%{_libdir}/libamclient.so
%{_libdir}/libamserver.so
%{_libdir}/librestore.so
%{_libdir}/libamandad.so

%changelog
* Tue Aug 28 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-8
- rebuild

* Fri Aug 17 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-7
- BuildRequires mtx and mt-st (#251690).

* Fri Aug 10 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-6
- Included upstream patch for chg-multi.sh (#251316).

* Wed Aug 08 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-5
- Added ssh and ncompress to BuildRequires (#250730).
- Removed some obsolete makes from build section.

* Thu Jul 12 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-4
- Enable backing up ACL/SElinux xattrs with tar (#201916).
- Removed obsolete patches and sources.

* Mon Jun 25 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-3
- Update -undefSymbols patch. All undefined symbols reported by
  'ldd -r' should now be fixed (#198178).

* Fri Jun 22 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-2
- Fix undefined symbols in libamserver.so.
- Fix ./autogen so it automatically installs ylwrap (bug 224143).
- Run ./autogen in prep section (otherwise the -pie patch had no effect).
- Update -pie patch.

* Thu Jun 21 2007 Radek Brich <rbrich@redhat.com> 2.5.2.p1-1
- New upstream version.
- Client rpm now installs amanda-client.conf.
- Removed obsolete patches -bug18322 and -rsh.
- Clean up spec file (non-utf8 error and some warnings from rpmlint).

* Mon Feb 19 2007 Jay Fenlason <fenlason@redhat.com> 2.5.1p3-1%{?dist}
- Upgrade to new upstream release, now that 2.5.1 is somewhat stable.
- Note that this requires changing the xinetd configuration and amanda.conf
  because of the new authentication mechanism.
- -server subpackage does not require xinetd.
- -server scriptlets do not need to reload xinetd.

* Mon Sep 25 2006 Jay Fenlason <fenlason@redhat.com> 2.5.0p2-4
- Include my -dump_size patch to close
  bz#206129: Dump output size determined incorrectly
- Clean up the spec file, following some suggestions in
  bz#185659: amanda 2.5.0
- Use a tarball without the problematic contrib/sst directory.
- Include my new_gnutar (based on a patch by Orion Poplawski
  <orion@cora.nwra.com>) to work around changed incremental file format
  in newer (>1.15.1) versions of gnutar.
- include my -wildcards patch to turn on wildcards with new versions of tar.

* Tue Sep 5 2006 Jay Fenlason <fenlason@redhat.com> 2.5.0p2-3
- move libamclient-*.so to the base rpm, so that multilib support works.
  This fixes
  bz#205202 File conflicts

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.0p2-2.1
- rebuild

* Thu Jun 8 2006 Jay Fenlason <fenlason@redhat.com> 2.5.0p2-2
- New upstream version
- Make the BuildRequires on /usr/bin/Mail rather than mailx, because we
  don't really care where the Mail command comes from.
- include the amcheck_badtape patch by Paul Bijnens
  <paul.bijnens@xplanation.com> to fix a problem where amcheck doesn't
  realize the wrong tape is in the drive.
- include the error_msg patch from Jean-Louis Martineau <martineau@zmanda.com>
  to fix a double-free problem
- include the restore patch from Jean-Louis Martineau <martineau@zmanda.com>
  to fix an error in amrestore
- include a slightly modified form of the big_holding_disk patch from
  Andrej Filipcic <andrej.filipcic@ijs.si> to fix a problem with holding
  disks bigger than 4tb

* Mon May 22 2006 Jesse Keating <jkeating@redhat.com> 2.5.0-3
- Fix BuildReqs

* Fri Apr 7 2006 Jay Fenlason <fenlason@redhat.com> 2.5.0-2
- New upstream release: 2.5.0, with new features
- Do not include our own amanda.conf anymore, use the one from the
  tarball.
- Remove the static libraries.
- Update the -pie patch
- Turn on the new -with-ssh-security option.
- Change the mode of ~amanda/.amandahosts to 600, since 2.5.0 requires
  it.
- actually use the defconfig macro it this spec file.
- Change the name of the index server to "amandahost" from localhost.
  Users should ensure that "amandahost.their-domain" points to their
  Amanda server.
- Change amandahosts likewise.
- Add dependency on /usr/bin/Mail
- Ensure unversioned .so files are only in the -devel rpm.
- Remove DUMPER_DIR and the files in it, as nothing seems to actually
  use them.
- Include the -overflow patch from Jean-Louis Martineau
  <martineau@zmanda.com>

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.4.5p1-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.4.5p1-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Jay Fenlason <fenlason@redhat.com> 2.4.5p1-3
- Fix spec file to use %%{_localstatedir} instead of hardcoding /var/lib
- Add amanda_user and amanda_group defines, to make changing the username
  easier.
- Add a BuildRequires on /usr/bin/Mail

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 4 2005 Jay Fenlason <fenlason@redhat.com>
- New upstream release.

* Sun Jul 31 2005 Florian La Roche <laroche@redhat.com>
- make sure amanda builds with newest rpm

* Wed Apr 20 2005 Jay Fenlason <fenlason@redhat.com> 2.4.5-2
- New upstream release.  This obsoletes the -bug144052 patch.
- Reorg this spec file slightly to allow someone to specify
  index server, tape server and default configuration when
  rebuilding the rpms via something like
  'rpmbuild -ba --define "indexserver foo.fqdn.com" amanda.spec'
  This change suggested by Matt Hyclak <hyclak@math.ohiou.edu>.
  
* Tue Apr 5 2005 Jay Fenlason <fenlason@redhat.com> 2.4.4p4-4
- Add -bug144052 patch to close
  bz#144052 amverifyrun sometimes verifies the wrong tapes

* Tue Mar 8 2005 Jay Fenlason <fenlason@redhat.com> 2.4.4p4-3
- rebuild with gcc4

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.4.4p4-2
- Rebuilt for new readline.

* Mon Oct 25 2004 Jay Fenlason <fenlason@redhat.com> 2.4.4p4-1
- New upstream version
- Turn on --disable-dependency-tracking to work around an automake bug.

* Fri Jun 28 2004 Jay Fenlason <fenlason@redhat.com> 2.4.4p3-1
- New upstream version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 19 2004 Jay Fenlason <fenlason@redhat.com> 2.4.4p2-3
- make a few more programs PIE by updating the amanda-2.4.4p2-pie.path

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 13 2004 Jay Fenlason <fenlason@redhat.com> 2.4.4p2-1
- New upstream version, includes the -sigchld and -client-utils
  patches.  Also includes a new chg-disk changer script and a new
  amqde "quick-and-dirty estimate" program (called from sendsize--not
  a user command.

* Wed Jul 23 2003 Jay Fenlason <fenlason@redhat.com> 2.4.4p1-1
- Merge from 2.4.4p1-0.3E

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 26 2003 Jay Fenlason <fenlason@redhat.com> 2.4.4-0
- New upstream version.

* Thu Feb 13 2003 Jay Fenlason <fenlason@redhat.com> 2.4.3-3
- Removed call to signal(SIGCHLD, SIG_IGN) which prevents wait...()
  from working on newer Red Hat systems.  This fixes bug #84092.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Jay Fenlason <fenlason@redhat.com> 2.4.3-2
- Add spec file entry for /usr/lib/amanda so owner/group set
  correctly  Fixes bugs 74025 and 73379.

* Wed Nov 20 2002 Elliot Lee <sopwith@redhat.com> 2.4.3-1
- Update to version 2.4.3, rebuild
- Update patch for bug18322 to match

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  2 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.4.2p2-7
- Don't strip explicitly
- Require samba-client instead of /usr/bin/smbclient

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.4.2p2-6
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jul 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Build and install the "tapetype"  utility program, for
  tape size identification (#48745)  

* Tue Jun 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
- don't use %%configure, to make it build

* Mon Apr  9 2001 Bill Nottingham <notting@redhat.com>
- include ia64 again

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.4.2p2 - fixes problems with amrecover (#26567)
- made config files noreplace
- don't build on IA64 right now, amanda doesn't like
  the dump there: It segfaults.

* Fri Mar 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add /usr/bin/smbclient to buildprereq (#31996), to
  avoid samba being built without such support

* Thu Feb 22 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%{version} in source URL, and thus actually use 
  2.4.2p1 instead of 2.4.2 (doh! # 28759)
- add patch to handle bogus /dev/root entries (#28759)

* Fri Feb 16 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.4.2p1 bugfix release
- move amandaixd and amidxtape to the server package (#28037)

* Wed Jan 31 2001 Trond Eivind Glomsrød <teg@redhat.com>
- move /etc/xinetd.d/amanda to the client subpackage (#25430)

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- don't have "chunksize -1" as the default, as it's no longer
  supported
- make it uid amanda, with home /var/lib/amada
  so programs can actually access it (#20510)
- make .amandahosts a config file (#18322)

* Tue Jan 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.4.2
- make the UDP service "wait" (#23047)

* Tue Oct 10 2000 Jeff Johnson <jbj@redhat.com>
- build with shared libraries.
- add amanda-devel package to contain static libraries.
- update to 2.4.2-19991216-beta1 (#16818).
- sort out client-server file confusions (#17232).
- amandaidx-xinetd should have "wait = no" (#17551).
- /var/lib/amanda needs operator.disk ownership (17913).
- /etc/xinetd.d/amanda added to the amanda-server package (#18112).
- ignore socket error message (#18322).

* Sun Sep  3 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- do not include /etc/xinetd.d/amandaidx in the server rpm

* Mon Aug 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- only do reload of xinetd if xinetd is running (#16653)
- don't show output of reload command to STDOUT (#16653)
- don't use /usr/sbin/tcpd in amidx, xinetd is linked
  with tcp_wrappers
- prereq initscripts (fixes #14572 and duplicates)

* Tue Aug  1 2000 Bill Nottingham <notting@redhat.com>
- turn off amandaidx by default (#14937)
- fix some binary permissions (#14938)

* Tue Aug  1 2000 Matt Wilson <msw@redhat.com>
- added Prereq: /sbin/service xinetd to client and server subpackages

* Tue Jul 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- xinetd support

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- add prereqs for scriptlets, requires for common package.

* Sat Jun 10 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- move to 7.0 distro.

* Tue May 23 2000 Tim Powers <timp@redhat.com>
- built for 7.0
- man pages in /usr/share/man

* Thu Apr 27 2000 Tim Powers <timp@redhat.com>
- added usr/lib/amanda/chg-zd-mtx to the client RPM to fix bug #8282

* Wed Mar 8 2000 Tim Powers <timp@redhat.com>
- fixed files/dirs ending up in the wrong packages.
- last time it wasn't built with dump (doh!), this time it is. Now has a
	BuildRequires for dump.

* Thu Feb 10 2000 Tim Powers <timp@redhat.com>
- strip binaries

* Fri Jan 21 2000 TIm Powers <timp@redhat.com>
- added chown lines to post section

* Tue Jan 11 2000 Tim Powers <timp@redhat.com>
- make sure the man pages are gzipped in each subpackage, overriding the build
	system spec_install_post macro.
- using mega spec file changes from Marc Merlin <merlin_bts@valinux.com> since
	the package we were shipping in the past had some major issues (not in
	Marc's words ;)
- using Marc's added README and modified config files.
- adapted patches written by Alexandre Oliva <oliva@dcc.unicamp.br> from Marc
	Merlin's package so that the patch matches the source version (the patches
	are the glibc2.1 and glibc2.2 patches)

* Mon Jan 3 2000 Tim Powers <timp@redhat.com>
- fix so configure doesn't crap out (libtoolize --force)
- gzip man pages, strip binaries
- rebuilt for 6.2

* Thu Aug 5 1999 Tim Powers <timp@redhat.com>
- applied patch so that it reports the available holding disk space correctly

* Thu Jul 8 1999 Tim Powers <timp@redhat.com>
- added %defattr lines
- rebuilt for 6.1

* Wed May 05 1999 Bill Nottingham <notting@redhat.com>
- update to 2.4.1p1

* Tue Oct 27 1998 Cristian Gafton <gafton@redhat.com>
- version 2.4.1

* Tue May 19 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to full 2.4.0 release

* Thu Feb 19 1998 Otto Hammersmith <otto@redhat.com>
- fixed group for -client and -server packages (Network->Networking)

* Wed Feb 11 1998 Otto Hammersmith <otto@redhat.com>
- updated to 2.4.0b6, fixes security hole among other things
  (as well as finally got the glibc patch in the main source.)
 
* Tue Jan 27 1998 Otto Hammersmith <otto@redhat.com>
- moved versionsuffix to client package to remove dependency of amanda on amanda-client

* Mon Jan 26 1998 Otto Hammersmith <otto@redhat.com>
- fixed libexec garbage.

* Wed Jan 21 1998 Otto Hammersmith <otto@redhat.com>
- split into three packages amanda, amanda-client, and amanda-server

* Fri Jan  9 1998 Otto Hammersmith <otto@redhat.com>
- updated to latest beta... builds much cleaner now.

* Thu Jan  8 1998 Otto Hammersmith <otto@redhat.com>
- created the package

