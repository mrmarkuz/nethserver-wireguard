Summary: NethServer wireguard integration
Name: nethserver-wireguard
Version: 1.0.0
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name} 
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

Requires: wireguard-dkms, wireguard-tools

BuildRequires: perl
BuildRequires: nethserver-devtools 

%description
NethServer Wireguard integration

%prep
%setup

%build
perl createlinks
mkdir -p root/var/lib/nethserver/zammad/backup

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} \
#  --dir /var/lib/nethserver/zammad/backup 'attr(755, postgres, postgres)' \
%{buildroot} > %{name}-%{version}-filelist

%post

%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update

%changelog
