from django import template
register = template.Library()

@register.filter()
def status_css_class(value):
    normalized_value = str(value).strip().title()
    status = {
        "Completed": "badge-success",
        'In Progress': "badge-warning",
        "On Hold": "badge-info",
    }
    return status.get(normalized_value, "badge-info")

@register.filter()
def priority_css_class(value):
    normalized_value = str(value).strip().title()
    priority = {
        "High": "badge-high ",
        "Low": "badge-medium",
        "Medium": "badge-low",
    }
    return priority.get(normalized_value, "badge-low")
