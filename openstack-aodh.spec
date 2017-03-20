%global pypi_name aodh

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             openstack-aodh
Version:          4.0.0
Release:          1%{?dist}
Summary:          OpenStack Telemetry Alarming
License:          ASL 2.0
URL:              https://github.com/openstack/aodh.git
Source0:          https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

Source1:          %{pypi_name}-dist.conf
Source2:          %{pypi_name}.logrotate
Source10:         %{name}-api.service
Source11:         %{name}-evaluator.service
Source12:         %{name}-notifier.service
Source13:         %{name}-expirer.service
Source14:         %{name}-listener.service

BuildArch:        noarch

BuildRequires:    openstack-macros
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    systemd
BuildRequires:    python-pbr
BuildRequires:    python-sphinx
BuildRequires:    python-eventlet
BuildRequires:    python-cotyledon
# Required to compile translation files
BuildRequires:    python-babel


%description
Aodh is the alarm engine of the Ceilometer project.


%package          compat
Summary:          OpenStack aodh compat

Provides:         openstack-ceilometer-alarm = %{version}-%{release}
Obsoletes:        openstack-ceilometer-alarm < 1:6.0.0

Requires:         python-aodh
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

%package -n       python-aodh
Summary:          OpenStack aodh python libraries

Requires:         pysnmp
Requires:         pytz
Requires:         python-croniter

Requires:         python-jsonschema
Requires:         python-lxml

Requires:         python-alembic >= 0.7.2
Requires:         python-cachetools >= 1.1.6
Requires:         python-cotyledon
Requires:         python-eventlet >= 0.17.4
Requires:         python-futures >= 3.0
Requires:         python-futurist >= 0.11.0
Requires:         python-migrate
Requires:         python-oslo-context
Requires:         python-oslo-concurrency
Requires:         python-oslo-config >= 2:2.6.0
Requires:         python-oslo-db >= 4.16.0
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-log >= 1.2.0
Requires:         python-oslo-policy >= 0.5.0
Requires:         python-oslo-messaging >= 5.2.0
Requires:         python-oslo-middleware >= 3.22.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-service >= 0.1.0
Requires:         python-keystonemiddleware >= 2.2.0
Requires:         python-pbr
Requires:         python-pecan >= 0.8.0
Requires:         python-six >= 1.9.0
Requires:         python-stevedore >= 1.5.0
Requires:         python-sqlalchemy
Requires:         python-requests >= 2.5.2
Requires:         python-retrying
Requires:         python-tenacity >= 3.2.1
Requires:         python-tooz >= 1.28.0
Requires:         python-werkzeug
Requires:         python-webob
Requires:         python-wsme >= 0.8
Requires:         python-paste-deploy
Requires:         python-ceilometerclient
Requires:         python-gnocchiclient >= 2.1.0
Requires:         python-keystoneclient >= 1.6.0

%description -n   python-aodh
OpenStack aodh provides API and services for managing alarms.

This package contains the aodh python library.

%package        common
Summary:        Components common to all OpenStack aodh services

# Config file generation
BuildRequires:    python-oslo-config >= 2:2.6.0
BuildRequires:    python-oslo-concurrency
BuildRequires:    python-oslo-db
BuildRequires:    python-oslo-log
BuildRequires:    python-oslo-messaging
BuildRequires:    python-oslo-policy
BuildRequires:    python-oslo-reports
BuildRequires:    python-oslo-service
BuildRequires:    python-oslo-vmware >= 0.6.0
BuildRequires:    python-ceilometerclient
BuildRequires:    python-glanceclient >= 1:2.0.0
BuildRequires:    python-keystonemiddleware
BuildRequires:    python-neutronclient
BuildRequires:    python-novaclient  >= 1:2.29.0
BuildRequires:    python-swiftclient
BuildRequires:    python-croniter
BuildRequires:    python-jsonpath-rw
BuildRequires:    python-jsonpath-rw-ext
BuildRequires:    python-lxml
BuildRequires:    python-pecan >= 1.0.0
BuildRequires:    python-tooz
BuildRequires:    python-werkzeug
BuildRequires:    python-wsme >= 0.7
BuildRequires:    python-gnocchiclient >= 2.1.0

Requires:       python-aodh = %{version}-%{release}

Requires:       python-oslo-log
Requires:       python-oslo-utils >= 3.5.0
Requires:       python-six
Requires:       python-ceilometerclient

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(pre):    shadow-utils


%description    common
OpenStack aodh provides API and services for managing alarms.


%package        api

Summary:        OpenStack aodh api

Requires:       %{name}-common = %{version}-%{release}
Requires:       python-ceilometerclient

%description api
OpenStack aodh provides API and servicesfor managing alarms.

