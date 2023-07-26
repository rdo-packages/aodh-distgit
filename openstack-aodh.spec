%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%global service aodh

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx openstackdocstheme

%global common_desc OpenStack %{service} provides API and services for managing alarms.

Name:             openstack-%{service}
Version:          XXX
Release:          XXX
Summary:          OpenStack Telemetry Alarming
License:          Apache-2.0
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
BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    systemd

%description
Aodh is the alarm engine of the Ceilometer project.


%package          compat
Summary:          OpenStack %{service} compat

Provides:         openstack-ceilometer-alarm = %{version}-%{release}
Obsoletes:        openstack-ceilometer-alarm < 1:6.0.0

Requires:         %{name}-common = %{version}-%{release}
Requires:         %{name}-api = %{version}-%{release}
Requires:         %{name}-evaluator = %{version}-%{release}
Requires:         %{name}-notifier = %{version}-%{release}
Requires:         %{name}-expirer = %{version}-%{release}
Requires:         %{name}-listener = %{version}-%{release}

%description      compat
This package only exists to help transition openstack-ceilometer-alarm users
to the new package split. It will be removed after one distribution release
cycle, please do not reference it or depend on it in any way.

%package -n       python3-%{service}
Summary:          OpenStack %{service} python libraries

%description -n   python3-%{service}
%{common_desc}

This package contains the %{service} python library.

%package        common
Summary:        Components common to all OpenStack %{service} services

Requires:       python3-aodh = %{version}-%{release}

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

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

sed -i "s/^ *gnocchi.*/  gnocchi/g" tox.ini
sed -i "/^ *pifpaf.*/d" tox.ini
sed -i "/.*AODH_TEST_DEPS.*/d" tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=%{service}/cmd/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

%pyproject_wheel


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
%pyproject_install

# Generate i18n files
%{__python3} setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/%{service}/locale --domain aodh


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

%check
%tox -e %{default_toxenv}

%files compat
# empty files`

%files -n python3-%{service}
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.dist-info
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
