Summary:	PHP binding for libvirt
Summary(pl.UTF-8):	Wiązanie PHP do libvirt
Name:		php-libvirt
Version:	0.4.6
Release:	1
# COPYING contains LGPL v2.1, but README specifies plain GPL
License:	GPL
Group:		Development/Languages/PHP
Source0:	ftp://libvirt.org/libvirt/php/libvirt-php-%{version}.tar.gz
# Source0-md5:	9d69974e29e37284b85440d0903259ec
URL:		http://libvirt.org/php/
BuildRequires:	libvirt-devel >= 0.6.2
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.519
%{?requires_php_extension}
Requires:	libvirt >= 0.6.2
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdocdir		%{_docdir}/phpdoc

%description
Libvirt-php is basically just PHP binding for libvirt virtualization
toolkit.

%description -l pl.UTF-8
Libvirt-php to właściwie zwykłe wiązanie PHP do biblioteki
wirtualizacji libvirt.

%package phpdoc
Summary:	Online manual for php-libvirt binding
Summary(pl.UTF-8):	Dokumentacja online do wiązania php-libvirt
Group:		Documentation
Requires:	php-dirs

%description phpdoc
Documentation for php-libvirt binding.

%description phpdoc -l pl.UTF-8
Dokumentacja do wiązania php-libvirt.

%prep
%setup -q -n libvirt-php-%{version}

%build
%configure \
	--with-html-dir=%{_phpdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PHPCDIR=%{php_sysconfdir}/conf.d

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(755,root,root) %{php_extensiondir}/libvirt-php.so
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d

%files phpdoc
%defattr(644,root,root,755)
%{_phpdocdir}/libvirt-php-%{version}
