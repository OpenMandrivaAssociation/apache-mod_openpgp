#Module-Specific definitions
%define mod_name mod_openpgp
%define mod_conf A97_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A Apache module that implements PGP access authorization
Name:		apache-%{mod_name}
Version:	0.5.0
Release:	%mkrel 6
Group:		System/Servers
License:	Apache License
URL:		https://wiki.buanzo.org/
Source0:	http://www.buanzo.com.ar/files/%{mod_name}-%{version}.tgz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	libgpgme-devel
BuildRequires:	libgpg-error-devel
Obsoletes:	apache-mod_auth_openpgp
Provides:	apache-mod_auth_openpgp = %{version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mod_OpenPGP is an Apache module that implements access authorization to
servers, vhosts, or directories when incoming requests' HTTP OpenPGP signatures
are valid and known by the local keyring. It's the Apache companion for
Firefox's extension "Enigform".

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c `apr-1-config --cppflags` -D_FILE_OFFSET_BITS=64 -lgpgme -lgpg-error -I%{_includedir}/gpgme mod_openpgp.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
