Name:           vvc-release       
Version:        5 
Release:        0
Summary:        VVC Repository Configuration

Group:          System Environment/Base 
License:        BSD
URL:            http://www.chepkov.com/rpms/

Source0:        http://www.chepkov.com/VVC-GPG-KEY
Source1:        vvc.repo	

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     	noarch
Requires:      	redhat-release >= %{version}

%description
This repository holds all RPM's built by Vadym Chepkov <vvc@chepkov.com>
This package contains the repository GPG key as well as configuration for the Yum

%prep
%setup -q  -c -T
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%build

%install
rm -rf $RPM_BUILD_ROOT

#GPG Key
%{__install} -Dpm 644 %{SOURCE0} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg/VVC-GPG-KEY

# yum
%{__install} -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
%{__install} -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/*

%changelog
* Sat Jan 17 2009 Vadym Chepkov <vvc@chepkov.com> - 5-0
- Initial verison
