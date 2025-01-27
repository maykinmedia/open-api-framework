from django import template

from decouple import Undefined

from open_api_framework.utils import get_configuraton_step_context

register = template.Library()


@register.filter(name="repeat_char")
def repeat_char(value, char="-"):
    try:
        length = len(value)
        return char * length
    except TypeError:
        return ""


@register.filter(name="is_undefined")
def is_undefined(value):
    return isinstance(value, Undefined)


@register.filter(name="to_str")
def to_str(value):
    if value == "":
        return "(empty string)"
    return str(value)


@register.filter(name="ensure_endswith")
def ensure_endswith(value, char):
    if not isinstance(value, str):
        value = str(value)
    if not value.endswith(char):
        value += char
    return value


@register.inclusion_tag("open_api_framework/components/setup_config_step.rst")
def render_setup_configuraiton_step(step_path):
    return get_configuraton_step_context(step_path)
