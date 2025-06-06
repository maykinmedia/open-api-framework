.. open_api_framework documentation master file, created by startproject.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to open_api_framework's documentation!
=================================================

|build-status| |code-quality| |ruff| |coverage|

|python-versions| |django-versions|

A metapackage for registration components, that bundles the dependencies shared between these
components and provides generic base settings

Features
========

* Bundling shared dependencies and introducing minimum versions for these dependencies
* Providing generic base Django settings to avoid duplicate settings across registration components

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   reference
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |build-status| image:: https://github.com/maykinmedia/open-api-framework/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/open-api-framework/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Code+quality+checks%22

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |coverage| image:: https://codecov.io/gh/maykinmedia/open-api-framework/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/open-api-framework
    :alt: Coverage status

.. .. |docs| image:: https://readthedocs.org/projects/open-api-framework/badge/?version=latest
..     :target: https://open-api-framework.readthedocs.io/en/latest/?badge=latest
..     :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/open-api-framework.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/open-api-framework.svg

.. .. |pypi-version| image:: https://img.shields.io/pypi/v/open-api-framework.svg
..     :target: https://pypi.org/project/open-api-framework/
