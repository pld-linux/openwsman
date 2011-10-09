# TODO:
# - daemon init script
# - where should arch-dependent .jar be packaged?
Summary:	Implementation of the Web Services Management specification (WS-Management)
Summary(pl.UTF-8):	Implementacja specyfikacji Web Services Management (WS-Management)
Name:		openwsman
Version:	2.2.6
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://downloads.sourceforge.net/openwsman/%{name}-%{version}.tar.bz2
# Source0-md5:	55b59e467630e00b958a0231942b686f
Patch0:		%{name}-link.patch
Patch1:		%{name}-ruby.patch
Patch2:		%{name}-java.patch
URL:		http://www.openwsman.org/project/openwsman
BuildRequires:	cmake >= 2.4
BuildRequires:	curl-devel >= 7.12.0
BuildRequires:	jdk
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	perl-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.606
BuildRequires:	ruby-devel >= 1.9
BuildRequires:	sblim-sfcc-devel
BuildRequires:	sed >= 4.0
BuildRequires:	swig >= 1.3.30
BuildRequires:	swig-perl >= 1.3.30
BuildRequires:	swig-python >= 1.3.30
BuildRequires:	swig-ruby >= 1.3.30
Requires:	%{name}-libs = %{version}-%{release}
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

%package libs
Summary:	Shared openwsman libraries
Summary(pl.UTF-8):	Biblioteki współdzielone openwsman
Group:		Libraries
Conflicts:	openwsman < 2.2.6

%description libs
Shared openwsman libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone openwsman.

%package devel
Summary:	Header files for openwsman
Summary(pl.UTF-8):	Pliki nagłówkowe openwsman
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	openwsman-static

%description devel
Header files for openwsman.

%description devel -l pl.UTF-8
Pliki nagłówkowe openwsman.

%package -n java-openwsman
Summary:	Java bindings for openwsman libraries
Summary(pl.UTF-8):	Wiązania Javy do bibliotek openwsman
Group:		Libraries/Java
Requires:	%{name}-libs = %{version}-%{release}
Requires:	jre

%description -n java-openwsman
Java bindings for openwsman libraries.

%description -n java-openwsman -l pl.UTF-8
Wiązania Javy do bibliotek openwsman.

%package -n perl-openwsman
Summary:	Perl bindings for openwsman libraries
Summary(pl.UTF-8):	Wiązania Perla do bibliotek openwsman
Group:		Development/Languages/Perl
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-openwsman
Perl bindings for openwsman libraries.

%description -n perl-openwsman -l pl.UTF-8
Wiązania Perla do bibliotek openwsman.

%package -n python-openwsman
Summary:	Python bindings for openwsman libraries
Summary(pl.UTF-8):	Wiązania Pythona do bibliotek openwsman
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-openwsman
Python bindings for openwsman libraries.

%description -n python-openwsman -l pl.UTF-8
Wiązania Pythona do bibliotek openwsman.

%package -n ruby-openwsman
Summary:	Ruby bindings for openwsman libraries
Summary(pl.UTF-8):	Wiązania języka Ruby do bibliotek openwsman
Group:		Development/Languages
Requires:	%{name}-libs = %{version}-%{release}
Requires:	ruby

%description -n ruby-openwsman
Ruby bindings for openwsman libraries.

%description -n ruby-openwsman -l pl.UTF-8
Wiązania języka Ruby do bibliotek openwsman.

%prep
%setup -q
%undos src/cpp/CMakeLists.txt
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e 's,rubyio\.h,ruby/io.h,' \
	bindings/openwsman.i \
	src/plugins/swig/plugin.i

%build
install -d build
cd build
%cmake .. \
	-DPACKAGE_ARCHITECTURE=%{_target_cpu} \
	-DJAVA_INCLUDE_PATH=%{java_home}/include

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/openwsman/subscriptions

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/openwsmand
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

%files libs
%defattr(644,root,root,755)
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

%files -n java-openwsman
%defattr(644,root,root,755)
%{_javadir}/openwsman-%{_target_cpu}-%{version}.jar

%files -n perl-openwsman
%defattr(644,root,root,755)
%attr(755,root,root) %{perl_vendorarch}/openwsman.so
%{perl_vendorlib}/openwsman.pm

%files -n python-openwsman
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_pywsman.so
%{py_sitedir}/pywsman.py[co]

%files -n ruby-openwsman
%defattr(644,root,root,755)
%attr(755,root,root) %{ruby_sitearchdir}/openwsman.so
%{ruby_sitelibdir}/openwsmanplugin.rb
%{ruby_sitelibdir}/openwsman
