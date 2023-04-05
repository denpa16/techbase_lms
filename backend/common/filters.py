import math

from django import forms
from django.core.exceptions import FieldError
from django.db.models import F, Max, Min
from django.db.models.functions import Greatest, Least, Lower, Upper
from django_filters.rest_framework import (
    BaseInFilter,
    BaseRangeFilter,
    BooleanFilter,
    CharFilter,
    ChoiceFilter,
    Filter,
    FilterSet,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
    MultipleChoiceFilter,
    NumberFilter,
    OrderingFilter,
    RangeFilter,
)

from .utils import ceil, floor


class FloatFilter(Filter):
    field_class = forms.FloatField


class IntegerFilter(Filter):
    field_class = forms.IntegerField


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class NumberRangeFilter(BaseRangeFilter, NumberFilter):
    pass


class CharInFilter(BaseInFilter, CharFilter):
    pass


# noinspection PyProtectedMember
class FacetFilterSet(FilterSet):
    def facets(self):
        # Инициализируем список фасетов
        facets = []
        #  Сохраняем изначальный список фильтры
        backup_filters = self.filters
        # Проверяем валидность введённых данных в фильтре
        self.is_valid()
        # Сохраняем параметры фильтрации
        backup_cleaned_data = self.form.cleaned_data

        # Пробегаемся по всем фильтрам
        for filter_name, _filter in self.filters.items():
            # Востанавливаем изначальные фильтры
            self.filters = backup_filters.copy()
            # Востанавливаем изначальные данные фильтрации
            self.form.cleaned_data = backup_cleaned_data.copy()

            # Убираем фильтр, если он не важен или не участвует в фильтре
            filter_pop = getattr(_filter, "pop") if hasattr(_filter, "pop") else True
            if filter_pop:
                self.filters.pop(filter_name)
                self.form.cleaned_data.pop(filter_name)

            # Обновляем существующий набор данных. Т.е. удаляем уже отфильтрованный набор данных.
            if hasattr(self, "_qs"):
                delattr(self, "_qs")

            # Если есть кастомное поведение фасетов, то вызываем кастомную функцию
            if hasattr(_filter, "aggregate_method"):
                method = getattr(_filter, "aggregate_method")
                # Добавляем в фасеты наименование фильтра, и полученные данные
                facets.append({"name": filter_name, "choices": getattr(self, method)(self.qs)})
            elif hasattr(_filter, "range_aggregate_method"):
                method = getattr(_filter, "range_aggregate_method")
                facets.append({"name": filter_name, "range": getattr(self, method)(self.qs)})
            # Если есть параметр пропуска, то пропускаем генерацию фасетов
            elif getattr(_filter, "skip", False):
                continue
            # Если параметр очередность, то пропускаем
            elif isinstance(_filter, OrderingFilter):
                continue
            # Если фильтр относиться к Булевому или Choice фильтрам, то вызываем дефолтную генерацию фасетов
            elif isinstance(
                _filter,
                (
                    BooleanFilter,
                    ChoiceFilter,
                    MultipleChoiceFilter,
                    ModelChoiceFilter,
                    ModelMultipleChoiceFilter,
                    BaseInFilter,
                ),
            ):
                # Вытаскиваем из набора данных, все возможные варианты фильтра
                choices = (
                    self.qs.filter(**{f"{_filter.field_name}__isnull": False})
                    .order_by(_filter.field_name)
                    .values_list(_filter.field_name, flat=True)
                    .distinct()
                )
                facets.append({"name": filter_name, "choices": list(choices)})
            # Если фильтр относиться к NumberFilter, то вызываем дефолтную генерацию фасетов
            elif isinstance(_filter, NumberFilter) and _filter.lookup_expr == "exact":
                # Вытаскиваем из набора данных, все возможные варианты фильтра
                choices = self.qs.dates(field_name=_filter.field_name, kind=_filter.lookup_expr)
                facets.append(
                    {
                        "name": filter_name,
                        "choices": [getattr(x, _filter.lookup_expr) for x in choices],
                    }
                )
            # Если фильтр относиться к RangeFilter, то вызываем дефолтную генерацию фасетов
            elif isinstance(_filter, (RangeFilter, BaseRangeFilter, NumberFilter)):
                # Вытаскиваем из набора данных, все возможные максимальные или минимальные наборы фильтров
                ranges = self.qs.aggregate(min=Min(_filter.field_name), max=Max(_filter.field_name))
                facets.append(
                    {
                        "name": filter_name,
                        "range": {"min": floor(ranges["min"]), "max": ceil(ranges["max"])},
                    }
                )
            # Если фильтр относиться к RangeFilter, то вызываем дефолтную генерацию фасетов
            elif isinstance(_filter, Filter) and _filter.lookup_expr == "contains":
                # Вытаскиваем из набора данных, все возможные максимальные или минимальные наборы фильтров
                bounds = self.qs.aggregate(
                    min=Least(Min(Lower(_filter.field_name)), Min(Upper(_filter.field_name))),
                    max=Greatest(Max(Lower(_filter.field_name)), Max(Upper(_filter.field_name))),
                )
                facets.append(
                    {
                        "name": filter_name,
                        "range": {
                            "min": None if bounds["min"] is None else math.ceil(bounds["min"]),
                            "max": None if bounds["max"] is None else math.floor(bounds["max"]),
                        },
                    }
                )
        # Востанавливаем исходные фильтры
        self.filters = backup_filters
        # Востанавливаем исходные параметры фильтров
        self.form.cleaned_data = backup_cleaned_data
        # Возвращание данные фасетов и количество объектов
        return {"facets": facets, "count": self.qs.count()}

    def specs(self):
        # Инициализируем список спеков
        specs = []
        #  Сохраняем изначальный список фильтров
        backup_filters = self.filters
        # Проверяем валидность введённых данных в фильтре
        self.is_valid()
        # Сохраняем параметры фильтрации
        backup_cleaned_data = self.form.cleaned_data

        # Пробегаемся по всем фильтрам
        for filter_name, _filter in self.filters.items():
            # Востанавливаем изначальные фильтры
            self.filters = backup_filters.copy()
            # Востанавливаем изначальные данные фильтрации
            self.form.cleaned_data = backup_cleaned_data.copy()
            # Если есть кастомное поведение спеков, то вызываем кастомную функцию
            if hasattr(_filter, "specs"):
                method = getattr(_filter, "specs")
                # Добавляем в фасеты наименование фильтра, и полученные данные
                specs.append({"name": filter_name, "choices": getattr(self, method)(self.queryset)})
            elif hasattr(_filter, "range_specs"):
                method = getattr(_filter, "range_specs")
                specs.append({"name": filter_name, "range": getattr(self, method)(self.queryset)})
            # Если параметр очередность, то пропускаем
            elif isinstance(_filter, OrderingFilter):
                continue
            # Если фильтр относиться к Булевому или Choice фильтрам, то вызываем дефолтную генерацию фасетов
            elif isinstance(
                _filter,
                (
                    BaseInFilter,
                    ChoiceFilter,
                    MultipleChoiceFilter,
                    ModelChoiceFilter,
                    ModelMultipleChoiceFilter,
                ),
            ):
                # Стандартная функция получения спеков для Choices
                def get_choices(field_name):
                    # Стандартная сортировка
                    order_by = (f"{_filter.field_name}__{field_name}",)
                    if isinstance(_filter, (ModelChoiceFilter, ModelMultipleChoiceFilter)):
                        model_ordering = _filter.queryset.model._meta.ordering
                        order_by = []
                        for o in model_ordering:
                            if o[0] == "-":
                                order_by.append(f"-{_filter.field_name}__{o[1:]}")
                            else:
                                order_by.append(f"{_filter.field_name}__{o}")

                    return (
                        self.queryset.filter(**{f"{_filter.field_name}__isnull": False})
                        .order_by(*order_by)
                        .values(
                            value=F(f"{_filter.field_name}__pk"),
                            label=F(f"{_filter.field_name}__{field_name}"),
                        )
                        .distinct()
                    )

                choices = ()
                try:
                    choices = get_choices("name")
                except FieldError:
                    try:
                        choices = get_choices("number")
                    except FieldError:
                        pass
                specs.append({"name": filter_name, "choices": choices})
            # Если фильтр относиться к RangeFilter, то вызываем дефолтную генерацию спеков
            elif isinstance(_filter, (RangeFilter, BaseRangeFilter, NumberFilter)):
                # Получаем все воможные параметры
                choices = (
                    self.queryset.values_list(_filter.field_name, flat=True).order_by().distinct()
                )
                specs.append(
                    {
                        "name": filter_name,
                        "ranges": {
                            "min": floor(min(choices) if choices else None),
                            "max": ceil(max(choices) if choices else None),
                        },
                    }
                )
            elif isinstance(_filter, Filter) and _filter.lookup_expr == "contains":
                bounds = self.queryset.aggregate(
                    min=Least(Min(Lower(_filter.field_name)), Min(Upper(_filter.field_name))),
                    max=Greatest(Max(Lower(_filter.field_name)), Max(Upper(_filter.field_name))),
                )
                specs.append(
                    {
                        "name": filter_name,
                        "range": {
                            "min": None if bounds["min"] is None else math.ceil(bounds["min"]),
                            "max": None if bounds["max"] is None else math.floor(bounds["max"]),
                        },
                    }
                )
        # Востанавливаем исходные фильтры
        self.filters = backup_filters
        # Востанавливаем исходные параметры фильтров
        self.form.cleaned_data = backup_cleaned_data
        # Возвращание данные спеков и количество объектов
        return specs
