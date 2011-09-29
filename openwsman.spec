# TODO:
# - libs subpackage
# - daemon init script
# - package perl and python
# - fix and package java and ruby
#
Summary:	Implementation of the Web Services Management specification (WS-Management)
Summary(pl.UTF-8):	Implementacja specyfikacji Web Services Management (WS-Management)
Name:		openwsman
Version:	2.2.6
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/openwsman/%{name}-%{version}.tar.bz2
# Source0-md5:	55b59e467630e00b958a0231942b686f
Patch0:		%{name}-link.patch
URL:		http://www.openwsman.org/project/openwsman
BuildRequires:	cmake >= 2.4
BuildRequires:	curl-devel >= 7.12.0
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sblim-sfcc-devel
BuildRequires:	sed >= 4.0
BuildRequires:	swig >= 1.3.30
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# plugins use symbols from libraries, client libs have circular dependencies with libwsman
%define		skip_post_check_so	.*%{_libdir}/openwsman/.* libwsman_client.so.* libwsman_curl_client_transport.so.*

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
Obsoletes:	openwsman-static

%description devel
Header files for openwsman.

%description devel -l pl.UTF-8
Pliki nagłówkowe openwsman.

%prep
%setup -q
%undos src/cpp/CMakeLists.txt
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DPACKAGE_ARCHITECTURE=%{_target_cpu} \
	-DBUILD_JAVA=NO \
	-DBUILD_RUBY=NO

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/openwsman/subscriptions

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/openwsmand
%attr(755,root,root) %{_libdir}/libwsman.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwsman.so.1
%attr(755,root,root) %{_libdir}/libwsman_client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwsman_client.so.1
%attr(755,root,root) %{_libdir}/libwsman_clientpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwsman_clientpp.so.1
%attr(755,root,root) %{_libdir}/libwsman_curl_client_transport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwsman_curl_client_transport.so.1
%attr(755,root,root) %{_libdir}/libwsman_server.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwsman_server.so.1
%dir %{_libdir}/openwsman
%dir %{_libdir}/openwsman/authenticators
%attr(755,root,root) %{_libdir}/openwsman/authenticators/libwsman_*.so*
%dir %{_libdir}/openwsman/plugins
%attr(755,root,root) %{_libdir}/openwsman/plugins/libwsman_*.so*
%dir %{_sysconfdir}/openwsman
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openwsman/openwsman.conf
%attr(754,root,root) %{_sysconfdir}/openwsman/owsmangencert.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openwsman/ssleay.cnf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/openwsman
/var/lib/openwsman

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwsman.so
%attr(755,root,root) %{_libdir}/libwsman_client.so
%attr(755,root,root) %{_libdir}/libwsman_clientpp.so
%attr(755,root,root) %{_libdir}/libwsman_curl_client_transport.so
%attr(755,root,root) %{_libdir}/libwsman_server.so
%{_includedir}/openwsman
%{_pkgconfigdir}/openwsman.pc
%{_pkgconfigdir}/openwsman++.pc
%{_pkgconfigdir}/openwsman-server.pc
