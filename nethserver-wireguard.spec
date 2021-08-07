Summary: NethServer wireguard integration
Name: nethserver-wireguard
Version: 1.0.0
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name}
Source0: %{name}-%{version}.tar.gz
Source1: wg-manager.tar.gz
BuildArch: noarch

Requires: wireguard-dkms, wireguard-tools, rh-python38-python-pip

BuildRequires: perl
BuildRequires: nethserver-devtools


%description
NethServer Wireguard integration

%prep
%setup

%build
perl createlinks

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/opt/wg-manager
tar xvf %{SOURCE1} -C %{buildroot}/opt/wg-manager/

mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/%{name}/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
cp -a ui/* %{buildroot}/usr/share/cockpit/%{name}/

%{genfilelist} %{buildroot} | grep -v -e '/opt/wg-manager' > %{name}-%{version}-filelist

# don't compile python
exit 0

%post

%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%config %attr (0440,root,root) %{_sysconfdir}/sudoers.d/90_wg-manager
%config %attr (0775,root,root) /usr/libexec/nethserver/api/%{name}/read
%config %attr (0664,root,root) %{_sysconfdir}/systemd/system/wg-manager.service
%dir %attr(0755,wg-manager,wg-manager) /opt/wg-manager
%attr(-,wg-manager,wg-manager) /opt/wg-manager

%pre
# ensure wg-manager user exists:
if ! getent passwd wg-manager >/dev/null ; then
   useradd -r -U -d /opt/wg-manager wg-manager
fi

%changelog
* Tue Jul 27 2021 Markus Neuberger <dev@markusneuberger.at> - 1.0.0-1
  - Initial release
