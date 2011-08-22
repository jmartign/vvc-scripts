%define nagios_plugins_dir %{_libdir}/nagios/plugins

Name:           nagios-plugins-drbd
Version:        0.5.3
Release:        1%{?dist}
Summary:        Nagios plugin to monitor DRBD status

Group:          Applications/System
License:        GPLv2
URL:            http://exchange.nagios.org/directory/Plugins/Uncategorized/Operating-Systems/Linux/check_drbd
Source0:        check_drbd
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
This plugin allows you to monitor status of DRBD

%prep

%build

%install

rm -rf ${RPM_BUILD_ROOT}

%{__install} -dm 755 ${RPM_BUILD_ROOT}/%{nagios_plugins_dir}
%{__install} -pm 755 %{SOURCE0} ${RPM_BUILD_ROOT}/%{nagios_plugins_dir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{nagios_plugins_dir}/check_drbd

%changelog
* Sun Apr 24 2011 Vadym Chepkov <vvc@chepkov.com> - 0.5.3-1
- Initial version


