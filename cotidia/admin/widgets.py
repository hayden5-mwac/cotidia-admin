import re
import json
import datetime

from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.dates import MONTHS
from django.forms.widgets import Widget, Select
from django.conf import settings

RE_DATE = re.compile(r"(\d{4})-(\d\d?)-(\d\d?)$")
RE_TIME = re.compile(r"(\d\d?)?:(\d\d?)?$")


class SelectDateWidget(Widget):
    """A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """

    none_value = (0, "---")
    month_field = "%s_month"
    day_field = "%s_day"
    year_field = "%s_year"

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year"
        # select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year - 1
            self.years = range(this_year, this_year + 10)

    def format_time_value(self, value):
        if value < 10:
            return "0%s" % value
        else:
            return "%s" % value

    def render(self, name, value, attrs=None):

        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, str):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        if "id" in self.attrs:
            id_ = self.attrs["id"]
        else:
            id_ = "id_%s" % name

        date_output = []

        #########
        # Day   #
        #########

        day_choices = [(i, i) for i in range(1, 32)]
        if not (self.required and value):
            day_choices.insert(0, (0, "Day"))

        local_attrs = self.build_attrs(self.attrs)

        s = Select(choices=day_choices)
        select_html = s.render(self.day_field % name, day_val, local_attrs)
        date_output.append(select_html)

        #########
        # Month #
        #########

        month_choices = tuple(MONTHS.items())
        if not (self.required and value):
            month_choices = ((0, "Month"),) + month_choices
        local_attrs["id"] = self.month_field % id_

        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        date_output.append(select_html)

        #########
        # Year  #
        #########

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, (0, "Year"))
        local_attrs["id"] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        date_output.append(select_html)

        return mark_safe(
            """<div class="date-select">
            <div class="form__control form__control--select">%s</div>
            <div class="form__control form__control--select">%s</div>
            <div class="form__control form__control--select">%s</div>
            </div>"""
            % (date_output[0], date_output[1], date_output[2])
        )

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None
        if y and m and d:
            return "%s-%s-%s" % (y, m, d)
        return data.get(name, None)


class SelectTimeWidget(Widget):
    """A Widget that splits date input into two <select> boxes."""

    none_value = (0, "---")
    hour_field = "%s_hour"
    minute_field = "%s_minute"

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year"
        # select box.
        self.attrs = attrs or {}
        self.required = required

    def format_time_value(self, value):
        if int(value) < 10:
            return "0%s" % value
        else:
            return "%s" % value

    def render(self, name, value, attrs=None):

        try:
            hour_val, minute_val = value.hour, value.minute
        except AttributeError:
            hour_val = minute_val = None
            if isinstance(value, str):
                match = RE_TIME.match(value)
                if match:
                    hour_val, minute_val = [v for v in match.groups()]

        if "id" in self.attrs:
            id_ = self.attrs["id"]
        else:
            id_ = "id_%s" % name

        time_output = []

        #########
        # Hour #
        #########

        hour_choices = [(i, self.format_time_value(i)) for i in range(0, 24)]
        if not (self.required and value):
            hour_choices.insert(0, ("", "Hour"))
        local_attrs = self.build_attrs(self.attrs)

        s = Select(choices=hour_choices)
        select_html = s.render(self.hour_field % name, str(hour_val), local_attrs)
        time_output.append(select_html)

        ##########
        # Minute #
        ##########

        minute_choices = [(i, self.format_time_value(i)) for i in range(0, 60)]
        if not (self.required and value):
            minute_choices.insert(0, ("", "Mins"))
        local_attrs = self.build_attrs(self.attrs)

        s = Select(choices=minute_choices)
        select_html = s.render(self.minute_field % name, str(minute_val), local_attrs)
        time_output.append(select_html)

        time_output = """<div class="time-select">
            <div class="form__control form__control--select">%s</div>
            <div class="form__control form__control--select">%s</div>
            </div>""" % (
            time_output[0],
            time_output[1],
        )

        return mark_safe("%s" % (time_output))

    def value_from_datadict(self, data, files, name):
        h = data.get(self.hour_field % name)
        minute = data.get(self.minute_field % name)
        if not h and not minute:
            return None
        return "%s:%s" % (self.format_time_value(h), self.format_time_value(minute))


