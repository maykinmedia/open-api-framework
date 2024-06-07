{% load doc_tags %}.. _installation_env_config:

===================================
Environment configuration reference
===================================

{% block intro %}{% endblock %}

Available environment variables
===============================

{% for group_name, vars in vars %}
{{group_name}}
{{group_name|repeat_char:"="}}

{% for var in vars %}* ``{{var.name}}``: {% if var.help_text %}{{var.help_text|safe|ensure_endswith:"."}}{% endif %}{% if not var.default|is_undefined %} Defaults to: ``{{var.default|to_str}}``{% endif %}
{% endfor %}
{% endfor %}
