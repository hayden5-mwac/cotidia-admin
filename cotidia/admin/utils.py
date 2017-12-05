from cotidia.account.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.db.models.fields import (
        UUIDField,
        DateTimeField,
        DateField,
        CharField,
        IntegerField,
        BooleanField,
        AutoField,
        TextField,
        )

SUPPORTED_FIELD_TYPES = [
        UUIDField,
        DateTimeField,
        DateField,
        CharField,
        IntegerField,
        BooleanField,
        AutoField,
        TextField,
        ]
FIELD_MAPPING = {
        DateTimeField: (lambda: {
            "display": "datetime",
            "filter": "date"
            }),
        UUIDField: (lambda: {
            "display": "verbatim",
            "filter": "text"
            }),
        DateField: (lambda: {
            "display": "date",
            "filter": "date"
            }),
        CharField: (lambda: {
            "display": "verbatim",
            "filter": "text"
            }),
        IntegerField: (lambda: {
            "display": "verbatim",
            "filter": "number"
            }),
        BooleanField: (lambda: {
            "display": "boolean",
            "filter": "boolean"
            }),
        TextField: (lambda: {
            "display": "verbatim",
            "filter": "text"
            }),
        AutoField: (lambda: {
            "display": "verbatim",
            "filter": "number"
            }),
        }


class UserCheckMixin(object):

    def check_user(self, user):
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            if request.user.is_authenticated():
                raise PermissionDenied
            else:
                return redirect(settings.ACCOUNT_ADMIN_LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)


class StaffPermissionRequiredMixin(UserCheckMixin):

    def get_permission_required(self):
        if hasattr(self, "permission_required"):
            return self.permission_required
        return None

    def check_user(self, user):
        """Check if the user has the relevant permissions."""
        if user.is_superuser:
            return True
        return user.is_staff and user.has_perm(self.get_permission_required())


def get_field_representation(field, model):
    """ Creates a dict object for a given field using field mapping above
        Fields not in (or a subclass of) elements in the SUPPORTED_FIELD_TYPES
        list will return as "None"
    """
    # Gets the first element that the field is an instance of The list is
    # sorted so the most specific classes are checked first using mro()
    sorted_types = sorted(SUPPORTED_FIELD_TYPES, key=lambda x: len(x.mro()))
    type = next(
            iter([t for t in sorted_types if isinstance(field, t)]),
            None)

    if type is None:
        return None
    # Gets the base representation for the given field type
    field_representation = FIELD_MAPPING[type]()
    field_representation['label'] = field.name
    if field.choices:
        field_representation['filter'] = 'choice'
        field_representation['options'] = field.choices

    # Checks if the developer has defined the field manually in the model
    try:
        if field.name in model.__meta__.field_representation:
            user_defined_representation = model.__meta__.field_representation[field.name]
            for key in user_defined_representation:
                field_representation[key] = user_defined_representation[key]
    except (KeyError, AttributeError):
        pass
    return field_representation


def get_fields_from_model(model):
    fields_representation = {}
    fields = model._meta.get_fields()
    for f in fields:
        field_representation = get_field_representation(f, model)
        if field_representation is not None:
            fields_representation[f.name] = field_representation
        else:
            print("Field not supported: %s" % f.get_internal_type())

    return fields_representation


def get_model_default_columns(model):
    fields = []
    try:
        fields = model.__meta__.default_fields
    except (AttributeError):
        fields = [f for f in get_fields_from_model(model).keys()]
    return fields


def get_model_structure(
        model,
        endpoint=None,
        detail_endpoint=None,
        token=None
        ):
    structure = {
            "columns": get_fields_from_model(model),
            "default_columns": get_model_default_columns(model),
            }
    if endpoint is not None:
        structure['endpoint'] = endpoint
    if detail_endpoint is not None:
        structure['detail_endpoint'] = detail_endpoint
    if token is not None:
        structure['token'] = token

    return structure
