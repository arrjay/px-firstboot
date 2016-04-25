# axe debug package
%define debug_package %{nil}

# selinux hackery - http://lvrabec-selinux.rhcloud.com/2015/07/07/how-to-create-selinux-product-policy/
%global selinux_variants mls targeted
%global modulenames px-firstboot
#%global relabel_files(/usr/libexec/px-firstboot/*)

# see also http://fedoraproject.org/wiki/SELinux_Policy_Modules_Packaging_Draft
%{!?_selinux_policy_version: %global _selinux_policy_version %(sed -e 's,.*selinux-policy-\\([^/]*\\)/.*,\\1,' /usr/share/selinux/devel/policyhelp 2>/dev/null)}
%if "%{_selinux_policy_version}" != ""
Requires:	selinux-policy >= %{_selinux_policy_version}
%endif

# Usage: _format var format
#   Expand 'modulenames' into various formats as needed
#   Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

Name:		px-firstboot
Version:	0.1
Release:	1%{?dist}
Summary:	Firstboot Setup Tasks

Group:		System Environment/Base
License:	BSD
URL:		http://github.com/arrjay/px-firstboot
Source0:	https://github.com/arrjay/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:	systemd-units
BuildRequires:  checkpolicy
BuildRequires:	selinux-policy-devel
BuildRequires:	/usr/share/selinux/devel/policyhelp
Requires:	systemd
Requires(post):	/sbin/restorecon
Requires(post):	/usr/sbin/semodule

%description
Firstboot setup tasks, likely specific to packager's desires

%prep
%autosetup -n %{name}-%{version}


%build
# make the selinux policy
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile px-firstboot.pp
  mv px-firstboot.pp px-firstboot.pp.${selinuxvariant}
done


%install
%make_install ROOT=%{buildroot}
for selinuxvariant in %{selinux_variants}
do
  install -d -m 0755 %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 0644 px-firstboot.pp.${selinuxvariant} %{buildroot}%{_datadir}/selinux/${selinuxvariant}/px-firstboot.pp
done


%post
# install selinux policy
for selinuxvariant in %{selinux_variants}
do
  %{_sbindir}/semodule -n -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/px-firstboot.pp &> /dev/null || :
done
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %{_sbindir}/restorecon /usr/libexec/px-firstboot/startup
fi
# we hard override to enable here.
systemctl enable px-firstboot.service


%postun
# remove selinux module
for selinuxvariant in %{selinux_variants}
do
  %{_sbindir}/semodule -n -s ${selinuxvariant} -r px-firstboot &> /dev/null || :
done


%files
%defattr(0644,root,root,0755)
/etc/px-firstboot
/lib/systemd/system/px-firstboot.service
/var/lib/px-firstboot
/usr/libexec/px-firstboot
%attr(0755,root,root) /usr/libexec/px-firstboot/*
%{_datadir}/selinux/*/px-firstboot.pp
%doc /usr/share/doc/px-firstboot/LICENSE


%changelog

