{% load doc_tags %}.. _installation_configuration_cli:

===================={{ project_name|repeat_char:"="}}
{{ project_name }} configuration (CLI)
===================={{ project_name|repeat_char:"="}}

After deploying {{ project_name }}, it needs to be configured to be fully functional.
The django management command ``setup_configuration`` assist with this configuration.
You can get the full command documentation with:

.. code-block:: bash

    python ./src/manage.py setup_configuration --help

.. warning:: This command is declarative - if configuration is manually changed after
   running the command and you then run the exact same command again, the manual
   changes will be reverted.

Preparation
===========

The command executes the list of pluggable configuration steps, and each step
requires specific configuration information, that should be prepared.
Here is the description of all available configuration steps and the configuration
format, used by each step.

{% for step_path in setup_configuraiton_steps %}
{% render_setup_configuraiton_step step_path %}
{% endfor %}


Execution
=========

{{ project_name }} configuration
{{ project_name|repeat_char:"-"}}--------------

With the full command invocation, everything is configured at once. Each configuration step
is idempotent, so any manual changes made via the admin interface will be updated if the command
is run afterwards.

.. code-block:: bash

    python ./src/manage.py setup_configuration --yaml-file /path/to/config.yaml

.. note:: Due to a cache-bug in the underlying framework, you need to restart all
   replicas for part of this change to take effect everywhere.
