from django import template

register = template.Library()


@register.filter()
def get_attr(obj, column):

    # If the column is a display function, call it with the object as first
    # argument
    if callable(column):
        return column(obj)

    attr = None

    if obj:
        attrs = column.split(".")
        attr = getattr(obj, attrs.pop(0))
        for a in attrs:
            attr = getattr(attr, a)

    # If the object attribute is a method, call it

    if callable(attr):
        if attr.__class__.__name__ == "ManyRelatedManager":
            return attr.all()

        return attr()

    return attr


@register.filter()
def get_value_type(value):
    return value.__class__.__name__
