# TODO: separate gltpd to -server package, add init script (requires portmap)
# Conditional build:
%bcond_without	tcl		# disable gui and nviz
%bcond_without	odbc	# disable unixODBC support
#
Summary:	Open Geographic Datastore Interface
Summary(pl):	OGDI - otwarty interfejs do danych geograficznych
Name:		ogdi
Version:	3.1.5
Release:	2
License:	BSD-like
Group:		Applications
Source0:	http://dl.sourceforge.net/ogdi/%{name}-%{version}.tar.gz
# Source0-md5:	9ccf8202b63875a68ded23588bd49544
Source1:	http://ogdi.sourceforge.net/ogdi.pdf
# Source1-md5:	029a8cdcd36bee73df92196ee769040e
Patch0:		%{name}-driversdir.patch
Patch1:		%{name}-pic.patch
URL:		http://ogdi.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	expat-devel
BuildRequires:	proj-devel
%{?with_tcl:uildRequires:	tcl-devel}
%{?with_odbc:BuildRequires:	unixODBC-devel}
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OGDI is the Open Geographic Datastore Interface. OGDI is an
application programming interface (API) that uses a standardized
access methods to work in conjunction with GIS software packages (the
application) and various geospatial data products. OGDI uses a
client/server architecture to facilitate the dissemination of
geospatial data products over any TCP/IP network, and a
driver-oriented approach to facilitate access to several geospatial
data products/formats.

%description -l pl
OGDI (Open Geographic Datastore Interface) oznacza otwarty interfejs
do danych geograficznych. OGDI to API u�ywaj�ce ustandaryzowanych
metod dost�pu do pracy z pakietami oprogramowania GIS i r�nymi danymi
geograficznymi. OGDI u�ywa architektury klient-serwer aby udost�pnia�
dane po dowolnej sieci TCP/IP oraz podej�cia bazuj�cego na
sterownikach aby zapewni� dost�p do r�nych produkt�w/format�w danych
geograficznych.

%package devel
Summary:	OGDI header files and documentation
Summary(pl):	Pliki nag��wkowe i dokumentacja OGDI
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	proj-devel

%description devel
OGDI header files and developer's documentation.

%description devel -l pl
Pliki nag��wkowe i dokumentacja programisty do OGDI.

%package odbc
Summary:	ODBC driver for OGDI
Summary(pl):	Sterownik ODBC do OGDI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description odbc
ODBC driver for OGDI.

%description odbc -l pl
Sterownik ODBC do OGDI.

%package -n tcl-ogdi
Summary:	Tcl wrapper for OGDI
Summary(pl):	Interfejs Tcl do OGDI
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description -n tcl-ogdi
Tcl wrapper for OGDI.

%description -n tcl-ogdi -l pl
Interfejs Tcl do OGDI.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

cp -f %{SOURCE1} .

%build
%{__autoconf}
TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET
%configure \
	--with-expat \
	--with-proj \
	--with-zlib

%{__make} \
	OPTIMIZATION="%{rpmcflags}"

%if %{with tcl}
%{__make} -C ogdi/tcl_interface \
	OPTIMIZATION="%{rpmcflags}" \
	TCL_LINKLIB="-ltcl"
%endif
%{__make} -C contrib/gdal \
	OPTIMIZATION="%{rpmcflags}"
%if %{with odbc}
%{__make} -C ogdi/attr_driver/odbc \
	OPTIMIZATION="%{rpmcflags}" \
	ODBC_LINKLIB="-lodbc"
%endif

%install
rm -rf $RPM_BUILD_ROOT

TOPDIR=`pwd`; TARGET=Linux; export TOPDIR TARGET

%{__make} install \
	INST_INCLUDE=$RPM_BUILD_ROOT%{_includedir} \
	INST_LIB=$RPM_BUILD_ROOT%{_libdir}/ogdi \
	INST_BIN=$RPM_BUILD_ROOT%{_bindir}

%if %{with tcl}
%{__make} install -C ogdi/tcl_interface \
	INST_LIB=$RPM_BUILD_ROOT%{_libdir}
%endif
%{__make} install -C contrib/gdal \
	INST_LIB=$RPM_BUILD_ROOT%{_libdir}/ogdi
%if %{with odbc}
%{__make} install -C ogdi/attr_driver/odbc \
	INST_LIB=$RPM_BUILD_ROOT%{_libdir}/ogdi
%endif

# only libogdi* is common library, the rest are dlopened drivers
mv -f $RPM_BUILD_ROOT%{_libdir}/ogdi/libogdi*.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS
%attr(755,root,root) %{_bindir}/gltpd
%attr(755,root,root) %{_bindir}/ogdi_*
%attr(755,root,root) %{_libdir}/libogdi*.so
%dir %{_libdir}/ogdi
%attr(755,root,root) %{_libdir}/ogdi/lib[^l]*.so

%files devel
%defattr(644,root,root,755)
%doc ogdi.pdf
%{_includedir}/*.h

%if %{with odbc}
%files odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ogdi/liblodbc.so
%endif

%if %{with tcl}
%files -n tcl-ogdi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libecs_tcl.so
%endif
