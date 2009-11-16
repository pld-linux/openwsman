# TODO:
# - libs subpackage
# - daemon init script
#
Summary:	Implementation of the Web Services Management specification (WS-Management)
Name:		openwsman
Version:	2.1.0
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/openwsman/%{name}-%{version}.tar.bz2
# Source0-md5:	25a135bea7c1653f66b2428c4b252d3a
URL:		http://www.openwsman.org/project/openwsman
BuildRequires:	curl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Openwsman is a project intended to provide an open-source
implementation of the Web Services Management specification
(WS-Management) and to expose system management information on the
Linux operating system using the WS-Management protocol. WS-Management
is based on a suite of web services specifications and usage
requirements that exposes a set of operations focused on and covers
all system management aspects.

%package devel
Summary:	Header files and develpment documentation for openwsman
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and openwsman documentation.

%package static
Summary:	Static openwsman library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static openwsman libraries.

%prep
%setup -q

sed -i -e 's#-Werror##g' configure* *.m4

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/openwsmand
%attr(755,root,root) %{_libdir}/*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/*.so.0
%attr(755,root,root) %ghost %{_libdir}/*.so.1
%dir %{_libdir}/openwsman
%dir %{_libdir}/openwsman/authenticators
%attr(755,root,root) %{_libdir}/openwsman/authenticators/*.so*
%{_libdir}/openwsman/authenticators/*.la
%dir %{_libdir}/openwsman/plugins
%attr(755,root,root) %{_libdir}/openwsman/plugins/*.so*
%{_libdir}/openwsman/plugins/*.la
%{_sysconfdir}/openwsman
/var/lib/openwsman

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_includedir}/openwsman
%{_libdir}/*.la
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
