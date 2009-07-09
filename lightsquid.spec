#===== Generic Info ======
%define apache_home %{_var}/www/html
%define apache_confdir %{_sysconfdir}/httpd/conf.d
%define lightsquid_confdir %{_sysconfdir}/lightsquid
%define lightdir %{apache_home}/lightsquid
%define srcname lightsquid-%{version}

Summary: Lite, small size and fast log analizer for squid proxy
Name: lightsquid
Version: 1.8
Release: 1%{?dist}
License: GPLv2
Group: Applications/Internet
Url: http://lightsquid.sourceforge.net/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Source: http://prdownloads.sourceforge.net/lightsquid/%name-%version.tgz

Requires: perl-GDGraph3d perl-GD perl-GDGraph
BuildRequires: sed
BuildArch: noarch

%description
%{name} report parser and visualyzer, generate sort of report
light fast no database required no additional perl modules
small disk usage template html - you can create you own look;

%prep
%setup -q -n %{srcname}

%{__sed} -i 's|/var/www/html/lightsquid/lang|%{_datadir}/%{name}/lang|' lightsquid.cfg
%{__sed} -i 's|/var/www/html/lightsquid/tpl|%{_datadir}/%{name}/tpl|' lightsquid.cfg
%{__sed} -i 's|/var/www/html/lightsquid/ip2name|%{_datadir}/%{name}/ip2name|' lightsquid.cfg
%{__sed} -i 's|\$cfgpath             =\"/var/www/html/lightsquid|\$cfgpath             =\"%lightsquid_confdir|' lightsquid.cfg
%{__sed} -i 's|require "ip2name|require "$ip2namepath|' lightparser.pl
%{__sed} -i 's|lightsquid.cfg|%lightsquid_confdir/lightsquid.cfg|' *.cgi *.pl
%{__sed} -i 's|common.pl|%_datadir/%name/common.pl|' *.cgi *.pl
%{__sed} -i 's|/etc/squid/users.txt|/etc/lightsquid/users.txt|' ip2name/ip2name.*

iconv -f WINDOWS-1251 -t UTF8 lang/ru.lng > lang/ru-utf8.lng
%{__sed} -i 's|windows-1251|utf8|' lang/ru-utf8.lng
	
%install
install -m 755 -d %{buildroot}{%{_sbindir},%{lightdir}}
install -m 755 -d %{buildroot}%{_sysconfdir}/cron.d
install -m 755 -d %{buildroot}%{_datadir}/%name/{lang,ip2name,tpl}
install -m 755 -d %{buildroot}%{_localstatedir}/%{name}
install -m 755 lightparser.pl %{buildroot}%{_sbindir}/
install -pD -m 644 lightsquid.cfg %{buildroot}%{lightsquid_confdir}/lightsquid.cfg
install -pD -m 644 group.cfg.src %{buildroot}%{lightsquid_confdir}/group.cfg
install -pD -m 644 realname.cfg %{buildroot}%{lightsquid_confdir}/realname.cfg
#install -pD -m 644 lightsquid.conf %{buildroot}%{apache_confdir}/lightsquid.conf

%__cat << EOF > %{buildroot}%{_sysconfdir}/cron.d/lightsquid
55 * * * *     lightsquid /usr/sbin/lightparser.pl today
EOF

# install lib
install -p -m 755 {common.pl,check-setup.pl} %{buildroot}%{_datadir}/%{name}/
install -p -m 644 tools/fixreport.pl %{buildroot}%{_datadir}/%{name}/
install -p -m 644 lang/check_tpl_lng.pl %{buildroot}%{_datadir}/%{name}/
install -p -m 755 lang/check_lng.pl %{buildroot}%{_datadir}/%{name}/
install -p -m 644 lang/*.lng %{buildroot}%{_datadir}/%{name}/lang/
install -p -m 644 ip2name/* %{buildroot}%{_datadir}/%{name}/ip2name/
%__cp -aRf tpl/* %{buildroot}%{_datadir}/%{name}/tpl/

%__install -p -m 755 [^A-Z]*.cgi %{buildroot}%{apache_home}/%{name}/

%files
%doc doc/*
%_sbindir/*
%_datadir/%name
%config(noreplace) %{lightsquid_confdir}/lightsquid.cfg
%config(noreplace) %{lightsquid_confdir}/group.cfg
%config(noreplace) %{lightsquid_confdir}/realname.cfg
%config(noreplace) %{_sysconfdir}/cron.d/lightsquid
#%attr(0755,root,root)
%{lightdir}/*.cgi
%config(noreplace) %{apache_confdir}/lightsquid.conf

%pre
/usr/sbin/groupadd -r -f %name 
#/usr/sbin/useradd -r -g %name -G squid -d %{_localstatedir}/%{name} -c 'Log parser lightsquid' -s /bin/false -n %name

#%post
#if [[ -d %{lightdir}/report ]]; then
 #  %{mv} %{lightdir}/report/* %{_localstatedir}/%{name}
 # echo "Reports move from %lightdir/report to %_localstatedir/%name"
#fi
#find %_localstatedir/%name -print0 | xargs -r0 chown %name:%name

%clean
%{__rm} -rf %{buildroot}

%changelog
* Thu Jul 9 2009 Popkov Aleksey <aleksey@psniip.ru> 1.8-1
- Build version of lightsquid 1.8.

* Wed Jun 17 2009 Popkov Aleksey <aleksey@psniip.ru> 1.7.1-1
- Some removed sed's and added BuildRoot directive.

* Tue Jun 16 2009 Popkov Aleksey <aleksey@psniip.ru> 1.7.1-1
- Adapted for Fedora Group
