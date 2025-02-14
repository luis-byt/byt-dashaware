from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.utils.translation import gettext_lazy as _

from apps.base.models import Patient, Note


class PatientExportResource(resources.ModelResource):
    consecutive = fields.Field(column_name=_('no.'), readonly=True)
    id = fields.Field(column_name=_('id'), readonly=True)
    first_name = fields.Field(column_name=_('first name'), readonly=True)
    last_name = fields.Field(column_name=_('last name'), readonly=True)
    phone_home = fields.Field(column_name=_('phone home'), readonly=True)
    phone_mobile = fields.Field(column_name=_('mobile'), readonly=True)
    email = fields.Field(column_name=_('email'), readonly=True)
    birthdate = fields.Field(column_name=_('birthdate'), readonly=True)
    gender = fields.Field(column_name=_('gender'), readonly=True)
    referred_by = fields.Field(column_name=_('referred by'), readonly=True)
    date_joined = fields.Field(column_name=_('date joined'), readonly=True)
    modified_date = fields.Field(column_name=_('modified date'), readonly=True)

    class Meta:
        model = Patient
        fields = [
            'consecutive', 'id', 'first_name', 'last_name', 'phone_home', 'phone_mobile', 'email', 'birthdate',
            'gender', 'referred_by', 'date_joined', 'modified_date',
        ]
        export_order = (
            'consecutive', 'id', 'first_name', 'last_name', 'phone_home', 'phone_mobile', 'email', 'birthdate',
            'gender', 'referred_by', 'date_joined', 'modified_date',
        )

    def __init__(self, **kwargs):
        super(PatientExportResource, self).__init__()
        self.counter = 0

    def dehydrate_consecutive(self, instance):
        self.counter = self.counter + 1
        for i, item in enumerate(self.get_queryset()):
            if instance == item:
                return self.counter

    @staticmethod
    def dehydrate_id(instance):
        return instance.id

    @staticmethod
    def dehydrate_first_name(instance):
        return instance.first_name

    @staticmethod
    def dehydrate_last_name(instance):
        return instance.last_name

    @staticmethod
    def dehydrate_phone_home(instance):
        return instance.phone_home

    @staticmethod
    def dehydrate_phone_mobile(instance):
        return instance.phone_mobile

    @staticmethod
    def dehydrate_email(instance):
        return instance.email

    @staticmethod
    def dehydrate_birthdate(instance):
        if instance.birthdate:
            return instance.birthdate.replace(tzinfo=None)
        return None

    @staticmethod
    def dehydrate_gender(instance):
        return instance.get_str_gender()

    @staticmethod
    def dehydrate_referred_by(instance):
        return instance.referred_by

    @staticmethod
    def dehydrate_date_joined(instance):
        if instance.date_joined:
            return instance.date_joined.replace(tzinfo=None)
        return None

    @staticmethod
    def dehydrate_modified_date(instance):
        if instance.modified_date:
            return instance.modified_date.replace(tzinfo=None)
        return None


class NoteExportResource(resources.ModelResource):
    consecutive = fields.Field(column_name=_('no.'), readonly=True)
    id = fields.Field(column_name=_('id'), readonly=True)
    reason = fields.Field(column_name=_('reason'), readonly=True)
    description = fields.Field(column_name=_('description'), readonly=True)
    date_joined = fields.Field(column_name=_('date joined'), readonly=True)
    modified_date = fields.Field(column_name=_('modified date'), readonly=True)

    class Meta:
        model = Note
        fields = ['consecutive', 'id', 'patient', 'reason', 'description', 'date_joined', 'modified_date',]
        export_order = (
            'consecutive', 'id', 'patient', 'reason', 'description', 'date_joined', 'modified_date',
        )

    def __init__(self, **kwargs):
        super(NoteExportResource, self).__init__()
        self.counter = 0

    def dehydrate_consecutive(self, instance):
        self.counter = self.counter + 1
        for i, item in enumerate(self.get_queryset()):
            if instance == item:
                return self.counter

    @staticmethod
    def dehydrate_id(instance):
        return instance.id

    @staticmethod
    def dehydrate_date_joined(instance):
        if instance.date_joined:
            return instance.date_joined.replace(tzinfo=None)
        return None

    @staticmethod
    def dehydrate_modified_date(instance):
        if instance.modified_date:
            return instance.modified_date.replace(tzinfo=None)
        return None