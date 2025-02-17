from datetime import datetime

from django.shortcuts import render
from .models import Patient, Note  # Ajusta según tus modelos
from apps.base.utils import (
    get_patients_last_year_for_month, get_notes_last_year_for_month, get_top_patients,
    get_patients_by_reasons, get_notes_by_reasons
)


def dashboard_callback(request, context):
    # 📌 Obtén los pacientes del año pasado por meses
    patients_last_year_for_month = get_patients_last_year_for_month()

    # 📌 Obtén las consultas del año pasado por meses
    notes_last_year_for_month = get_notes_last_year_for_month()

    # 📌 Obtener los 5 pacientes con más visitas
    top_patients = get_top_patients()

    # 📌 Segmentar pacientes por temas (ejemplo: tipo de consulta)
    patients_segments = get_patients_by_reasons()

    # 📌 Segmentar consultas por temas (ejemplo: Tratamiento)
    notes_segments = get_notes_by_reasons()

    # Añade los datos al contexto
    context.update({
        'patients_last_year_for_month': patients_last_year_for_month,
        'notes_last_year_for_month': notes_last_year_for_month,
        "top_patients": top_patients,
        "patients_segments": patients_segments,
        "notes_segments": notes_segments
    })
    return context
