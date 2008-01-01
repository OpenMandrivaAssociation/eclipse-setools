%define gcj_support 1

Exclusiveos:linux

%define require_setools_major_ver	3.3
%define require_setools_fix_ver		.2
#BuildRequires: perl(XML::XPath)
BuildRequires: eclipse-pde
BuildRequires: ant >= 0:1.6
BuildRequires: java-rpmbuild >= 0:1.5
%if %{gcj_support}
BuildRequires: java-gcj-compat-devel
%endif
BuildRequires: setools-libs-java >= %{require_setools_major_ver}%{require_setools_fix_ver}

%define eclipse_name		eclipse
%define eclipse_base		%{_datadir}/%{eclipse_name}
%define eclipse_lib_base	%{_libdir}/%{eclipse_name}
%define svnbase			http://oss.tresys.com/repos/slide/trunk/

Summary: Eclipse plugin wrapper for SETools Java policy analysis tools for SELinux
Name: eclipse-setools
Group: Development/Java
License: LGPLv2+
URL: http://oss.tresys.com/projects/setools
Version: 3.3.2.3

# mkdir eclipse-setools
# cd eclipse-setools
# svn export http://oss.tresys.com/repos/slide/trunk/setools-plugin setools-plugin
# svn export http://oss.tresys.com/repos/slide/trunk/setools-feature setools-feature
# svn export http://oss.tresys.com/repos/slide/trunk/setools.linux.x86 setools.linux.x86
# svn export http://oss.tresys.com/repos/slide/trunk/setools.linux.x86_64 setools.linux.x86_64
# svn export http://oss.tresys.com/repos/slide/trunk/setools.linux.ppc setools.linux.ppc
# svn export http://oss.tresys.com/repos/slide/trunk/setools.linux.ppc64 setools.linux.ppc64
# tar -czf eclipse-setools.tar.gz *
#Source0: %{name}.tar.gz 
#Release: 0.2.svn1998%{?dist}

Source0: http://oss.tresys.com/projects/slide/chrome/site/src/%{name}-%{version}.tar.gz
Release: %mkrel 0.1.1
%ifarch %{ix86}
%define arch	x86
%else
%define arch %{_arch}
%endif

Requires: setools-libs-java >= %{require_setools_major_ver}%{require_setools_fix_ver}
Requires: eclipse-platform

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# Files under %%_libdir are either text files or symlinks to the libraries
# in setools-libs-java, so debuginfo rpm is useless.
%define debug_package %{nil}

%description
Eclipse SETools is an eclipse plugin exposing the java interfaces for SELinux
policy analysis tools for use in eclipse plugins.
The package inclues java runtime libraries for the following:

 libapol		policy analysis library
 libpoldiff		semantic policy difference library
 libqpol		library tha abstracts policy internals
 libseaudit		parse and filer SELinux audit messages in log files

%prep
%setup -q -c -n eclipse-setools

%build
export CLASSPATH=
export OPT_JAR_LIST=:
#cd ${RPM_BUILD_DIR}%{plugin_dir}
cd setools-plugin
%{ant} -f rpmbuild.xml build

%install
%{__rm} -rf %{buildroot}

PLUGIN_VER=`grep Bundle-Version setools-plugin/META-INF/MANIFEST.MF | cut -d : -f 2 | tr -d " "`
FRAGMENT_VER=`grep Bundle-Version setools.%{_os}.%{arch}/META-INF/MANIFEST.MF | cut -d : -f 2 | tr -d " "`

FEATURE_DIR=%{eclipse_base}/features/com.tresys.setools_%{version}
PLUGIN_DIR=%{eclipse_base}/plugins/com.tresys.setools_${PLUGIN_VER}
FRAGMENT_DIR=%{eclipse_lib_base}/plugins/com.tresys.setools.%{_os}.%{arch}_${FRAGMENT_VER}
FRAGMENT_SRC=eclipse-setools/setools.%{_os}.%{arch}

install -dp -m755 ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -dp -m755 ${RPM_BUILD_ROOT}${FEATURE_DIR}
install -dp -m755 ${RPM_BUILD_ROOT}${FRAGMENT_DIR}

install -dp -m755 ${RPM_BUILD_ROOT}${PLUGIN_DIR}/META-INF
#ln -s /usr/share/setools-3.3 ${RPM_BUILD_ROOT}/${PLUGIN_DIR}/setools
ln -s ../../../setools-%{require_setools_major_ver} ${RPM_BUILD_ROOT}/${PLUGIN_DIR}/setools

install -dp -m755 ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/lib
install -dp -m755 ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/META-INF

install -p -m644 ${RPM_BUILD_DIR}/eclipse-setools/setools-plugin/setools.jar ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-setools/setools-plugin/build.properties ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-setools/setools-plugin/plugin.properties ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-setools/setools-plugin/about.html ${RPM_BUILD_ROOT}${PLUGIN_DIR}
install -p -m644 ${RPM_BUILD_DIR}/eclipse-setools/setools-plugin/META-INF/MANIFEST.MF ${RPM_BUILD_ROOT}${PLUGIN_DIR}/META-INF

install -p -m644 ${RPM_BUILD_DIR}/${FRAGMENT_SRC}/build.properties ${RPM_BUILD_ROOT}${FRAGMENT_DIR}
install -p -m644 ${RPM_BUILD_DIR}/${FRAGMENT_SRC}/META-INF/MANIFEST.MF ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/META-INF
#cp -pd ${RPM_BUILD_DIR}/${FRAGMENT_SRC}/lib/* ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/lib
ln -s ../../../../libjapol.so.4 ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/lib/libjapol.so
ln -s ../../../../libjpoldiff.so.1 ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/lib/libjpoldiff.so
ln -s ../../../../libjqpol.so.1 ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/lib/libjqpol.so
ln -s ../../../../libjseaudit.so.4 ${RPM_BUILD_ROOT}${FRAGMENT_DIR}/lib/libjseaudit.so

install -p -m644 ${RPM_BUILD_DIR}/eclipse-setools/setools-feature/feature.xml ${RPM_BUILD_ROOT}${FEATURE_DIR}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
if [ -x %{_bindir}/rebuild-gcj-db ] 
then
	%{_bindir}/rebuild-gcj-db
fi

%postun
if [ -x %{_bindir}/rebuild-gcj-db ] 
then
	%{_bindir}/rebuild-gcj-db 
fi

%files
%defattr(-,root,root,0755)
%{eclipse_base}/plugins/com.tresys.setools*/
%{eclipse_base}/features/com.tresys.setools*/
%{eclipse_lib_base}/plugins/com.tresys.setools*/
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif
