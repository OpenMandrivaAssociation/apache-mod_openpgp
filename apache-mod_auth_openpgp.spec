#Module-Specific definitions
%define mod_name mod_auth_openpgp
%define mod_conf A97_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A Apache module that implements PGP access authorization
Name:		apache-%{mod_name}
Version:	0.2.1
Release:	%mkrel 5
Group:		System/Servers
License:	Apache License
URL:		http://linux-consulting.buanzo.com.ar/2007/04/modauthopenpgp-020-released.html
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
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mod_Auth_OpenPGP is an Apache module that implements access authorization to
servers, vhosts, or directories when incoming requests' HTTP OpenPGP signatures
are valid and known by the local keyring. It's the Apache companion for
Firefox's extension "Enigform".

%prep

%setup -q -n auth_openpgp

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c -lgpgme -lgpg-error -I%{_includedir}/gpgme mod_auth_openpgp.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
