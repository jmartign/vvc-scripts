Name:           resource-agents-vvc
Version:        1 
Release:        5
Summary:        Reusable cluster resource scripts by Vadym Chepkov

Group:          System Environment/Base 
License:        BSD
URL:            http://www.chepkov.com/rpms/

Source0:        ldap
Source1:        daemon
Source2:        link

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     	noarch
Requires:	resource-agents >= 1.0.4

%description
Scripts to allow common services to operate in a High Availability environment.

%install
rm -rf $RPM_BUILD_ROOT

%{__install} -dm 755 ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/vvc
%{__install} -pm 755 %{SOURCE0} ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/vvc
%{__install} -pm 755 %{SOURCE1} ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/vvc
%{__install} -pm 755 %{SOURCE2} ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/vvc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir /usr/lib/ocf/resource.d/vvc
/usr/lib/ocf/resource.d/vvc/*

%changelog
* Wed Feb 16 2011 Vadym Chepkov <vvc@chepkov.com> - 1-5
- modified for resource-agents 1.0.4

* Mon Jun 14 2010 Vadym Chepkov <vvc@chepkov.com> - 1-4
- added link agent

* Sat Jun 12 2010 Vadym Chepkov <vvc@chepkov.com> - 1-3
- changed parameter name from binary to binfile

* Thu Jun 10 2010 Vadym Chepkov <vvc@chepkov.com> - 1-2
- added monitoring script to daemon RA

* Wed Jun 09 2010 Vadym Chepkov <vvc@chepkov.com> - 1-1
- Initial version

