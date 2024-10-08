{% load doc_tags %}
{% spaceless %}
{{ title }}

Enable/Disable configuration:
"""""""""""""""""""""""""""""

::

    {{ enable_setting }}

{% if required_settings %}
Required settings
"""""""""""""""""
{% for setting in required_settings %}
* ``{{ setting }}``: {% config_var_description setting detailed_info %}
{% endfor %}{% endif %}

{% if optional_settings %}
Optional Settings
"""""""""""""""""
{% for setting in optional_settings %}
* ``{{ setting }}``: {% config_var_description setting detailed_info %}
{% endfor %}{% endif %}

{% endspaceless %}
