#
Summary:	A C++ interface for glib library - cross Mingw32 version
Summary(pl.UTF-8):	Interfejs C++ dla biblioteki glib - wersja skrośna Mingw32
%define		_realname	glibmm
Name:		crossmingw32-%{_realname}
Version:	2.12.5
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.12/%{_realname}-%{version}.tar.bz2
# Source0-md5:	309fab274ada3d62aa4506fb6f5685e2
URL:		http://gtkmm.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	crossmingw32-glib2 >= 2.12.9
BuildRequires:	crossmingw32-libsigc++ >= 2.0.17
BuildRequires:	crossmingw32-pkgconfig
#BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.4d
BuildRequires:	perl-XML-Parser
Requires:	crossmingw32-glib2 >= 2.12.9
Requires:	crossmingw32-libsigc++ >= 2.0.17
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		_sysprefix		/usr
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_prefix			%{_sysprefix}/%{target}
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
A C++ interface for glib library - cross Mingw32 version.

%description -l pl.UTF-8
Interfejs C++ dla biblioteki glib - wersja skrośna Mingw32.

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CHANGES NEWS README
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_bindir}/*.dll
%dir %{_libdir}/%{_realname}-2.4
%{_libdir}/%{_realname}-2.4/include
%dir %{_libdir}/%{_realname}-2.4/proc
%{_libdir}/%{_realname}-2.4/proc/m4
%{_libdir}/%{_realname}-2.4/proc/pm
%attr(755,root,root) %{_libdir}/%{_realname}-2.4/proc/gmmproc
%attr(755,root,root) %{_libdir}/%{_realname}-2.4/proc/*.pl
%{_includedir}/%{_realname}-2.4