class SelectDateTimeWidget(Widget):
    """A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """

    none_value = (0, "---")
    month_field = "%s_month"
    day_field = "%s_day"
    year_field = "%s_year"

    hour_field = "%s_hour"
    minute_field = "%s_minute"

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year"
        # select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year - 1
            self.years = range(this_year, this_year + 10)

    def format_time_value(self, value):
        if value < 10:
            return "0%s" % value
        else:
            return "%s" % value

    def render(self, name, value, attrs=None):

        try:
            year_val, month_val, day_val, hour_val, minute_val = (
                value.year,
                value.month,
                value.day,
                value.hour,
                value.minute,
            )
        except AttributeError:
            year_val = month_val = day_val = hour_val = minute_val = None
            if isinstance(value, str):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val, hour_val, minute_val = [
                        int(v) for v in match.groups()
                    ]

        if "id" in self.attrs:
            id_ = self.attrs["id"]
        else:
            id_ = "id_%s" % name

        date_output = []
        time_output = []

        #########
        # Day   #
        #########

        day_choices = [(i, i) for i in range(1, 32)]
        if not (self.required and value):
            day_choices.insert(0, (0, "Day"))

        local_attrs = self.build_attrs(self.attrs)

        s = Select(choices=day_choices)
        select_html = s.render(self.day_field % name, day_val, local_attrs)
        date_output.append(select_html)

        #########
        # Month #
        #########

        month_choices = tuple(MONTHS.items())
        if not (self.required and value):
            month_choices = ((0, "Month"),) + month_choices
        local_attrs["id"] = self.month_field % id_

        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        date_output.append(select_html)

        #########
        # Year  #
        #########

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, (0, "Year"))
        local_attrs["id"] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        date_output.append(select_html)

        #########
        # Hour #
        #########

        hour_choices = [(i, self.format_time_value(i)) for i in range(0, 23)]
        if not (self.required and value):
            hour_choices.insert(0, ("", "Hour"))
        local_attrs = self.build_attrs(self.attrs)

        s = Select(choices=hour_choices)
        select_html = s.render(self.hour_field % name, hour_val, local_attrs)
        time_output.append(select_html)

        ##########
        # Minute #
        ##########

        minute_choices = [(i, self.format_time_value(i)) for i in range(0, 59)]
        if not (self.required and value):
            minute_choices.insert(0, ("", "Minute"))
        local_attrs = self.build_attrs(self.attrs)

        s = Select(choices=minute_choices)
        select_html = s.render(self.minute_field % name, minute_val, local_attrs)
        time_output.append(select_html)

        date_output = """<div class="date-select">
            <div class="form__control form__control--select">%s</div>
            <div class="form__control form__control--select">%s</div>
            <div class="form__control form__control--select">%s</div>
            </div>""" % (
            date_output[0],
            date_output[1],
            date_output[2],
        )

        time_output = """<div class="time-select">
            <div class="form__control form__control--select">%s</div>
            <div class="form__control form__control--select">%s</div>
            </div>""" % (
            time_output[0],
            time_output[1],
        )

        return mark_safe("%s%s" % (date_output, time_output))

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        h = data.get(self.hour_field % name)
        minute = data.get(self.minute_field % name)
        if y == m == d == h == minute == "0":
            return None
        if y and m and d and h and minute:
            return "%s-%s-%s %s:%s" % (y, m, d, int(h), int(minute))
        return data.get(name, None)


class TrixEditor(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):

        if attrs is None:
            attrs = {}
        attrs.update({"style": "visibility: hidden; position: absolute;"})

        params = {
            "input": attrs.get("id") or "{}_id".format(name),
            "class": "trix-content",
        }
        param_str = " ".join('{}="{}"'.format(k, v) for k, v in params.items())

        html = super(TrixEditor, self).render(name, value, attrs)
        html = format_html(
            '{}<div style="flex-grow: 1; margin-top: 2rem;"><trix-editor {}></trix-editor></div>',
            html,
            mark_safe(param_str),
        )
        return html

    class Media:
        css = {"all": ("trix/trix.css",)}
        js = ("trix/trix.js",)


class DateInput(forms.DateInput):
    input_type = "date"


class TimeInput(forms.TimeInput):
    input_type = "time"


