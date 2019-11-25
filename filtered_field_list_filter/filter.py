from django.contrib import admin
from django.contrib.admin.utils import prepare_lookup_value


def filtered_field_list_filter(*fields: str):
    class FilteredFieldListFilter(admin.RelatedFieldListFilter):
        def field_choices(self, field, request, model_admin):
            filtered_field = self.field_path
            limit_choices_to = {
                param.replace(f"{filtered_field}__", "", 1): prepare_lookup_value(
                    param, value
                )
                for (param, value) in request.GET.items()
                if any(
                    param.startswith(f"{filtered_field}__{field}") for field in fields
                )
            }
            return field.get_choices(
                include_blank=False, limit_choices_to=limit_choices_to
            )

    return FilteredFieldListFilter
