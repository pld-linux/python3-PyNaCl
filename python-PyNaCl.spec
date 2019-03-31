#
# Conditional build:
%bcond_with	doc		# build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module	PyNaCl
Summary:	Python binding to the Networking and Cryptography (NaCl) library
Name:		python-%{module}
Version:	1.3.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/pyca/pynacl/archive/%{version}.tar.gz
# Source0-md5:	cb6560512d1d2300b3ddbe1a1daf871d
URL:		https://github.com/dstufft/pynacl/
BuildRequires:	libsodium-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	python-modules
BuildRequires:	python-six
%if %{with tests}
BuildRequires:	python-hypothesis >= 3.27.0
BuildRequires:	python-pytest > 3.3.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
BuildRequires:	python3-six
%if %{with tests}
BuildRequires:	python3-hypothesis >= 3.27.0
BuildRequires:	python3-pytest > 3.3.0
%endif
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PyNaCl is a Python binding to libsodium, which is a fork of the
Networking and Cryptography library.

%package -n python3-%{module}
Summary:	Python binding to the Networking and Cryptography (NaCl) library
Group:		Libraries/Python

%description -n python3-%{module}
PyNaCl is a Python binding to libsodium, which is a fork of the
Networking and Cryptography library.

%package apidocs
Summary:	%{module} API documentation
Group:		Documentation

%description apidocs
API documentation for %{module}.

%prep
%setup -q -n pynacl-%{version}

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
SODIUM_INSTALL=system; export SODIUM_INSTALL \
%py_build %{?with_tests:test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
SODIUM_INSTALL=system; export SODIUM_INSTALL \
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd docs
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
SODIUM_INSTALL=system; export SODIUM_INSTALL \
%py_install

%py_postclean

%endif

%if %{with python3}
SODIUM_INSTALL=system; export SODIUM_INSTALL \
%py3_install

%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%dir %{py_sitedir}/nacl
%attr(755,root,root) %{py_sitedir}/nacl/*.so
%{py_sitedir}/nacl/*.py[co]
%dir %{py_sitedir}/nacl/bindings
%{py_sitedir}/nacl/bindings/*.py[co]
%dir %{py_sitedir}/nacl/pwhash
%{py_sitedir}/nacl/pwhash/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitedir}/PyNaCl-%{version}-py*.egg-info
%endif
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%dir %{py3_sitedir}/nacl
%attr(755,root,root) %{py3_sitedir}/nacl/*.so
%{py3_sitedir}/nacl/*.py
%dir %{py3_sitedir}/nacl/__pycache__
%{py3_sitedir}/nacl/__pycache__/*.py[co]
%dir %{py3_sitedir}/nacl/bindings
%{py3_sitedir}/nacl/bindings/*.py
%dir %{py3_sitedir}/nacl/bindings/__pycache__
%{py3_sitedir}/nacl/bindings/__pycache__/*.py[co]
%dir %{py3_sitedir}/nacl/pwhash
%{py3_sitedir}/nacl/pwhash/*.py
%dir %{py3_sitedir}/nacl/pwhash/__pycache__
%{py3_sitedir}/nacl/pwhash/__pycache__/*.py[co]
%{py3_sitedir}/PyNaCl-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
