Summary:	A C++ interface for glib library - cross MinGW32 version
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki glib - wersja skrośna MinGW32
%define		realname	glibmm
Name:		crossmingw32-%{realname}
Version:	2.66.7
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	https://download.gnome.org/sources/glibmm/2.66/%{realname}-%{version}.tar.xz
# Source0-md5:	c6edf4cc986adec2a6d21e7423bad7d1
Patch0:		glibmm-mingw32.patch
URL:		https://www.gtkmm.org/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	crossmingw32-gcc-c++ >= 1:4.7
BuildRequires:	crossmingw32-glib2 >= 2.62.0
BuildRequires:	crossmingw32-libsigc++ >= 2.10.0
BuildRequires:	crossmingw32-std-threads
BuildRequires:	libtool >= 2:2.0
BuildRequires:	m4
BuildRequires:	mm-common >= 0.9.10
BuildRequires:	perl-XML-Parser
BuildRequires:	perl-base
BuildRequires:	pkgconfig >= 1:0.15
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	crossmingw32-gcc-c++ >= 1:4.7
Requires:	crossmingw32-glib2 >= 2.62.0
Requires:	crossmingw32-libsigc++ >= 2.10.0
Requires:	crossmingw32-std-threads
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
# now at least i486 is required for atomic operations
%define		optflags	-O2 -march=i486
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*
%define		filterout_cxx	-f[-a-z0-9=]*

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
Requires:	crossmingw32-glib2-dll >= 2.62.0
Requires:	crossmingw32-libsigc++-dll >= 2.10.0
Requires:	wine

%description dll
DLL glibmm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL glibmm dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch -P0 -p1

%build
export PKG_CONFIG_LIBDIR=%{_prefix}/lib/pkgconfig
mm-common-prepare --copy --force
%{__libtoolize}
%{__aclocal} -I build
%{__autoconf}
%{__autoheader}
%{__automake}
# std-threads require at least WinXP API
CPPFLAGS="%{rpmcppflags} -DWINVER=0x0501"
# mingw32 requires gnu++11 (instead of c++11) for off[64]_t
CXXFLAGS="%{rpmcxxflags} -std=gnu++11"
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-documentation \
	--enable-maintainer-mode \
	--disable-silent-rules \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

# use these from native glibmm if needed
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/glibmm-2.4/proc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README.md
%{_libdir}/libgiomm-2.4.dll.a
%{_libdir}/libglibmm-2.4.dll.a
%{_libdir}/libglibmm_generate_extra_defs-2.4.dll.a
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
%{_dlldir}/libgiomm-2.4-1.dll
%{_dlldir}/libglibmm-2.4-1.dll
%{_dlldir}/libglibmm_generate_extra_defs-2.4-1.dll
