from django.contrib.admin import SimpleListFilter, site
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.forms import ModelChoiceField
from django_admin_listfilter_dropdown.filters import SimpleDropdownFilter


class ChaindedRelatedDropdownFilter(SimpleDropdownFilter):

    lookup = None
    parent_parameters = None
    child_parameters = None
    model = None
    value_field = "id"
    title_field = "name"

    # noinspection PyProtectedMember
    def lookups(self, request, model_admin):
        related_admin = model_admin.admin_site._registry.get(self.model)
        if not related_admin:
            related_admin = site._registry.get(self.model)
        queryset = related_admin.get_queryset(request)
        if self.parent_parameters:
            for parent_parameter in self.parent_parameters:
                if parent_parameter[0] in request.GET:
                    lookups = {parent_parameter[1]: request.GET[parent_parameter[0]]}
                    queryset = queryset.filter(**lookups)
        return queryset.distinct().values_list(self.value_field, self.title_field)

    # noinspection PyUnusedLocal
    def queryset(self, request, queryset):
        value = self.value()
        lookup = self.lookup
        if not lookup:
            lookup = self.parameter_name
        if value:
            return queryset.filter(**{lookup: self.value()})
        return None

    def choices(self, changelist):
        remove_params = list(self.child_parameters) if self.child_parameters else []
        remove_params += [self.parameter_name]
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string({}, remove_params),
            "display": "All",
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}, self.child_parameters
                ),
                "display": title,
            }


class ChainedListFilter(SimpleListFilter):
    """Фильтр чьи варианты значений фильтруются на основе другого фильтра"""

    lookup = None
    parent_parameters = None
    child_parameters = None
    model = None
    value_field = "id"
    title_field = "name"

    # noinspection PyProtectedMember
    def lookups(self, request, model_admin):
        related_admin = model_admin.admin_site._registry.get(self.model)
        if not related_admin:
            related_admin = site._registry.get(self.model)
        queryset = related_admin.get_queryset(request)
        if self.parent_parameters:
            for parent_parameter in self.parent_parameters:
                if parent_parameter[0] in request.GET:
                    lookups = {parent_parameter[1]: request.GET[parent_parameter[0]]}
                    queryset = queryset.filter(**lookups)
        return queryset.distinct().values_list(self.value_field, self.title_field)

    # noinspection PyUnusedLocal
    def queryset(self, request, queryset):
        value = self.value()
        lookup = self.lookup
        if not lookup:
            lookup = self.parameter_name
        if value:
            return queryset.filter(**{lookup: self.value()})
        return None

    def choices(self, changelist):
        remove_params = list(self.child_parameters) if self.child_parameters else []
        remove_params += [self.parameter_name]
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string({}, remove_params),
            "display": "All",
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}, self.child_parameters
                ),
                "display": title,
            }


# noinspection PyUnresolvedReferences
class DeclaredFirstAdminMixin:
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        for field in reversed(form.declared_fields.keys()):
            form.base_fields.move_to_end(field, last=False)
        return form


# noinspection PyProtectedMember, PyUnresolvedReferences
class WrapRelatedAdminMixin:
    def _wrap_related_field(self, name, field, model, request):
        """Оборачивает виджет внешнего ключа в RelatedFieldWidgetWrapper чтобы у него появились
        кнопки с действиями: добавить, изменить, удалить"""
        if isinstance(field.widget, RelatedFieldWidgetWrapper):
            return
        rel = model._meta.get_field(name).remote_field
        rel_admin = self.admin_site._registry.get(model)
        can_change_related = (rel_admin.has_change_permission(request),)
        can_delete_related = (rel_admin.has_delete_permission(request),)
        can_view_related = (rel_admin.has_view_permission(request),)
        field.widget = RelatedFieldWidgetWrapper(
            field.widget,
            rel,
            self.admin_site,
            can_change_related=can_change_related,
            can_delete_related=can_delete_related,
            can_view_related=can_view_related,
        )

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Добавляем в форму CRUD кнопки для полей выбора внешних ключей"""
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        model_field_names = [field.name for field in self.model._meta.fields]
        for field_name, field in form.base_fields.items():
            if isinstance(field, ModelChoiceField) and field_name in model_field_names:
                self._wrap_related_field(field_name, field, self.model, request)
        return form
