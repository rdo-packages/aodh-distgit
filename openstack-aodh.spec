# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global service aodh

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc OpenStack %{service} provides API and services for managing alarms.

Name:             openstack-%{service}
Version:          XXX
Release:          XXX
Summary:          OpenStack Telemetry Alarming
License:          ASL 2.0
URL:              https://github.com/openstack/%{service}.git
Source0:          https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

Source1:          %{service}-dist.conf
Source2:          %{service}.logrotate
Source10:         %{name}-api.service
Source11:         %{name}-evaluator.service
Source12:         %{name}-notifier.service
Source13:         %{name}-expirer.service
Source14:         %{name}-listener.service

BuildArch:        noarch

BuildRequires:    openstack-macros
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-devel
BuildRequires:    systemd
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-cotyledon
# Required to compile translation files
BuildRequires:    python%{pyver}-babel


%description
Aodh is the alarm engine of the Ceilometer project.


%package          compat
Summary:          OpenStack %{service} compat

Provides:         openstack-ceilometer-alarm = %{version}-%{release}
Obsoletes:        openstack-ceilometer-alarm < 1:6.0.0

Requires:         python%{pyver}-aodh
Requires:         %{name}-common
Requires:         %{name}-api
Requires:         %{name}-evaluator
Requires:         %{name}-notifier
Requires:         %{name}-expirer
Requires:         %{name}-listener

%description      compat
This package only exists to help transition openstack-ceilometer-alarm users
to the new package split. It will be removed after one distribution release
cycle, please do not reference it or depend on it in any way.

%package -n       python%{pyver}-%{service}
Summary:          OpenStack %{service} python libraries
%{?python_provide:%python_provide python%{pyver}-%{service}}

Requires:         python%{pyver}-pytz
Requires:         python%{pyver}-croniter

Requires:         python%{pyver}-jsonschema

Requires:         python%{pyver}-alembic >= 0.7.2
Requires:         python%{pyver}-cachetools >= 1.1.6
Requires:         python%{pyver}-cotyledon
Requires:         python%{pyver}-futurist >= 0.11.0
Requires:         python%{pyver}-oslo-config >= 2:2.6.0
Requires:         python%{pyver}-oslo-db >= 4.16.0
Requires:         python%{pyver}-oslo-i18n >= 1.5.0
Requires:         python%{pyver}-oslo-log >= 1.2.0
Requires:         python%{pyver}-oslo-policy >= 0.5.0
Requires:         python%{pyver}-oslo-messaging >= 5.2.0
Requires:         python%{pyver}-oslo-middleware >= 3.22.0
Requires:         python%{pyver}-oslo-serialization >= 1.4.0
Requires:         python%{pyver}-oslo-service >= 0.1.0
Requires:         python%{pyver}-keystonemiddleware >= 2.2.0
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-pecan >= 0.8.0
Requires:         python%{pyver}-six >= 1.9.0
Requires:         python%{pyver}-stevedore >= 1.5.0
Requires:         python%{pyver}-sqlalchemy
Requires:         python%{pyver}-requests >= 2.5.2
Requires:         python%{pyver}-tenacity >= 3.2.1
Requires:         python%{pyver}-tooz >= 1.28.0
Requires:         python%{pyver}-webob
Requires:         python%{pyver}-wsme >= 0.8
Requires:         python%{pyver}-gnocchiclient >= 3.1.0
Requires:         python%{pyver}-keystoneclient >= 1.6.0
Requires:         python%{pyver}-keystoneauth1 >= 2.1
Requires:         python%{pyver}-debtcollector
Requires:         python%{pyver}-voluptuous >= 0.8.10

%if %{pyver} == 2
Requires:         pysnmp
Requires:         python%{pyver}-futures >= 3.0
Requires:         python-lxml
Requires:         python-paste-deploy
%else
Requires:         python%{pyver}-pysnmp
Requires:         python%{pyver}-lxml
Requires:         python%{pyver}-paste-deploy
%endif


%description -n   python%{pyver}-%{service}
%{common_desc}

This package contains the %{service} python library.

%package        common
Summary:        Components common to all OpenStack %{service} services

# Config file generation
BuildRequires:    python%{pyver}-oslo-config >= 2:2.6.0
BuildRequires:    python%{pyver}-oslo-db
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-messaging
BuildRequires:    python%{pyver}-oslo-policy
BuildRequires:    python%{pyver}-oslo-reports
BuildRequires:    python%{pyver}-oslo-service
BuildRequires:    python%{pyver}-oslo-vmware >= 0.6.0
BuildRequires:    python%{pyver}-glanceclient >= 1:2.0.0
BuildRequires:    python%{pyver}-keystonemiddleware
BuildRequires:    python%{pyver}-neutronclient
BuildRequires:    python%{pyver}-novaclient  >= 1:2.29.0
BuildRequires:    python%{pyver}-swiftclient
BuildRequires:    python%{pyver}-croniter
BuildRequires:    python%{pyver}-jsonpath-rw-ext
BuildRequires:    python%{pyver}-pecan >= 1.0.0
BuildRequires:    python%{pyver}-tooz
BuildRequires:    python%{pyver}-wsme >= 0.7
BuildRequires:    python%{pyver}-gnocchiclient >= 3.1.0

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-jsonpath-rw
BuildRequires:    python-lxml
%else
BuildRequires:    python%{pyver}-jsonpath-rw
BuildRequires:    python%{pyver}-lxml
%endif


