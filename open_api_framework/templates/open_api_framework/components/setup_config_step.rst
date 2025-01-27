{% load doc_tags %}
{% spaceless %}
{{ step_title }}
{{ step_title|repeat_char:"-"}}

{{ step_description }}

.. setup-config-example:: {{ step_path }}
{% endspaceless %}
