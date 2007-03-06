Summary:	A C++ interface for glib library - cross Mingw32 version
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki glib - wersja skrośna Mingw32
%define		_realname	glibmm
Name:		crossmingw32-%{_realname}
Version:	2.12.7
Release:	1
License:	LGPL
Group:		Development/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.12/%{_realname}-%{version}.tar.bz2
# Source0-md5:	fd2338d504b852ba5ddaf3e1491715cd
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-glib2 >= 2.12.9
BuildRequires:	crossmingw32-libsigc++ >= 2.0.17
BuildRequires:	pkgconfig
BuildRequires:	libtool >= 2:1.5
BuildRequires:	perl-XML-Parser
Requires:	crossmingw32-glib2 >= 2.12.9
Requires:	crossmingw32-libsigc++ >= 2.0.17
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
A C++ interface for glib library - cross Mingw32 version.

%description -l pl.UTF-8
Interfejs C++ dla biblioteki glib - wersja skrośna Mingw32.

%package static
Summary:	Static glibmm library (cross mingw32 version)
Summary(pl.UTF-8):	Statyczna biblioteka glibmm (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static glibmm library (cross mingw32 version).

%description static -l pl.UTF-8
Statyczna biblioteka glibmm (wersja skrośna mingw32).

%package dll
Summary:	DLL glibmm library for Windows
Summary(pl.UTF-8):	Biblioteka DLL glibmm dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-glib2-dll >= 2.12.9
Requires:	crossmingw32-libsigc++-dll >= 2.0.17
Requires:	wine

%description dll
DLL glibmm library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL glibmm dla Windows.

%prep
%setup -q -n %{_realname}-%{version}

%build
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig
%{__libtoolize}
%{__aclocal} -I scripts
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

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
# use these from native glibmm if needed
rm -rf $RPM_BUILD_ROOT%{_libdir}/glibmm-2.4/proc
rm -rf $RPM_BUILD_ROOT%{_datadir}/aclocal

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CHANGES NEWS README
%{_libdir}/libglibmm-2.4.dll.a
%{_libdir}/libglibmm_generate_extra_defs-2.4.dll.a
%{_libdir}/libglibmm-2.4.la
%{_libdir}/libglibmm_generate_extra_defs-2.4.la
%dir %{_libdir}/%{_realname}-2.4
%{_libdir}/%{_realname}-2.4/include
%{_includedir}/%{_realname}-2.4
%{_pkgconfigdir}/glibmm-2.4.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libglibmm-2.4.a
%{_libdir}/libglibmm_generate_extra_defs-2.4.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libglibmm-2.4-*.dll
%{_dlldir}/libglibmm_generate_extra_defs-2.4-*.dll
