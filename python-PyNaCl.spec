#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	PyNaCl
Summary:	Python 2 binding to the Networking and Cryptography (NaCl) library
Summary(pl.UTF-8):	Wiązania Pythona 2 do biblioteki NaCl (Networking and Cryptography)
Name:		python-%{module}
Version:	1.4.0
Release:	6
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/pyca/pynacl/archive/%{version}/pynacl-%{version}.tar.gz
# Source0-md5:	50b7f2d00b16c270095b7ae4bea9fba8
Patch0:		%{name}-no-wheel.patch
URL:		https://github.com/dstufft/pynacl/
BuildRequires:	libsodium-devel >= 1.0.18
%if %{with python2}
BuildRequires:	python-cffi >= 1.4.1
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-hypothesis >= 3.27.0
BuildRequires:	python-pytest >= 3.3.1
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-cffi >= 1.4.1
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis >= 3.27.0
BuildRequires:	python3-pytest >= 3.3.1
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-six
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

%package -n python3-%{module}
Summary:	Python 3 binding to the Networking and Cryptography (NaCl) library
Summary(pl.UTF-8):	Wiązania Pythona 3 do biblioteki NaCl (Networking and Cryptography)
Group:		Libraries/Python
Requires:	libsodium >= 1.0.18

%description -n python3-%{module}
PyNaCl is a Python binding to libsodium, which is a fork of the
Networking and Cryptography library.

%description -n python3-%{module} -l pl.UTF-8
PyNaCl to wiązanie Pythona do libsodium - odgałęzienia biblioteki
NaCl (Networking and Cryptography).

%package apidocs
Summary:	API documentation for PyNaCl module
Summary(pl.UTF-8):	Dokumentacja API modułu PyNaCl
Group:		Documentation

%description apidocs
API documentation for PyNaCl module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu PyNaCl.

%prep
%setup -q -n pynacl-%{version}
%patch0 -p1

%build
export SODIUM_INSTALL=system

%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-2/lib.*) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

export SODIUM_INSTALL=system

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%dir %{py_sitedir}/nacl
%attr(755,root,root) %{py_sitedir}/nacl/_sodium.so
%{py_sitedir}/nacl/*.py[co]
%{py_sitedir}/nacl/bindings
%{py_sitedir}/nacl/pwhash
%{py_sitedir}/PyNaCl-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%dir %{py3_sitedir}/nacl
%attr(755,root,root) %{py3_sitedir}/nacl/_sodium.abi3.so
%{py3_sitedir}/nacl/*.py
%{py3_sitedir}/nacl/__pycache__
%{py3_sitedir}/nacl/bindings
%{py3_sitedir}/nacl/pwhash
%{py3_sitedir}/PyNaCl-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_downloads,_images,_modules,_static,api,vectors,*.html,*.js}
%endif