Requires:       python%{pyver}-aodh = %{version}-%{release}

Requires:       python%{pyver}-oslo-utils >= 3.5.0

%{?systemd_requires}
Requires(pre):    shadow-utils


%description    common
%{common_desc}


%package        api

Summary:        OpenStack %{service} API

Requires:       %{name}-common = %{version}-%{release}

%description api
%{common_desc}

This package contains the %{service} API service.


%package        evaluator

Summary:        OpenStack %{service} evaluator

Requires:       %{name}-common = %{version}-%{release}

%description evaluator
%{common_desc}

This package contains the %{service} evaluator service.

%package        notifier

Summary:        OpenStack %{service} notifier

Requires:       %{name}-common = %{version}-%{release}

%description notifier
%{common_desc}

This package contains the %{service} notifier service.

%package        listener

Summary:        OpenStack %{service} listener

Requires:       %{name}-common = %{version}-%{release}

%description listener
%{common_desc}

This package contains the %{service} listener service.

%package        expirer

Summary:        OpenStack %{service} expirer

Requires:       %{name}-common = %{version}-%{release}

%description expirer
%{common_desc}

This package contains the %{service} expirer service.

%package -n python%{pyver}-%{service}-tests
Summary:        Aodh tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}
Requires:       python%{pyver}-aodh = %{version}-%{release}
Requires:       python%{pyver}-gabbi >= 1.30.0

%description -n python%{pyver}-%{service}-tests
%{common_desc}

This package contains the %{service} test files.


%prep
%setup -q -n %{service}-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py
# FIXME (jpena): Remove buggy PO-Revision-Date lines in translation
# See https://bugs.launchpad.net/openstack-i18n/+bug/1586041 for details
sed -i '/^\"PO-Revision-Date: \\n\"/d' %{service}/locale/*/LC_MESSAGES/*.po

%py_req_cleanup


%build
# Generate config file
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=%{service}/cmd/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

%{pyver_build}
# Generate i18n files
%{pyver_bin} setup.py compile_catalog -d build/lib/%{service}/locale


# Programmatically update defaults in sample config
# which is installed at /etc/aodh/aodh.conf
# TODO: Make this more robust
# Note it only edits the first occurrence, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" %{service}/%{service}.conf
done < %{SOURCE1}



%install
%{pyver_install}

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 %{service}/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}/tmp
install -d -m 750 %{buildroot}%{_localstatedir}/log/%{service}

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Install systemd unit services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-evaluator.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-notifier.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-expirer.service
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/%{name}-listener.service

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{pyver_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{pyver_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

# Remove unused files
rm -fr %{buildroot}/usr/etc

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
if ! getent passwd %{service} >/dev/null; then
  useradd -r -g %{service} -G %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin -c "OpenStack %{service} Daemons" %{service}
fi
exit 0

%post -n %{name}-api
%systemd_post %{name}-api.service

%preun -n %{name}-api
%systemd_preun %{name}-api.service

%post -n %{name}-evaluator
%systemd_post %{name}-evaluator.service

%preun -n %{name}-evaluator
%systemd_preun %{name}-evaluator.service

%post -n %{name}-notifier
%systemd_post %{name}-notifier.service

%preun -n %{name}-notifier
%systemd_preun %{name}-notifier.service

%post -n %{name}-listener
%systemd_post %{name}-listener.service

%preun -n %{name}-listener
%systemd_preun %{name}-listener.service

%post -n %{name}-expirer
%systemd_post %{name}-expirer.service

%preun -n %{name}-expirer
%systemd_preun %{name}-expirer.service

%files compat
# empty files`

%files -n python%{pyver}-%{service}
%{pyver_sitelib}/%{service}
%{pyver_sitelib}/%{service}-*.egg-info
%license LICENSE
%exclude %{pyver_sitelib}/%{service}/tests

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/tests

%files common -f %{service}.lang
%doc README.rst
%dir %{_sysconfdir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0750, %{service}, root)  %{_localstatedir}/log/%{service}
%{_bindir}/%{service}-dbsync
%{_bindir}/%{service}-config-generator

%defattr(-, %{service}, %{service}, -)
%dir %{_sharedstatedir}/%{service}
%dir %{_sharedstatedir}/%{service}/tmp

%files api
%{_bindir}/%{service}-api
%{_unitdir}/%{name}-api.service

%files evaluator
%{_bindir}/%{service}-evaluator
%{_unitdir}/%{name}-evaluator.service

%files notifier
%{_bindir}/%{service}-notifier
%{_unitdir}/%{name}-notifier.service

%files listener
%{_bindir}/%{service}-listener
%{_unitdir}/%{name}-listener.service


%files expirer
%{_bindir}/%{service}-expirer
%{_unitdir}/%{name}-expirer.service


%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/aodh/commit/?id=bef0f9bfd0db5ad604d85766b0d3200625355c95
