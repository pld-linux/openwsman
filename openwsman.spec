# TODO:
# - libs subpackage
# - daemon init script
#
Summary:	Implementation of the Web Services Management specification (WS-Management)
Summary(pl.UTF-8):	Implementacja specyfikacji Web Services Management (WS-Management)
Name:		openwsman
Version:	2.1.0
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/openwsman/%{name}-%{version}.tar.bz2
# Source0-md5:	25a135bea7c1653f66b2428c4b252d3a
URL:		http://www.openwsman.org/project/openwsman
BuildRequires:	curl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Openwsman is a project intended to provide an open-source
implementation of the Web Services Management specification
(WS-Management) and to expose system management information on the
Linux operating system using the WS-Management protocol. WS-Management
is based on a suite of web services specifications and usage
requirements that exposes a set of operations focused on and covers
all system management aspects.

%description -l pl.UTF-8
Openwsman to projekt, którego celem jest zapewnienie mającej otwarte
źródła implementacji specyfikacji Web Services Management
(WS-Management) i udostępnienie informacji związanych z zarządzaniem
systemem pod Linuksem poprzez protokół WS-Management. WS-Management
jest oparty na zbiorze specyfikacji i wymaganiach usług WWW,
udostępniających zbiór operacji pokrywających wszystkie aspekty
zarządzania systemem.

%package devel
Summary:	Header files for openwsman
Summary(pl.UTF-8):	Pliki nagłówkowe openwsman
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for openwsman.

%description devel -l pl.UTF-8
Pliki nagłówkowe openwsman.

%package static
Summary:	Static openwsman libraries
Summary(pl.UTF-8):	Statyczne biblioteki openwsman
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static openwsman libraries.

%description static -l pl.UTF-8
Statyczne biblioteki openwsman.

%prep
%setup -q

%{__sed} -i -e 's#-Werror##g' configure* *.m4

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
