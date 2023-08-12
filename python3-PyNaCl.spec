#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	PyNaCl
Summary:	Python 2 binding to the Networking and Cryptography (NaCl) library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki NaCl (Networking and Cryptography)
Name:		python3-%{module}
Version:	1.5.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/pyca/pynacl/archive/%{version}/pynacl-%{version}.tar.gz
# Source0-md5:	5f4332422b2be24fb1584eb447061b30
URL:		https://github.com/pyca/pynacl/
BuildRequires:	libsodium-devel >= 1.0.18
BuildRequires:	python3-cffi >= 1.4.1
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis >= 3.27.0
BuildRequires:	python3-pytest >= 3.3.1
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.6.5
%endif
Requires:	libsodium >= 1.0.18
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyNaCl is a Python binding to libsodium, which is a fork of the
Networking and Cryptography library.

%description -l pl.UTF-8
PyNaCl to wiązanie Pythona do libsodium - odgałęzienia biblioteki
NaCl (Networking and Cryptography).

%package apidocs
Summary:	API documentation for PyNaCl module
Summary(pl.UTF-8):	Dokumentacja API modułu PyNaCl
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for PyNaCl module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu PyNaCl.

%prep
%setup -q -n pynacl-%{version}

%build
export SODIUM_INSTALL=system

%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

export SODIUM_INSTALL=system

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%dir %{py3_sitedir}/nacl
%attr(755,root,root) %{py3_sitedir}/nacl/_sodium.abi3.so
%{py3_sitedir}/nacl/py.typed
%{py3_sitedir}/nacl/*.py
%{py3_sitedir}/nacl/__pycache__
%{py3_sitedir}/nacl/bindings
%{py3_sitedir}/nacl/pwhash
%{py3_sitedir}/PyNaCl-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_downloads,_images,_modules,_static,api,vectors,*.html,*.js}
%endif
