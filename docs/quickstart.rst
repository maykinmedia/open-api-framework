==========
Quickstart
==========

Requirements
============

* Python 3.9 or above
* Django 4.2 or newer

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

Documenting environment variables
---------------------------------

This library provides utilities and a management command to generate .rst style documentation for environment variables that are
in your project. The :func:`open_api_framework.conf.utils.config` can be used for this as follows to
specify environment variable documentation. By default, all environment variables are added
to the documentation (unless ``add_to_docs=False`` is passed to ``config``).

.. code:: python

    from open_api_framework.conf.base import *  # noqa
    from open_api_framework.conf.utils import config

    config(
        "DB_NAME",
        PROJECT_DIRNAME,
        group="Database",
        help_text="name of the PostgreSQL database.",
    )

The generic base settings are documented in the same way, so these will be automatically picked up
when generating the documentation. In order to generate the documentation, the run the following command:

.. code:: bash

    python src/manage.py generate_envvar_docs --file docs/installation/config.rst

If no ``--file`` is supplied, it will write to ``docs/env_config.rst``.
Additionally, if some groups do not apply for your project, they can be excluded from the docs like this:

.. code:: bash

    python src/manage.py generate_envvar_docs --exclude-group Celery --exclude-group Cross-Origin-Resource-Sharing

In order to add extra information for your project, add a template in ``templates/open_api_framework/env_config.rst`` and customize it:

.. code:: html

    {% extends "open_api_framework/env_config.rst" %}

    {% block intro %}
    Intro
    -----

    <some introductory information>

    {% endblock %}

    {% block extra %}

    Custom section
    --------------

    <some extra information>

    {% endblock %}



.. note::

    Currently only environment variables that are part of settings or modules that are loaded
    when running management commands are included in the documentation


.. _open_api_framework.conf.base: https://github.com/maykinmedia/open-api-framework/blob/main/open_api_framework/conf/base.py
