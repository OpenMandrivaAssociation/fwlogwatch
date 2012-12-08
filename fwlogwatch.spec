Summary:	Firewall log analyzer, report generator and realtime response agent
Name:		fwlogwatch
Version:	1.2
Release:	%mkrel 5
Group:		Monitoring
License:	GPL
URL:		http://fwlogwatch.inside-security.de/
Source0:	%{name}-%{version}.tar.bz2
Source1:	fwlogwatch.init
Source2:	fwlogwatch.sysconfig
Patch0:		fwlogwatch-mdv_conf.diff
BuildRequires:	adns-devel
BuildRequires:	flex
BuildRequires:	gettext
BuildRequires:	zlib-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

cp %{SOURCE1} fwlogwatch.init
cp %{SOURCE2} fwlogwatch.sysconfig

chmod 644 contrib/fwlogsummary.cgi contrib/fwlogsummary_small.cgi

# fix encoding
perl -pi -e "s|iso-8859-1|UTF-8|g" *.c

%build
%serverbuild

%make CFLAGS="$CFLAGS -DHAVE_ZLIB -DHAVE_GETTEXT -DHAVE_IPV6 -DHAVE_ADNS" LIBS="-L%{_libdir} -lcrypt -lz -ladns"

# fix encoding
pushd po

for i in de pt sv; do
    perl -pi -e "s|ISO-8859-1|UTF-8|g" $i.po
    iconv --from-code=ISO-8859-1 --to-code=UTF-8 $i.po > $i.po.new; mv $i.po.new $i.po
done

for i in de ja pt sv zh_CN zh_TW; do
    msgfmt -v -o $i.mo $i.po
done

popd

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
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


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2-2mdv2011.0
+ Revision: 664398
- mass rebuild

* Thu Nov 11 2010 Lonyai Gergely <aleph@mandriva.org> 1.2-1mdv2011.0
+ Revision: 595935
- 1.2
  Rediffed: fwlogwatch-mdv_conf.diff

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-9mdv2010.1
+ Revision: 520111
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.1-8mdv2010.0
+ Revision: 424507
- rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.1-7mdv2009.0
+ Revision: 264521
- rebuild early 2009.0 package (before pixel changes)

* Mon May 12 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-6mdv2009.0
+ Revision: 206190
- major rework, fixes a bug reported on the cooker ml (Maxim Heijndijk)
- rediffed the path patch (now fwlogwatch-mdv_conf.diff)
- enable ipv6 and adns

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-5mdv2008.1
+ Revision: 178847
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Jun 28 2007 Adam Williamson <awilliamson@mandriva.org> 1.1-3mdv2008.0
+ Revision: 45372
- rebuild for 2008
- Import fwlogwatch



* Thu Aug 10 2006 Lenny Cartier <lenny@mandriva.com> 1.1-2mdv2007.0
- rebuild

* Thu May 04 2006 Jerome Soyer <saispo@mandriva.org> 1.1-1mdk
- New release 1.1

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.0-2mdk
- Rebuild

* Wed May 11 2005 Lenny Cartier <lenny@mandriva.com> 1.0-1mdk
- 1.0
- regenerated P0

* Thu Jan 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.9.3-1mdk
- 0.9.3
- regenerated P0
- cosmetics

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.9-2mdk
- rebuild
- use %%make macro
- use %%makeinstall_std macro
- quiet setup

* Mon Feb 03 2003 Florin <florin@mandrakesoft.com> 0.9-1mdk
- 0.9

* Tue Jun 18 2002 Stefan van der Eijk <stefan@eijk.nu> 0.6-3mdk
- fix initscript (thanks to Andre DUCLOS)

* Sat Jun  8 2002 Stefan van der Eijk <stefan@eijk.nu> 0.6-2mdk
- BuildRequires
- add %%_post_service and %%_preun_service (rpmlint)
- %%{_initrddir}/fwlogwatch --> %%config %%{_initrddir}/fwlogwatch (rpmlint)

* Thu Feb 28 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.6-1mdk
- 0.6
- regenerate patch

* Thu Jan 31 2002 Philippe Libat <philippe@mandrakesoft.com> 0.5.2-1mdk
- new version

* Tue Sep 11 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.4-1mdk
- added by Oden Eriksson <oden.eriksson@kvikkjokk.net> :
	- initial MDK contrib package
	- added patch 1