class RadioButtonSelect(forms.RadioSelect):
    template_name = "widgets/radio_button.html"
    option_template_name = "widgets/radio_option_button.html"


class SlugInput(forms.TextInput):
    class Media:
        js = ("js/slug.js",)


class GeolocateInput(forms.TextInput):
    def render(self, name, value, attrs=None):

        if attrs is None:
            attrs = {}
        attrs.update(
            {
                "data-geolocate": True,
                "data-latitude-field": attrs.get("data-latitude-field", "id_lat"),
                "data-longitude-field": attrs.get("data-longitude-field", "id_lng"),
            }
        )

        html = super().render(name, value, attrs)
        return html

    class Media:
        js = (
            "https://maps.google.com/maps/api/js?key={}".format(
                getattr(settings, "GOOGLE_MAP_API_KEY", "")
            ),
            "js/geolocate.js",
        )


class SelectSingleLookup(forms.HiddenInput):
    template_name = "admin/widgets/select_single_lookup.html"
    queryset_lookup = "pk"

    def __init__(self, config=None, queryset_lookup="pk", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.queryset_lookup = queryset_lookup

    def get_endpoint(self):
        if self.config.get("endpoint"):
            endpoint = self.config["endpoint"]
        else:
            endpoint = reverse(
                "generic-api:multiple-select-lookup",
                kwargs={
                    "app_label": self.config["app_label"],
                    "model_name": self.config["model_name"],
                },
            )
        return endpoint

    def get_initial_data(self, value):
        if "queryset" in self.config:
            instance = self.config["queryset"].get(**{self.queryset_lookup: value})
            initial_data = [
                {
                    "value": str(getattr(instance, self.queryset_lookup)),
                    "label": str(instance),
                }
            ]
        else:
            initial_data = [
                {"value": c[0], "label": c[1]} for c in self.choices if c[0] == value
            ]

        return initial_data

    def get_context(self, name, value, attrs):
        if value:
            initial_data = self.get_initial_data(value)
        else:
            initial_data = []

        context = super().get_context(name, value, attrs)
        context["config"] = {
            "data-widget": "typeahead-select",
            "data-multiple": False,
            "data-label": self.config.get("label", False),
            "data-name": name,
            "data-typeahead-endpoint": self.get_endpoint(),
            "data-typeahead-minchars": "3",
            "data-initial": json.dumps(initial_data),
            "data-placeholder": self.config["placeholder"],
            "data-id": "id_{}".format(name),
        }
        return context


class SelectMultipleLookup(forms.MultipleHiddenInput):
    template_name = "admin/widgets/select_multiple_lookup.html"
    queryset_lookup = "pk"

    def __init__(self, config=None, queryset_lookup="pk", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.queryset_lookup = queryset_lookup

    def get_endpoint(self):
        if self.config.get("endpoint"):
            endpoint = (
                self.config["endpoint"]
                + "?country=d2dba710-bf66-4d7e-a490-e92875618857"
            )
        else:
            endpoint = reverse(
                "generic-api:multiple-select-lookup",
                kwargs={
                    "app_label": self.config["app_label"],
                    "model_name": self.config["model_name"],
                },
            )
        return endpoint

    def get_initial_data(self, value):
        if self.config.get("queryset"):
            queryset = self.config["queryset"].filter(
                **{f"{self.queryset_lookup}__in": value}
            )
            initial_data = [
                {
                    "value": getattr(instance, self.queryset_lookup),
                    "label": str(instance),
                }
                for instance in queryset
            ]
        else:
            initial_data = [
                {"value": c[0], "label": c[1]} for c in self.choices if c[0] in value
            ]

        return initial_data

    def get_context(self, name, value, attrs):
        if value:
            initial_data = self.get_initial_data(value)
        else:
            initial_data = []

        context = super().get_context(name, value, attrs)
        context["config"] = {
            "data-widget": "typeahead-select",
            "data-multiple": True,
            "data-label": self.config.get("label", False),
            "data-name": name,
            "data-typeahead-endpoint": self.get_endpoint,
            "data-typeahead-minchars": "3",
            "data-initial": json.dumps(initial_data),
            "data-placeholder": self.config["placeholder"],
            "data-id": "id_{}".format(name),
        }
        return context
