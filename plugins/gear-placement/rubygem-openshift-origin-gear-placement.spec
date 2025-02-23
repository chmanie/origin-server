%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
%endif
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name openshift-origin-gear-placement
%global rubyabi 1.9.1

Summary:       OpenShift plugin for customizing the gear placement algorithm
Name:          rubygem-%{gem_name}
Version:       0.0.2
Release:       1%{?dist}
Group:         Development/Languages
License:       ASL 2.0
URL:           http://openshift.redhat.com
Source0:       http://mirror.openshift.com/pub/openshift-origin/source/%{name}/rubygem-%{gem_name}-%{version}.tar.gz
%if 0%{?fedora} >= 19
Requires:      ruby(release)
%else
Requires:      %{?scl:%scl_prefix}ruby(abi) >= %{rubyabi}
%endif
Requires:      %{?scl:%scl_prefix}rubygems
Requires:      %{?scl:%scl_prefix}rubygem(json)
Requires:      rubygem(openshift-origin-common)
%if 0%{?fedora}%{?rhel} <= 6
BuildRequires: %{?scl:%scl_prefix}build
BuildRequires: scl-utils-build
%endif
%if 0%{?fedora} >= 19
BuildRequires: ruby(release)
%else
BuildRequires: %{?scl:%scl_prefix}ruby(abi) >= %{rubyabi}
%endif
BuildRequires: %{?scl:%scl_prefix}rubygems
BuildRequires: %{?scl:%scl_prefix}rubygems-devel
BuildArch:     noarch

%description
OpenShift plugin for customizing the gear placement algorithm. It can be used to determine which node a gear resides on.

%prep
%setup -q

%build
%{?scl:scl enable %scl - << \EOF}
mkdir -p .%{gem_dir}
# Build and install into the rubygem structure
gem build %{gem_name}.gemspec
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force %{gem_name}-%{version}.gem
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/etc/openshift/plugins.d
cp conf/openshift-origin-gear-placement.conf.example %{buildroot}/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.example
cp conf/openshift-origin-gear-placement.conf.blacklisted-vendor-example %{buildroot}/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.blacklisted-vendor-example
cp conf/openshift-origin-gear-placement.conf.pin-php-to-host-example %{buildroot}/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.pin-php-to-host-example
cp conf/openshift-origin-gear-placement.conf.pin-user-to-host-example %{buildroot}/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.pin-user-to-host-example

%files
%dir %{gem_instdir}
%dir %{gem_dir}
%doc Gemfile LICENSE README
%{gem_dir}/doc/%{gem_name}-%{version}
%{gem_dir}/gems/%{gem_name}-%{version}
%{gem_dir}/cache/%{gem_name}-%{version}.gem
%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.example
/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.blacklisted-vendor-example
/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.pin-php-to-host-example
/etc/openshift/plugins.d/openshift-origin-gear-placement.conf.pin-user-to-host-example

%changelog
* Tue Aug 26 2014 Adam Miller <admiller@redhat.com> 0.0.2-1
- new package built with tito

