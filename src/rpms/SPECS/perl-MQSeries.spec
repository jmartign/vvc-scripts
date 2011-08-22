Summary: MQSeries interface for perl
Name: perl-MQSeries
Version: 1.30
Release: 1
License: GPL+ or Artistic
Group: Applications/CPAN
URL: http://search.cpan.org/dist/MQSeries/

Source: http://www.cpan.org/modules/by-module/MQSeries/MQSeries-%{version}.tar.gz
Patch1: perl-MQSeries-rpath.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: perl >= 5.8.0
BuildRequires: MQSeriesSDK MQSeriesClient MQSeriesServer
Requires:  MQSeriesRuntime perl(Params::Validate) perl(Test::Simple) perl(Convert::EBCDIC) perl(Test::Pod)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:  perl(MQSeries) = %{version}-%{release}
AutoReqProv: no

%description
This module implements a perl5 API for the IBM MQSeries / WebSphere MQ
messaging middleware product API (often referred to as the MQI), as
well as:

Object Oriented (OO) interface to the MQI
OO interface to the MQSeries administrative commands via PCF or MQSC
OO interface to the various configuration, log, and error files

For more information on the MQSeries / WebSphere MQ product itself,
see the IBM website at: http://www-306.ibm.com/software/integration/wmq/

%package Client
Summary: Client API component for %{name}
Group: Applications/Registry
Requires: MQSeriesRuntime MQSeriesClient
Requires: perl(MQSeries) = %{version}-%{release}
Provides: MQSeries.so
AutoReqProv: no

%description Client
Client component for %{name}

%package Server
Summary: Server API component for %{name}
Group: Applications/Registry
Requires: MQSeriesRuntime MQSeriesServer
Requires: perl(MQSeries) = %{version}-%{release}
Provides: MQSeries.so
AutoReqProv: no

%description Server
Server component for %{name}

%prep
%setup -n MQSeries-%{version}
%patch1 -p1 -b .rpath

%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install
find %{buildroot} -name .packlist -delete

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYRIGHT LICENSE MANIFEST README
%{perl_vendorarch}/MQSeries/
%{perl_vendorarch}/auto/MQSeries/
%{perl_vendorarch}/MQSeries.pm
%{_mandir}/man3/*.3*

%files Client
%defattr(-,root,root,-)
%{perl_vendorarch}/MQClient/
%{perl_vendorarch}/auto/MQClient/

%files Server
%defattr(-,root,root,-)
%{perl_vendorarch}/MQServer/
%{perl_vendorarch}/auto/MQServer/

%changelog
* Tue Dec 22 2009 soa_support@lists.verizonbusiness.com - 1.30-1
- Using official 1.30 distribution

* Fri Jul 31 2009 Vadym Chepkov <Vadym.Chepkov@verizonbusiness.com> - 1.30-0
- Upgrade to 1.30

* Mon Jul 27 2009 Vadym Chepkov <Vadym.Chepkov@verizonbusiness.com> - 1.29-1
- Upgrade to 1.29

* Wed Jul 02 2008 Vadym Chepkov <Vadym.Chepkov@verizonbusiness.com> - 1.28-2
- Added missing dependencies

* Wed Jul 02 2008 Vadym Chepkov <Vadym.Chepkov@verizonbusiness.com> - 1.28-1
- Initial package.
