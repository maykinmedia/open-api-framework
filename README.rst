Open API Framework
==================

:Version: 0.4.2
:Source: https://github.com/maykinmedia/open-api-framework
:Keywords: metapackage, dependencies

|build-status| |code-quality| |black| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

A metapackage for registration components, that bundles the dependencies shared between these components

.. contents::

.. section-numbering::

Features
========

* Bundling shared dependencies and introducing minimum versions for these dependencies
* Providing generic base Django settings to avoid duplicate settings across registration components

Installation
============

Requirements
------------

* Python 3.9 or above
* Django 4.2 or newer


Install
-------

1. Add open-api-framework to your requirements file
2. Remove dependencies from your requirements file that occur in ``pyproject.toml``
3. Recompile the dependencies

If you want to reuse the generic base settings, you can do the following:

* Add the following imports to the top of the project's ``base.py`` file:

.. code:: python

    from open_api_framework.conf.base import *  # noqa
    from open_api_framework.conf.utils import config

* Then you can initialize sentry by adding the following line to ``base.py``:

.. code:: python

    init_sentry()

* After that, compare the settings from ``open_api_framework.conf.base`` to the settings defined in the project's
`base.py <open_api_framework/conf/base.py>`_ and remove settings from the latter to make use of the generic settings (if this is desired).

Local development
=================

To install and develop the library locally, use:

.. code-block:: bash

    pip install -e .[tests,coverage,docs,release]

When running management commands via ``django-admin``, make sure to add the root
directory to the python path (or use ``python -m django <command>``):

.. code-block:: bash

    export PYTHONPATH=. DJANGO_SETTINGS_MODULE=testapp.settings
    django-admin check
    # or other commands like:
    # django-admin makemessages -l nl

License
=======

Copyright © Maykin 2024

Licensed under the `MIT license`.


.. _`MIT license`: LICENSE


.. |build-status| image:: https://github.com/maykinmedia/open-api-framework/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/open-api-framework/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/open-api-framework/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/open-api-framework/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/open-api-framework
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/open-api-framework/badge/?version=latest
    :target: https://open-api-framework.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/open-api-framework.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/open-api-framework.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/open-api-framework.svg
    :target: https://pypi.org/project/open-api-framework/
