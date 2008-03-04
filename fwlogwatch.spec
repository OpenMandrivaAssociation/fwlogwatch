%define	name	fwlogwatch
%define	version	1.1
%define	release	%mkrel 5

Summary:	Firewall log analyzer, report generator and realtime response agent
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Monitoring
URL:		http://cert.uni-stuttgart.de/projects/fwlogwatch/
License:	GPL
Source0:	%{name}-%{version}.tar.bz2
Patch0:		%{name}-1.0-paths.patch.bz2
Patch1:		%{name}-0.6-initscript.patch.bz2
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(pre):		rpm-helper

%description
fwlogwatch produces ipchains, netfilter/iptables, ipfilter, Cisco IOS and
Cisco PIX log summary reports in text and HTML form and has a lot of
options to find and display relevant patterns in connection attempts. With
the data found it can also generate customizable incident reports from a
template and send them to abuse contacts at offending sites or CERT
coordination centers. Finally, it can also run as daemon and report
anomalies or start countermeasures.

%prep
%setup -q
%patch0 -p1 -b .paths
%patch1 -p1

%build
%serverbuild
%make OPTFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_initrddir}

mkdir -p $RPM_BUILD_ROOT%_datadir/locale/{de,ja,pt_BR,sv,zh_CN,zh_TW}/LC_MESSAGES

%makeinstall_std install-config install-i18n \
		MANDIR=%{_mandir}  INSTALL_DIR=%{_prefix}  CONF_DIR=%{_sysconfdir} \
		DATADIR=%{_datadir}

cp contrib/fwlogwatch.init.redhat %{buildroot}%{_initrddir}/fwlogwatch

%find_lang %{name}

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%post
%_post_service fwlogwatch

%preun
%_preun_service fwlogwatch

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING CREDITS ChangeLog README
%doc contrib/fwlogsummary.cgi contrib/fwlogsummary_small.cgi
%config(noreplace) %{_sysconfdir}/fwlogwatch.config
%config(noreplace) %{_sysconfdir}/fwlogwatch.template
%{_sbindir}/fwlogwatch
%{_sbindir}/fwlw_notify
%{_sbindir}/fwlw_respond
%config (noreplace) %{_initrddir}/fwlogwatch
%{_mandir}/man8/fwlogwatch.8*
