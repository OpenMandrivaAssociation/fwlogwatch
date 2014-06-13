Summary:	Firewall log analyzer, report generator and realtime response agent
Name:		fwlogwatch
Version:	1.2
Release:	10
Group:		Monitoring
License:	GPLv2
Url:		http://fwlogwatch.inside-security.de/
Source0:	%{name}-%{version}.tar.bz2
Source1:	fwlogwatch.init
Source2:	fwlogwatch.sysconfig
Patch0:		fwlogwatch-mdv_conf.diff

BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	adns-devel
BuildRequires:	pkgconfig(zlib)
Requires(post,preun):	rpm-helper

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
%apply_patches

cp %{SOURCE1} fwlogwatch.init
cp %{SOURCE2} fwlogwatch.sysconfig

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
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8

install -m0755 fwlogwatch.init %{buildroot}%{_initrddir}/%{name}
install -m0644 fwlogwatch.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

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
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f %{name}.lang
%doc AUTHORS COPYING CREDITS ChangeLog README
%doc contrib/fwlogsummary.cgi contrib/fwlogsummary_small.cgi
%doc contrib/fwlogwatch.php contrib/fwlw_notify contrib/fwlw_respond
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/fwlogwatch.config
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/fwlogwatch
%{_sbindir}/fwlw_notify
%{_sbindir}/fwlw_respond
%{_mandir}/man8/fwlogwatch.8*