This package contains the aodh API service.


%package        evaluator

Summary:        OpenStack aodh evaluator

Requires:       %{name}-common = %{version}-%{release}

%description evaluator
OpenStack aodh provides API and services for managing alarms.

This package contains the aodh evaluator service.

%package        notifier

Summary:        OpenStack aodh notifier

Requires:       %{name}-common = %{version}-%{release}

%description notifier
OpenStack aodh provides API and services for managing alarms.

This package contains the aodh notifier service.

%package        listener

Summary:        OpenStack aodh listener

Requires:       %{name}-common = %{version}-%{release}

%description listener
OpenStack aodh provides API and services for managing alarms.

This package contains the aodh listener service.

%package        expirer

Summary:        OpenStack aodh expirer

Requires:       %{name}-common = %{version}-%{release}

%description expirer
OpenStack aodh provides API and services for managing alarms.

This package contains the aodh expirer service.

%package -n python-aodh-tests
Summary:        Aodh tests
Requires:       python-aodh = %{version}-%{release}

%description -n python-aodh-tests
OpenStack aodh provides API and services for managing alarms.

This package contains the Aodh test files.


%prep
%setup -q -n %{pypi_name}-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find aodh -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py
# FIXME (jpena): Remove buggy PO-Revision-Date lines in translation
# See https://bugs.launchpad.net/openstack-i18n/+bug/1586041 for details
sed -i '/^\"PO-Revision-Date: \\n\"/d' aodh/locale/*/LC_MESSAGES/*.po

rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=etc/aodh/aodh-config-generator.conf --output-file=aodh/aodh.conf

%{__python2} setup.py build
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{pypi_name}/locale


# Programmatically update defaults in sample config
# which is installed at /etc/aodh/aodh.conf
# TODO: Make this more robust
# Note it only edits the first occurrence, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" aodh/aodh.conf
done < %{SOURCE1}



%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Create fake egg-info for the tempest plugin
# TODO switch to %{service} everywhere as in openstack-example.spec
%global service aodh
%py2_entrypoint %{service} %{service}

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/aodh
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/aodh/aodh-dist.conf
install -p -D -m 640 aodh/aodh.conf %{buildroot}%{_sysconfdir}/aodh/aodh.conf
install -p -D -m 640 aodh/api/policy.json %{buildroot}%{_sysconfdir}/aodh/policy.json

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/aodh
install -d -m 755 %{buildroot}%{_sharedstatedir}/aodh/tmp
install -d -m 750 %{buildroot}%{_localstatedir}/log/aodh

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
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*/LC_*/%{pypi_name}*po
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{pypi_name}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{pypi_name} --all-name

# Remove unused files
rm -fr %{buildroot}/usr/etc

%pre common
getent group aodh >/dev/null || groupadd -r aodh
if ! getent passwd aodh >/dev/null; then
  useradd -r -g aodh -G aodh -d %{_sharedstatedir}/aodh -s /sbin/nologin -c "OpenStack aodh Daemons" aodh
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

%files -n python-aodh
%{python2_sitelib}/aodh
%{python2_sitelib}/aodh-*.egg-info
%license LICENSE
%exclude %{python2_sitelib}/aodh/tests

%files -n python-aodh-tests
%license LICENSE
%{python2_sitelib}/aodh/tests
%{python2_sitelib}/%{service}_tests.egg-info

%files common -f %{pypi_name}.lang
%doc README.rst
%dir %{_sysconfdir}/aodh
%attr(-, root, aodh) %{_datadir}/aodh/aodh-dist.conf
%config(noreplace) %attr(-, root, aodh) %{_sysconfdir}/aodh/aodh.conf
%config(noreplace) %attr(-, root, aodh) %{_sysconfdir}/aodh/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %attr(0755, aodh, root)  %{_localstatedir}/log/aodh
%{_bindir}/aodh-dbsync

%defattr(-, aodh, aodh, -)
%dir %{_sharedstatedir}/aodh
%dir %{_sharedstatedir}/aodh/tmp

%files api
%{_bindir}/aodh-api
%{_bindir}/aodh-combination-alarm-conversion
%{_unitdir}/%{name}-api.service

%files evaluator
%{_bindir}/aodh-evaluator
%{_unitdir}/%{name}-evaluator.service

%files notifier
%{_bindir}/aodh-notifier
%{_unitdir}/%{name}-notifier.service

%files listener
%{_bindir}/aodh-listener
%{_unitdir}/%{name}-listener.service


%files expirer
%{_bindir}/aodh-expirer
%{_unitdir}/%{name}-expirer.service


%changelog
* Thu Feb 09 2017 Alfredo Moralejo <amoralej@redhat.com> 4.0.0-1
- Update to 4.0.0

