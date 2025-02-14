from django.contrib import admin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export.admin import ImportExportMixin

from apps.core.models import GroupCore, User

admin.site.unregister(Group)


@admin.register(GroupCore)
class GroupCoreAdmin(ImportExportMixin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(User)
class UserAdmin(ImportExportMixin, ModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
