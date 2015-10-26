# TODO:
# - daemon init script
# - where should arch-dependent .jar be packaged?
# - add -module to plugins build?
#
# Conditional build:
%bcond_without	cim	# CIM plugin (sblim-sfcc based)
%bcond_without	java	# Java bindings
%bcond_without	perl	# Perl bindings
%bcond_without	python	# Python bindings
%bcond_without	ruby	# Ruby bindings

Summary:	Implementation of the Web Services Management specification (WS-Management)
Summary(pl.UTF-8):	Implementacja specyfikacji Web Services Management (WS-Management)
Name:		openwsman
Version:	2.6.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/Openwsman/openwsman/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	221163800046cca5ddb38868d3f82d7e
Patch0:		%{name}-link.patch
Patch1:		%{name}-java.patch
Patch2:		rdoc-rubygems.patch
Patch3:		%{name}-python.patch
URL:		https://github.com/Openwsman
BuildRequires:	cmake >= 2.4
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
%{?with_python:BuildRequires:	python-devel >= 2}
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
%define		skip_post_check_so	.*%{_libdir}/openwsman/.* libwsman_client.so.* libwsman_curl_client_transport.so.* libwsman_server.so.1.0.0 libwsman_clientpp.so.1.0.0

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
Requires:	python-libs

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
%patch3 -p1

%build
install -d build
cd build
%cmake .. \
%if %{with java}
	-DJAVA_INCLUDE_PATH=%{java_home}/include \
%else
	-DBUILD_JAVA=NO \
%endif
	%{!?with_cim:-DBUILD_LIBCIM=NO} \
	%{!?with_perl:-DBUILD_PERL=NO} \
	%{!?with_python:-DBUILD_PYTHON=NO} \
	-DBUILD_RUBY=%{!?with_ruby:NO}%{?with_ruby:YES} \
	-DPACKAGE_ARCHITECTURE=%{_target_cpu} \
	-DPYTHON_EXECUTABLE=%{__python} \
	-DRUBY_HAS_VENDOR_RUBY:BOOL=ON

# ruby .gemspec contains non-ascii characters, build fails with C locale
%{?with_ruby:LC_ALL=en_US} \
%{__make} -j1

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

%files -n python-openwsman
%defattr(644,root,root,755)
%{py_sitedir}/pywsman.py[co]
%attr(755,root,root) %{py_sitedir}/_pywsman.so

%if %{with ruby}
%files -n ruby-openwsman
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/winrs.rb
%{ruby_vendorlibdir}/openwsmanplugin.rb
%{ruby_vendorlibdir}/openwsman.rb
%{ruby_vendorlibdir}/openwsman
%attr(755,root,root) %{ruby_vendorarchdir}/_openwsman.so
%endif
