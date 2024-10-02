from django import template

from decouple import Undefined

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


@register.simple_tag
def config_var_description(variable, details):

    var_details = details.get(variable)
    if var_details:
        return var_details.get("description", "No description provided")

    return "No description provided"
