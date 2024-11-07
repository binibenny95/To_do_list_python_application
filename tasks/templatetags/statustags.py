from django import template
register = template.Library()

@register.filter()
def status_css_class(value):
    status = {
        "Completed": "badge-success",
        "In Progress": "badge-warning",
        "On Hold" : "badge-info",
    }
    try:
        return status[value]
    except KeyError:
        return "badge-info"

@register.filter()
def priority_css_class(value):
    priority = {
        "High": "badge-success",
        "low": "badge-warning",
        "medium" : "badge-info",
    }
    try:
        return priority[value]
    except KeyError:
        return "badge-info"