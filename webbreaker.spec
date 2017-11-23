%define _unpackaged_files_terminate_build 0
%define name webbreaker
%define user webbreaker
%define group webbreaker
%define version 2.0
%define release 03
%define installdir /opt/webbreaker
%define allocated_id 666

Summary: Client for Dynamic Application Security Test Orchestration (DASTO).
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: MIT
Requires: shadow-utils, cronie, crontabs, glibc
Requires: /bin/rm, /usr/sbin/useradd, /usr/sbin/groupadd, /bin/ln, /usr/sbin/alternatives, /bin/sed, /usr/bin/getent, /usr/sbin/userdel
Packager: Brandon Spruth <brandon.spruth2@target.com>
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: x86_64
Vendor: Target Brands, Inc.
Url: https://github.com/target/webbreaker

%description
WebBreaker is an open source Dynamic Application Security Test Orchestration (DASTO) client, enabling development teams to release secure software with continuous delivery, visibility, and scalability.

%prep
%setup -q -n %{name}-%{version}

%pre
# Add the webbreaker user and group
getent group %{user} >/dev/null || groupadd -f -g %{allocated_id} -r %{user}
if ! getent passwd %{user} >/dev/null ; then
    if ! getent passwd %{allocated_id} >/dev/null ; then
      useradd -r -u %{allocated_id} -g %{user} -d %{installdir} -s /bin/sh -c "WebBreaker Client User" %{user}
    else
      useradd -r -g %{user} -d %{installdir} -s /bin/sh -c "WebBreaker User for DASTO" %{user}
    fi
fi
exit 0

#make sure no old log or pid files are here
rm -rf $RPM_BUILD_ROOT%{installdir}/log/*

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{installdir}
mkdir -p $RPM_BUILD_ROOT%{installdir}/log
mkdir -p $RPM_BUILD_ROOT%{installdir}/etc
install -d $RPM_BUILD_ROOT%{installdir}
install -d $RPM_BUILD_ROOT%{installdir}/log
install -d $RPM_BUILD_ROOT%{installdir}/etc
cp opt/webbreaker/webbreaker.bin $RPM_BUILD_ROOT/opt/webbreaker/webbreaker.bin
cp opt/webbreaker/etc/config.ini $RPM_BUILD_ROOT/opt/webbreaker/etc/config.ini
cp opt/webbreaker/etc/config.ini $RPM_BUILD_ROOT/opt/webbreaker/log/webbreaker.log


%post
/usr/bin/chown -R %{user}:%{user} %{installdir} 2> /dev/null
# Set up the alternatives files
#[ -d %{installdir}/log ] && rm -rf %{installdir}/log

/usr/sbin/alternatives --install /usr/bin/webbreaker webbreaker %{installdir}/webbreaker.bin 100
/usr/sbin/alternatives --auto webbreaker
/usr/sbin/alternatives --set webbreaker %{installdir}/webbreaker.bin

%preun

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,%{user},%{group},755)
%attr(755,%{user},%{group}) %dir %{installdir}
%attr(755,%{user},%{group}) %dir %{installdir}/log
%attr(755,%{user},%{group}) %dir %{installdir}/etc
%attr(755,%{user},%{group}) %{installdir}/webbreaker.bin
%attr(755,%{user},%{group}) %{installdir}/etc/config.ini
%attr(755,%{user},%{group}) %{installdir}/log/webbreaker.log

%changelog
* Wed Nov 22 2017 Target Product Security Engineering <brandon.spruth2@target.com> - 2.0-01
- Initial creation
