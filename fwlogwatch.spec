%define debug_package %{nil}

Summary:	Firewall log analyzer, report generator and realtime response agent
Name:		fwlogwatch
Version:	1.2
Release:	19
Group:		Monitoring
License:	GPL
URL:		https://fwlogwatch.inside-security.de/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}.service
Source2:	%{name}.sysconfig
Patch0:		fwlogwatch-mdv_conf.diff
BuildRequires:	adns-devel
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	pkgconfig(zlib)
Requires(post,preun): rpm-helper
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
fwlogwatch produces ipchains, netfilter/iptables, ipfilter, Cisco IOS and
Cisco PIX log summary reports in text and HTML form and has a lot of options
to find and display relevant patterns in connection attempts. With the data
found it can also generate customizable incident reports from a template and
send them to abuse contacts at offending sites or CERT coordination centers.
Finally, it can also run as daemon and report anomalies or start
countermeasures.

%prep

%setup -q
%patch0 -p1 -b .paths

chmod 644 contrib/fwlogsummary.cgi contrib/fwlogsummary_small.cgi

# fix encoding
sed -i -e "s|iso-8859-1|UTF-8|g" *.c

%build
%serverbuild

%make CFLAGS="$CFLAGS -DHAVE_ZLIB -DHAVE_GETTEXT -DHAVE_IPV6 -DHAVE_ADNS" LIBS="-L%{_libdir} -lcrypt -lz -ladns"

# fix encoding
pushd po

for i in de pt sv; do
    sed -i -e "s|ISO-8859-1|UTF-8|g" $i.po
    iconv --from-code=ISO-8859-1 --to-code=UTF-8 $i.po > $i.po.new; mv $i.po.new $i.po
done

for i in de ja pt sv zh_CN zh_TW; do
    msgfmt -v -o $i.mo $i.po
done

popd

%install

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8

install -D -m0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -m0755 fwlogwatch %{buildroot}%{_sbindir}
install -m0755 contrib/fwlw_notify %{buildroot}%{_sbindir}
install -m0755 contrib/fwlw_respond %{buildroot}%{_sbindir}
install -m0644 fwlogwatch.8 %{buildroot}%{_mandir}/man8
install -m0644 fwlogwatch.config %{buildroot}%{_sysconfdir}/

for i in de ja pt sv zh_CN zh_TW; do
    install -d %{buildroot}%{_datadir}/locale/${i}/LC_MESSAGES
    install -m0644 po/${i}.mo %{buildroot}%{_datadir}/locale/${i}/LC_MESSAGES/fwlogwatch.mo
done

%find_lang %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean

%files -f %{name}.lang
%doc AUTHORS COPYING CREDITS ChangeLog README
%doc contrib/fwlogsummary.cgi contrib/fwlogsummary_small.cgi
%doc contrib/fwlogwatch.php contrib/fwlw_notify contrib/fwlw_respond
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/fwlogwatch.config
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/fwlogwatch
%{_sbindir}/fwlw_notify
%{_sbindir}/fwlw_respond
%{_mandir}/man8/fwlogwatch.8*
