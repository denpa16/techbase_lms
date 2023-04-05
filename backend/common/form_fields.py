from django import forms
from django.contrib.postgres.forms import BaseRangeField
from django.core.exceptions import ValidationError
from django.forms import CharField, MultiValueField
from psycopg2.extras import NumericRange

from .widgets import PolygonWidget, PpoiWidget


class PolygonFormField(MultiValueField):
    widget = PolygonWidget

    default_error_messages = {"invalid": "Значение должно быть двумя числами, разделенными запятой"}

    def __init__(self, **kwargs):
        fields = (CharField(),)
        super().__init__(fields, **kwargs)

    def compress(self, data_list):
        return data_list


class PpoiFormField(MultiValueField):
    widget = PpoiWidget

    default_error_messages = {"invalid": "Значение должно быть двумя числами, разделенными запятой"}

    def __init__(self, **kwargs):
        fields = (CharField(required=False), CharField(required=False))
        super().__init__(fields, require_all_fields=False, **kwargs)

    def compress(self, data_list):
        return data_list

    def validate(self, value):
        super().validate(value)
        if value[0] == "" or value is None:
            return
        parts = value[0].split(",")
        if not len(parts) == 2:
            raise ValidationError(self.error_messages["invalid"], code="invalid")
        try:
            float(parts[0])
            float(parts[1])
        except ValueError:
            raise ValidationError(self.error_messages["invalid"], code="invalid")


class InclusiveNumericRange(NumericRange):
    def __init__(self, lower=None, upper=None, bounds="[]", empty=False):
        super().__init__(lower, upper, bounds, empty)


class FloatRangeFormField(BaseRangeField):
    range_type = InclusiveNumericRange
    base_field = forms.FloatField


class IntegerRangeFormField(BaseRangeField):
    range_type = InclusiveNumericRange
    base_field = forms.IntegerField
