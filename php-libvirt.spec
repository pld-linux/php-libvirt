#
# Conditional build:
%bcond_without	phpdoc		# package phpdoc

# don't build for php53
%if 0%{?_pld_builder:1} && "%{?php_suffix}" != "55"
%undefine	with_phpdoc
%endif

%define		php_name	php%{?php_suffix}
%define		modname		libvirt
Summary:	PHP binding for libvirt
Summary(pl.UTF-8):	Wiązanie PHP do libvirt
Name:		%{php_name}-%{modname}
Version:	0.5.5
Release:	1
License:	LGPL v2.1
Group:		Development/Languages/PHP
Source0:	https://libvirt.org/sources/php/libvirt-php-%{version}.tar.gz
# Source0-md5:	28fb7e2e216805e5aa5d5744fb3fd303
URL:		https://libvirt.org/php/
BuildRequires:	%{php_name}-devel
BuildRequires:	%{php_name}-pecl-imagick
# libvirt, libvirt-qemu
BuildRequires:	libvirt-devel >= 1.2.13
BuildRequires:	libxml2-devel >= 2.0.0
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Requires:	libvirt >= 1.2.13
Provides:	php(%{modname}) = %{version}
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
	--disable-silent-rules \
	--with-html-dir=%{_phpdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	PHPCDIR=%{php_sysconfdir}/conf.d \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{php_extensiondir}/*.la

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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/libvirt-php.ini

%if %{with phpdoc}
%files phpdoc
%defattr(644,root,root,755)
%{_phpdocdir}/libvirt-php-%{version}
%endif
