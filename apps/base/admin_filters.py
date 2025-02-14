from django.contrib import admin
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from unfold.contrib.filters.admin import TextFilter, DropdownFilter


class FullNameFilter(TextFilter):
    title = _("full name")
    parameter_name = "full_name__icontains"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(
                first_name__icontains=self.value()
            ) | queryset.filter(
                last_name__icontains=self.value()
            ) | queryset.filter(
                first_name__icontains=self.value().split()[0],
                last_name__icontains=" ".join(self.value().split()[1:])
            )
        return queryset


class PatientFullNameFilter(TextFilter):
    title = _("patient full name")
    parameter_name = "patient_full_name__icontains"

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(
                patient__first_name__icontains=self.value()
            ) | queryset.filter(
                patient__last_name__icontains=self.value()
            ) | queryset.filter(
                patient__first_name__icontains=self.value().split()[0],
                patient__last_name__icontains=" ".join(self.value().split()[1:])
            )
        return queryset


class ReasonFilter(DropdownFilter):
    title = _("reason")
    parameter_name = "reason__icontains"

    def lookups(self, request, model_admin):
        return [
            ('Nutrición', 'Nutrición'),
            ('Seguimiento', 'Seguimiento'),
            ('Tratamiento', 'Tratamiento'),
            ('Laboratorio', 'Laboratorio'),
            ('Comentario', 'Comentario'),
            ('Inbody', 'Inbody'),
            ('Consulta', 'Consulta'),
            ('Receta', 'Receta'),
            ('Obesidad', 'Obesidad'),
            ('Dieta', 'Dieta'),
            ('Otros', 'Otros'),  # Agregar opción para notas sin coincidencias en el título
        ]

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "Otros":
                return queryset.exclude(
                    Q(reason__icontains="Nutrición") |
                    Q(reason__icontains="Seguimiento") |
                    Q(reason__icontains="Tratamiento") |
                    Q(reason__icontains="Laboratorio") |
                    Q(reason__icontains="Comentario") |
                    Q(reason__icontains="Inbody") |
                    Q(reason__icontains="Consulta") |
                    Q(reason__icontains="Receta") |
                    Q(reason__icontains="Obesidad") |
                    Q(reason__icontains="Dieta")
                )
            else:
                return queryset.filter(reason__icontains=self.value())
        return queryset


class PatientReasonFilter(DropdownFilter):
    title = _("reason")
    parameter_name = "reason__icontains"

    def lookups(self, request, model_admin):
        return [
            ('Nutrición', 'Nutrición'),
            ('Seguimiento', 'Seguimiento'),
            ('Tratamiento', 'Tratamiento'),
            ('Laboratorio', 'Laboratorio'),
            ('Comentario', 'Comentario'),
            ('Inbody', 'Inbody'),
            ('Consulta', 'Consulta'),
            ('Receta', 'Receta'),
            ('Obesidad', 'Obesidad'),
            ('Dieta', 'Dieta'),
            ('Otros', 'Otros'),  # Agregar opción para notas sin coincidencias en el título
        ]

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == "Otros":
                return queryset.exclude(
                    Q(notes__reason__icontains="Nutrición") |
                    Q(notes__reason__icontains="Seguimiento") |
                    Q(notes__reason__icontains="Tratamiento") |
                    Q(notes__reason__icontains="Laboratorio") |
                    Q(notes__reason__icontains="Comentario") |
                    Q(notes__reason__icontains="Inbody") |
                    Q(notes__reason__icontains="Consulta") |
                    Q(notes__reason__icontains="Receta") |
                    Q(notes__reason__icontains="Obesidad") |
                    Q(notes__reason__icontains="Dieta")
                ).distinct()
            else:
                return queryset.filter(notes__reason__icontains=self.value()).distinct()
        return queryset
