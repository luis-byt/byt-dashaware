from django.contrib import admin
from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib import messages
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.decorators import action
from import_export.admin import ImportExportMixin, ExportMixin

from apps.base.models import (
    Patient, Note
)
from apps.core.admin_filters import (
    FieldTextFilter, ChoicesDropdownFilter, CustomRangeDateFilter
)
from apps.base.admin_filters import (
    FullNameFilter, PatientFullNameFilter, ReasonFilter, PatientReasonFilter
)
from apps.base.resources import PatientExportResource, NoteExportResource
from apps.base.utils import sync_up_patients, sync_up_notes


class NoteInLine(TabularInline):
    model = Note
    fields = ['id', 'date_joined', 'description']
    readonly_fields = ('id', 'date_joined', 'description')
    min_num = 0
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Patient)
class PatientAdmin(ImportExportMixin, ModelAdmin):
    list_display = (
        'get_id', 'full_name', 'get_phones', 'email', 'get_birthdate',
        'gender', 'referred_by', 'get_date_joined', 'get_modified_date'
    )
    list_filter_submit = True
    list_filter = (
        FullNameFilter,
        ("gender", ChoicesDropdownFilter),
        ("date_joined", CustomRangeDateFilter),
        ("modified_date", CustomRangeDateFilter),
        PatientReasonFilter,
    )
    inlines = [NoteInLine]
    actions = ['export']

    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_class = PatientExportResource

    def export(self, request, queryset):
        appointment_resource = PatientExportResource()
        dataset = appointment_resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(_('Patients'))
        return response

    export.short_description = _('Export selected %(verbose_name_plural)s')

    actions_list = ["changelist_global_action_sync_up"]

    @action(description=_("Sync up"))
    def changelist_global_action_sync_up(self, request: HttpRequest):
        sync_up_patients()
        messages.success(request, _('Patients synced correctly.'))
        return redirect("/base/patient/")

    def get_id(self, instance):
        return '{0}...{1}'.format(instance.id[:10], instance.id[-10:])

    get_id.short_description = _('ID')
    get_id.allow_tags = True

    def full_name(self, instance):
        # url = reverse("admin:base_patient_change", args=[instance.id])
        # return format_html(
        #     '<a href="{}" style="font-weight: bold; color: #c084fc;">{}</a>',
        #     url, instance.get_full_name()
        # )
        return instance.get_full_name()

    full_name.short_description = _('full name')

    def get_phones(self, instance):
        if len(instance.get_phones()) > 0:
            return " | ".join(instance.get_phones())
        return "-"

    get_phones.short_description = _('phones')
    get_phones.allow_tags = True

    def get_birthdate(self, instance):
        return instance.birthdate.strftime('%d/%m/%Y') if instance.birthdate else None

    get_birthdate.short_description = _('birthdate')
    get_birthdate.allow_tags = True

    def get_date_joined(self, instance):
        return instance.date_joined.strftime('%d/%m/%Y') if instance.date_joined else None

    get_date_joined.short_description = _('date joined')
    get_date_joined.allow_tags = True

    def get_modified_date(self, instance):
        return instance.modified_date.strftime('%d/%m/%Y') if instance.modified_date else None

    get_modified_date.short_description = _('modified date')
    get_modified_date.allow_tags = True


@admin.register(Note)
class NoteAdmin(ImportExportMixin, ModelAdmin):
    list_display = (
        'get_id', 'patient_link', 'reason', 'description', 'get_date_joined', 'get_modified_date'
    )
    list_filter_submit = True
    list_filter = (
        PatientFullNameFilter,
        ReasonFilter,
        ("date_joined", CustomRangeDateFilter),
        ("modified_date", CustomRangeDateFilter),
    )
    actions = ['export'] # 'update'

    import_form_class = ImportForm
    export_form_class = ExportForm
    resource_class = NoteExportResource

    def export(self, request, queryset):
        appointment_resource = NoteExportResource()
        dataset = appointment_resource.export(queryset)
        response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="{}.xlsx"'.format(_('Notes'))
        return response

    export.short_description = _('Export selected %(verbose_name_plural)s')

    def update(self, request, queryset):
        for item in queryset.all():
            item.reason ='Laboratorio'
            item.save()

            '''
            Nutrición:      3219
            Seguimiento:    21431
            Tratamiento:    46
            Laboratorio:    214
            Comentario:     292
            Inbody:         5505
            Consulta:       188
            Receta:         138
            Obesidad:       30
            Dieta:          388
            --------------------
            Otros:          5326
            '''
            # print(item.reason) # Homogenizar la info para un solo reason, algo como un nomenclador

    update.short_description = _('Update selected %(verbose_name_plural)s')

    actions_list = ["changelist_global_action_sync_up"]

    @action(description=_("Sync up"))
    def changelist_global_action_sync_up(self, request: HttpRequest):
        sync_up_notes()
        messages.success(request, _('Notes synced correctly.'))
        return redirect("/base/note/")

    def get_id(self, instance):
        return '{0}...{1}'.format(instance.id[:10], instance.id[-10:])

    get_id.short_description = _('ID')
    get_id.allow_tags = True

    def patient_link(self, instance):
        if instance.patient:
            url = reverse("admin:base_patient_change", args=[instance.patient_id])
            return format_html(
                '<a href="{}" style="font-weight: bold; color: #c084fc;">{}</a>',
                url, instance.patient.get_full_name()
            )
        return "-"

    patient_link.short_description = "Patient"

    def get_date_joined(self, instance):
        return instance.date_joined.strftime('%d/%m/%Y') if instance.date_joined else None

    get_date_joined.short_description = _('date joined')
    get_date_joined.allow_tags = True

    def get_modified_date(self, instance):
        return instance.modified_date.strftime('%d/%m/%Y') if instance.modified_date else None

    get_modified_date.short_description = _('modified date')
    get_modified_date.allow_tags = True
