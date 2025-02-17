from typing import Any, Dict, List, Optional, Tuple, Type
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.views.main import ChangeList
from django.core.validators import EMPTY_VALUES
from django.db.models import Max, Min, Model, QuerySet
from django.http import HttpRequest
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import (
    TextFilter, FieldTextFilter, RangeDateFilter, ChoicesDropdownFilter, RelatedDropdownFilter
)
from datetime import datetime

from apps.core.forms import (
    DropdownForm,
    SearchForm,
)


class ValueMixin:
    def value(self) -> Optional[str]:
        return (
            self.lookup_val[0]
            if self.lookup_val not in EMPTY_VALUES
            and isinstance(self.lookup_val, List)
            and len(self.lookup_val) > 0
            else self.lookup_val
        )


class DropdownMixin:
    template = "core/filters/filters_field.html"
    form_class = DropdownForm
    all_option = ["", _("All")]

    def queryset(self, request, queryset) -> QuerySet:
        if self.value() not in EMPTY_VALUES:
            return super().queryset(request, queryset)

        return queryset


class TextFilter(admin.SimpleListFilter):
    template = "core/filters/filters_field.html"
    form_class = SearchForm

    def has_output(self) -> bool:
        return True

    def lookups(self, request: HttpRequest, model_admin: ModelAdmin) -> Tuple:
        return ()

    def choices(self, changelist: ChangeList) -> Tuple[Dict[str, Any], ...]:
        return (
            {
                "form": self.form_class(
                    name=self.parameter_name,
                    label=_("By {}").format(self.title.title()),
                    data={self.parameter_name: self.value()},
                ),
            },
        )


class FieldTextFilter(FieldTextFilter):
    template = "core/filters/filters_field.html"
    # form_class = SearchForm

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = f"{field_path}__icontains"
        self.lookup_val = params.get(self.lookup_kwarg)
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self) -> List[str]:
        return [self.lookup_kwarg]

    def choices(self, changelist: ChangeList) -> Tuple[Dict[str, Any], ...]:
        return (
            {
                "form": self.form_class(
                    label=_("By {}").format(self.title.title()),
                    name=self.lookup_kwarg,
                    data={self.lookup_kwarg: self.value()},
                ),
            },
        )


class DropdownFilter(admin.SimpleListFilter):
    template = "core/filters/filters_field.html"
    form_class = DropdownForm
    all_option = ["", _("All")]

    def choices(self, changelist: ChangeList) -> Tuple[Dict[str, Any], ...]:
        return (
            {
                "form": self.form_class(
                    label=_("By {}").format(self.title.title()),
                    name=self.parameter_name,
                    choices=[self.all_option, *self.lookup_choices],
                    data={self.parameter_name: self.value()},
                ),
            },
        )


class ChoicesDropdownFilter(ChoicesDropdownFilter):
    def choices(self, changelist: ChangeList):
        choices = [self.all_option, *self.field.flatchoices]

        yield {
            "form": self.form_class(
                label=_("By {}").format(self.title.title()),
                name=self.lookup_kwarg,
                choices=choices,
                data={self.lookup_kwarg: self.value()},
            ),
        }


class RelatedDropdownFilter(RelatedDropdownFilter):
    def choices(self, changelist: ChangeList):
        yield {
            "form": self.form_class(
                label=_("By {}").format(self.title.title()),
                name=self.lookup_kwarg,
                choices=[self.all_option, *self.lookup_choices],
                data={self.lookup_kwarg: self.value()},
            ),
        }


class CustomRangeDateFilter(RangeDateFilter):
    template = "core/filters/filters_date_range.html"

    def queryset(self, request, queryset) -> QuerySet:
        filters = {}

        value_from = self.used_parameters.get(self.parameter_name + "_from", None)
        if value_from not in EMPTY_VALUES:
            filters.update(
                {
                    self.parameter_name + "__gte": datetime.strptime(
                        value_from, '%d/%m/%Y'
                    ).strftime('%Y-%m-%d 00:00:00'),
                }
            )

        value_to = self.used_parameters.get(self.parameter_name + "_to", None)
        if value_to not in EMPTY_VALUES:
            filters.update(
                {
                    self.parameter_name + "__lte": datetime.strptime(
                        value_to, '%d/%m/%Y'
                    ).strftime('%Y-%m-%d 00:00:00'),
                }
            )

        try:
            return queryset.filter(**filters)
        except (ValueError, ValidationError) as e:
            return None
