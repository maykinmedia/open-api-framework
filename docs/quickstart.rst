==========
Quickstart
==========

Requirements
============

* Python 3.12 or above
* Django 5.2 or newer

Installation
============

1. Add open-api-framework to your requirements file
2. Remove dependencies from your requirements file that occur in ``pyproject.toml``
3. Recompile the dependencies


Usage
=====

If you want to reuse the generic base settings, you can do the following:

Add the following imports to the top of the project's ``base.py`` file:

.. code:: python

    from open_api_framework.conf.base import *  # noqa
    from open_api_framework.conf.utils import config


After that, compare the settings from `open_api_framework.conf.base`_ to the settings
defined in the project's ``base.py`` and remove settings from the latter to make use of the generic settings (if this is desired).

.. warning::

    All settings defined in ``open_api_framework.conf.base`` will be loaded when importing from
    that file, even if only specific settings are imported.

.. _open_api_framework.conf.base: https://github.com/maykinmedia/open-api-framework/blob/main/open_api_framework/conf/base.py
