# TODO:
# - daemon init script
# - where should arch-dependent .jar be packaged?
# - add -module to plugins build?
#
# Conditional build:
%bcond_without	cim	# CIM plugin (sblim-sfcc based)
%bcond_without	java	# Java bindings
%bcond_without	perl	# Perl bindings
%bcond_without	python	# Python bindings (any)
%bcond_without	python2	# Python 2.x bindings
%bcond_without	python3	# Python 3.x bindings
%bcond_without	ruby	# Ruby bindings

%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif
Summary:	Implementation of the Web Services Management specification (WS-Management)
Summary(pl.UTF-8):	Implementacja specyfikacji Web Services Management (WS-Management)
Name:		openwsman
Version:	2.6.9
Release:	3
License:	BSD
Group:		Libraries
Source0:	https://github.com/Openwsman/openwsman/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	82f0cdab1ccbad847e994ed6f4c19b01
Patch0:		rdoc-rubygems.patch
Patch1:		%{name}-python.patch
URL:		https://github.com/Openwsman
BuildRequires:	cmake >= 2.6
BuildRequires:	curl-devel >= 7.12.0
%if %{with ruby}
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%endif
BuildRequires:	jdk
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
%{?with_perl:BuildRequires:	perl-devel}
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 2}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpmbuild(macros) >= 1.606
%{?with_ruby:BuildRequires:	ruby-devel >= 1.9}
%{?with_cim:BuildRequires:	sblim-sfcc-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	swig >= 2.0.5
%{?with_perl:BuildRequires:	swig-perl >= 2.0.5}
%{?with_python:BuildRequires:	swig-python >= 2.0.5}
%{?with_ruby:BuildRequires:	swig-ruby >= 2.0.5}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# plugins use symbols from libraries, client libs have circular dependencies with libwsman
%define		skip_post_check_so	.*%{_libdir}/openwsman/.* libwsman_client.so.* libwsman_curl_client_transport.so.* libwsman_server.so.1.0.0 libwsman_clientpp.so.1.0.0 libwsman.so.1.0.0

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
Summary:	Python 2 bindings for openwsman libraries
Summary(pl.UTF-8):	Wiązania Pythona 2 do bibliotek openwsman
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-libs

%description -n python-openwsman
Python 2 bindings for openwsman libraries.

%description -n python-openwsman -l pl.UTF-8
Wiązania Pythona 2 do bibliotek openwsman.

%package -n python3-openwsman
Summary:	Python 3 bindings for openwsman libraries
Summary(pl.UTF-8):	Wiązania Pythona 3 do bibliotek openwsman
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python3-libs >= 1:3.2

%description -n python3-openwsman
Python 3 bindings for openwsman libraries.

%description -n python3-openwsman -l pl.UTF-8
Wiązania Pythona 3 do bibliotek openwsman.

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

%build
install -d build
cd build
%cmake .. \
%if %{with java}
	-DJAVA_INCLUDE_PATH=%{java_home}/include \
%else
	-DBUILD_JAVA=OFF \
%endif
	%{!?with_cim:-DBUILD_LIBCIM=OFF} \
	%{!?with_perl:-DBUILD_PERL=OFF} \
	%{!?with_python2:-DBUILD_PYTHON=OFF} \
	-DBUILD_PYTHON3=OFF \
	-DBUILD_RUBY=%{!?with_ruby:OFF}%{?with_ruby:ON} \
	-DPACKAGE_ARCHITECTURE=%{_target_cpu} \
	%{?with_python2:-DPYTHON_EXECUTABLE=%{__python}} \
	-DRUBY_HAS_VENDOR_RUBY:BOOL=ON

# ruby .gemspec contains non-ascii characters, build fails with C locale
%{?with_ruby:LC_ALL=en_US} \
%{__make} -j1

cd ..

%if %{with python3}
install -d build-python3
cd build-python3
%cmake .. \
	-DBUILD_JAVA=OFF \
	%{!?with_cim:-DBUILD_LIBCIM=ON} \
	-DBUILD_PERL=OFF \
	-DBUILD_PYTHON=OFF \
	-DBUILD_PYTHON3=ON \
	-DBUILD_RUBY=OFF \
	-DPACKAGE_ARCHITECTURE=%{_target_cpu} \
	-DPYTHON_EXECUTABLE=%{__python3}

%{__make} -j1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/openwsman/subscriptions

%if %{with python3}
%{__make} -C build-python3 install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md TODO
%attr(755,root,root) %{_sbindir}/openwsmand
%dir %{_libdir}/openwsman
%dir %{_libdir}/openwsman/authenticators
%attr(755,root,root) %{_libdir}/openwsman/authenticators/libwsman_*.so*
%dir %{_libdir}/openwsman/plugins
%attr(755,root,root) %{_libdir}/openwsman/plugins/libwsman_*.so*
%attr(755,root,root) %{_libdir}/openwsman/plugins/libredirect.so*
%dir %{_sysconfdir}/openwsman
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openwsman/openwsman.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openwsman/openwsman_client.conf
%attr(754,root,root) %{_sysconfdir}/openwsman/owsmangencert.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openwsman/ssleay.cnf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/openwsman
%dir /var/lib/openwsman
%dir /var/lib/openwsman/subscriptions

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwsman.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwsman.so.1
%attr(755,root,root) %{_libdir}/libwsman_client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libwsman_client.so.4
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

%if %{with java}
%files -n java-openwsman
%defattr(644,root,root,755)
%{_javadir}/openwsman-%{_target_cpu}-%{version}.jar
%endif

%files -n perl-openwsman
%defattr(644,root,root,755)
%{perl_vendorlib}/openwsman.pm
%attr(755,root,root) %{perl_vendorarch}/openwsman.so

%if %{with python2}
%files -n python-openwsman
%defattr(644,root,root,755)
%{py_sitedir}/pywsman.py[co]
%attr(755,root,root) %{py_sitedir}/_pywsman.so
%endif

%if %{with python3}
%files -n python3-openwsman
%defattr(644,root,root,755)
%{py3_sitedir}/pywsman.py
%{py3_sitedir}/__pycache__/pywsman.cpython-*.py[co]
%attr(755,root,root) %{py3_sitedir}/_pywsman.so
%endif

%if %{with ruby}
%files -n ruby-openwsman
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/winrs
%{ruby_vendorlibdir}/openwsmanplugin.rb
%{ruby_vendorlibdir}/openwsman.rb
%{ruby_vendorlibdir}/openwsman
%attr(755,root,root) %{ruby_vendorarchdir}/_openwsman.so
%endif
