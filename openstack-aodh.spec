%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    openstack-macros
BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    systemd
BuildRequires:    python3-pbr
BuildRequires:    python3-sphinx
BuildRequires:    python3-cotyledon
# Required to compile translation files
BuildRequires:    python3-babel


%description
Aodh is the alarm engine of the Ceilometer project.


%package          compat
Summary:          OpenStack %{service} compat

Provides:         openstack-ceilometer-alarm = %{version}-%{release}
Obsoletes:        openstack-ceilometer-alarm < 1:6.0.0

Requires:         python3-aodh
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

%package -n       python3-%{service}
Summary:          OpenStack %{service} python libraries
%{?python_provide:%python_provide python3-%{service}}

Requires:         python3-pytz >= 2013.6
Requires:         python3-croniter >= 0.3.4
Requires:         python3-jsonschema >= 3.2.0
Requires:         python3-alembic >= 0.7.2
Requires:         python3-cachetools >= 1.1.6
Requires:         python3-cotyledon
Requires:         python3-futurist >= 0.11.0
Requires:         python3-oslo-config >= 2:6.8.0
Requires:         python3-oslo-db >= 4.8.0
Requires:         python3-oslo-i18n >= 1.5.0
Requires:         python3-oslo-log >= 4.3.0
Requires:         python3-oslo-policy >= 3.7.0
Requires:         python3-oslo-reports >= 1.18.0
Requires:         python3-oslo-messaging >= 5.2.0
Requires:         python3-oslo-middleware >= 3.22.0
Requires:         python3-oslo-upgradecheck >= 1.3.0
Requires:         python3-keystonemiddleware >= 5.1.0
Requires:         python3-pbr >= 2.0.0
Requires:         python3-pecan >= 0.8.0
Requires:         python3-stevedore >= 1.5.0
Requires:         python3-sqlalchemy >= 1.4.1
Requires:         python3-requests >= 2.5.2
Requires:         python3-tenacity >= 3.2.1
Requires:         python3-tooz >= 1.28.0
Requires:         python3-webob >= 1.2.3
Requires:         python3-wsme >= 0.8
Requires:         python3-dateutil
Requires:         python3-gnocchiclient >= 6.0.0
Requires:         python3-keystoneclient >= 1.6.0
Requires:         python3-heatclient >= 1.17.0
Requires:         python3-keystoneauth1 >= 2.1
Requires:         python3-octaviaclient >= 1.8.0
Requires:         python3-debtcollector >= 1.2.0
Requires:         python3-voluptuous >= 0.8.10

Requires:         python3-lxml >= 2.3
Requires:         python3-paste-deploy >= 1.5.0
Requires:         python3-oslo-context >= 2.22.0


%description -n   python3-%{service}
%{common_desc}

This package contains the %{service} python library.

%package        common
Summary:        Components common to all OpenStack %{service} services

# Config file generation
BuildRequires:    python3-oslo-config >= 2:6.8.0
BuildRequires:    python3-oslo-context
BuildRequires:    python3-oslo-db
BuildRequires:    python3-oslo-log
BuildRequires:    python3-oslo-messaging
BuildRequires:    python3-oslo-policy
BuildRequires:    python3-oslo-reports
BuildRequires:    python3-oslo-upgradecheck >= 0.1.1
BuildRequires:    python3-oslo-vmware >= 0.6.0
BuildRequires:    python3-glanceclient >= 1:2.0.0
BuildRequires:    python3-heatclient
BuildRequires:    python3-keystonemiddleware
BuildRequires:    python3-neutronclient
BuildRequires:    python3-novaclient  >= 1:2.29.0
BuildRequires:    python3-swiftclient
BuildRequires:    python3-croniter
BuildRequires:    python3-jsonpath-rw-ext
BuildRequires:    python3-pecan >= 1.0.0
BuildRequires:    python3-tooz
BuildRequires:    python3-wsme >= 0.7
BuildRequires:    python3-dateutil
BuildRequires:    python3-gnocchiclient >= 6.0.0
BuildRequires:    python3-octaviaclient

BuildRequires:    python3-jsonpath-rw
BuildRequires:    python3-lxml


Requires:       python3-aodh = %{version}-%{release}

Requires:       python3-oslo-utils >= 3.5.0

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

%package -n python3-%{service}-tests
Summary:        Aodh tests
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       python3-aodh = %{version}-%{release}
Requires:       python3-gabbi >= 1.30.0

%description -n python3-%{service}-tests
%{common_desc}

This package contains the %{service} test files.


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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
PYTHONPATH=. oslo-config-generator --config-file=%{service}/cmd/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

%{py3_build}
# Generate i18n files
%{__python3} setup.py compile_catalog -d build/lib/%{service}/locale --domain aodh


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
%{py3_install}

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 %{service}/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf
install -p -D -m 640 %{service}/api/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini

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
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

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

%files -n python3-%{service}
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info
%license LICENSE
%exclude %{python3_sitelib}/%{service}/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%files common -f %{service}.lang
%doc README.rst
%dir %{_sysconfdir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0750, %{service}, root)  %{_localstatedir}/log/%{service}
%{_bindir}/%{service}-dbsync
%{_bindir}/%{service}-config-generator
%{_bindir}/%{service}-status

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
