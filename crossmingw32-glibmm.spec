Summary:	A C++ interface for glib library - cross MinGW32 version
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki glib - wersja skrośna MinGW32
%define		realname	glibmm
Name:		crossmingw32-%{realname}
Version:	2.28.2
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.28/%{realname}-%{version}.tar.bz2
# Source0-md5:	cf33d1861d09fb2952a6a1d69e0502e3
URL:		http://www.gtkmm.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-glib2 >= 2.28.0
BuildRequires:	crossmingw32-libsigc++ >= 2.2.0
BuildRequires:	libtool >= 2:1.5
BuildRequires:	m4
BuildRequires:	mm-common >= 0.9.5
BuildRequires:	pkgconfig >= 1:0.15
Requires:	crossmingw32-glib2 >= 2.28.0
Requires:	crossmingw32-libsigc++ >= 2.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
A C++ interface for glib library - cross MinGW32 version.

%description -l pl.UTF-8
Interfejs C++ dla biblioteki glib - wersja skrośna MinGW32.

%package static
Summary:	Static glibmm library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka glibmm (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static glibmm library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka glibmm (wersja skrośna MinGW32).

%package dll
Summary:	DLL glibmm library for Windows
Summary(pl.UTF-8):	Biblioteka DLL glibmm dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-glib2-dll >= 2.28.0
Requires:	crossmingw32-libsigc++-dll >= 2.2.0
Requires:	wine

%description dll
DLL glibmm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL glibmm dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-fulldocs \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{doc,devhelp}
# use these from native glibmm if needed
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/glibmm-2.4/proc \
	$RPM_BUILD_ROOT%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/libgiomm-2.4.dll.a
%{_libdir}/libglibmm-2.4.dll.a
%{_libdir}/libglibmm_generate_extra_defs-2.4.dll.a
%{_libdir}/libgiomm-2.4.la
%{_libdir}/libglibmm-2.4.la
%{_libdir}/libglibmm_generate_extra_defs-2.4.la
%dir %{_libdir}/giomm-2.4
%{_libdir}/giomm-2.4/include
%dir %{_libdir}/glibmm-2.4
%{_libdir}/glibmm-2.4/include
%{_includedir}/giomm-2.4
%{_includedir}/glibmm-2.4
%{_pkgconfigdir}/giomm-2.4.pc
%{_pkgconfigdir}/glibmm-2.4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgiomm-2.4.a
%{_libdir}/libglibmm-2.4.a
%{_libdir}/libglibmm_generate_extra_defs-2.4.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libgiomm-2.4-*.dll
%{_dlldir}/libglibmm-2.4-*.dll
%{_dlldir}/libglibmm_generate_extra_defs-2.4-*.dll
