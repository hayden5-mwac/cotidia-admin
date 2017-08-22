import importlib

from django import template
from django.template.loader import get_template
from django.apps import apps

register = template.Library()


def can_view_item(context, item):
    """Check permission for a link or sublinks, only return True if allowed."""
    request = context["request"]
    # If there's a url, then we look up the matching permission
    if item.get("url"):
        perms = item.get("permissions", [])
        if perms == []:
            return True
        elif request.user.has_perms(perms):
            return True
    # If it has sub items, then check it can access at least one item
    elif item.get("nav_items"):
        for subitem in item.get("nav_items"):
            return can_view_item(context, subitem)
    return False


def build_permitted_item(context, item):
    """Return permitted links and sublinks."""
    data = {}
    keys = ["text", "icon", "align_right", "url", "permissions"]
    for key in keys:
        if item.get(key):
            data[key] = item.get(key)
    if item.get("nav_items"):
        data["nav_items"] = []
        for subitem in item.get("nav_items"):
            if can_view_item(context, subitem):
                data["nav_items"].append(
                    build_permitted_item(context, subitem)
                )
    return data


def build_permitted_menu(context, menu, permitted_menu):
    """Build a menu with only the permitted links."""
    for item in menu:
        if can_view_item(context, item):
            permitted_menu.append(build_permitted_item(context, item))
    return permitted_menu


@register.simple_tag(takes_context=True)
def menu(context):
    permitted_menu = []

    # For each app, try to find an admin_menu function inside menu.py
    for app in apps.get_app_configs():

        try:
            module = importlib.import_module("{}.menu".format(app.name))
            admin_menu = module.admin_menu
        except (ModuleNotFoundError, AttributeError):
            admin_menu = None

        if admin_menu:
            menu = admin_menu(context)
            permitted_menu = build_permitted_menu(context, menu, permitted_menu)

    context = context.flatten()
    context["menu"] = permitted_menu

    template = get_template('admin/menu/menu.html')
    return template.render(context)