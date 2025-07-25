#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	cereal
Summary:	Binary serialization library
Summary(pl.UTF-8):	Biblioteka serializacji binarnej
Name:		ghc-%{pkgname}
Version:	0.5.8.1
Release:	3
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	4f5e41ee3371272daa12a2d073d2fd4f
URL:		http://hackage.haskell.org/package/cereal/
# for ghc < 8.0 also ghc-fail 4.9.x
BuildRequires:	ghc >= 8.0
BuildRequires:	ghc-array
BuildRequires:	ghc-base >= 4.4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.10.4
BuildRequires:	ghc-bytestring < 1
BuildRequires:	ghc-containers
BuildRequires:	ghc-ghc-prim >= 0.2
%if %{with prof}
BuildRequires:	ghc-prof >= 8.0
BuildRequires:	ghc-array-prof
BuildRequires:	ghc-base-prof >= 4.4
BuildRequires:	ghc-bytestring-prof >= 0.10.4
BuildRequires:	ghc-containers-prof
BuildRequires:	ghc-ghc-prim-prof >= 0.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-array
Requires:	ghc-base >= 4.4
Requires:	ghc-bytestring >= 0.10.4
Requires:	ghc-containers
Requires:	ghc-ghc-prim >= 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
A binary serialization library, similar to binary, that introduces an
isolate primitive for parser isolation, and labeled blocks for better
error messages.

%description -l pl.UTF-8
Biblioteka serializacji binarnej, podobna do binary, wprowadzająca
primityw isolate do izolacji parserów oraz etykietowane bloki w celu
lepszych komunikatów błędów.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-array-prof
Requires:	ghc-base-prof >= 4.4
Requires:	ghc-bytestring-prof >= 0.10.4
Requires:	ghc-containers-prof
Requires:	ghc-ghc-prim-prof >= 0.2

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build

runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Serialize
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Serialize/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Serialize/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Serialize/*.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
