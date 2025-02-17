from django.template.backends.django import reraise
from django.utils.dateparse import parse_time
from unfold.templatetags.unfold_list import results
from collections import defaultdict
from django.db.models import Count, Q
from django.utils.timezone import now
from django.db.models.functions import ExtractMonth

from apps.connection import SugarOnWebConn as sugarcon
from apps.base.models import Patient, Note
import re


def set_gender(value):
    if value:
        return str(value).upper()[:1]
    return 'SE'

def extract_numbers(value):
    """
    Extrae solo los números de una cadena y los devuelve como un string concatenado.
    """
    if value:
        return "".join(re.findall(r"\d+", value))
    return None

def sync_up_patients() -> None:
    conn = sugarcon()
    results = conn.execute(
       'SELECT '
       'c.id AS paciente_id, '
       'c.date_entered AS date_joined, '
       'c.date_modified AS modified_date, '
       'c.first_name AS first_name, '
       'c.last_name AS last_name, '
       'c.phone_home AS phone_home, '
       'c.phone_mobile AS phone_mobile, '
       'cc.fechadenacimiento_c AS birthdate, '
       'cc.sexo_c AS gender, '
       'cc.quienlorefiere_c AS referred_by '
       'FROM '
       'contacts c '
       'JOIN '
       'contacts_cstm cc ON c.id = cc.id_c;'
    )
    conn.close()

    for item in results:
        patient, created = Patient.objects.update_or_create(
            id=item[0],
            defaults={
                'date_joined': item[1],
                'modified_date': item[2],
                'first_name': item[3],
                'last_name': item[4],
                'phone_home': extract_numbers(item[5]),
                'phone_mobile': extract_numbers(item[6]),
                'birthdate': item[7],
                'gender': set_gender(item[8]),
                'referred_by': item[9],
            }
        )

def sync_up_notes() -> None:
    conn = sugarcon()
    results = conn.execute(
        ''
        'SELECT '
        'n.id, '
        'n.date_entered, '
        'n.date_modified,'
        'n.name,'
        'n.description,'
        'n.contact_id '
        'FROM `notes` n '
        'INNER JOIN contacts c ON n.contact_id = c.id '
        'WHERE name IS NOT NULL;'
        ''
    )
    conn.close()

    for item in results:
        note, created = Note.objects.update_or_create(
            id=item[0],
            defaults={
                'date_joined': item[1],
                'modified_date': item[2],
                'reason': item[3],
                'description': item[4],
                'patient_id': item[5],
            }
        )


# Categorías principales que queremos destacar
REASONS = [
    "Nutrición", "Seguimiento", "Tratamiento", "Laboratorio",
    "Eliminación", "Antiinflamatorio", "Comentario",
    "Inbody", "Consulta", "Receta", "Obesidad", "Dieta"
]


def get_patients_last_year_for_month():
    """
    Obtiene la cantidad de pacientes dados de alta en cada mes del año anterior.
    """
    last_year = now().year - 1

    patients_by_month = (
        Patient.objects.filter(date_joined__year=last_year)
        .annotate(month=ExtractMonth("date_joined"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    # Convertimos en diccionario con claves de 1 a 12 (meses)
    data_for_month = defaultdict(int, {item["month"]: item["total"] for item in patients_by_month})

    return {
        "labels": list(data_for_month.keys()),
        "values": list(data_for_month.values())
    }

def get_notes_last_year_for_month():
    """
    Obtiene la cantidad de pacientes dados de alta en cada mes del año anterior.
    """
    last_year = now().year - 1

    notes_by_month = (
        Note.objects.filter(date_joined__year=last_year)
        .annotate(month=ExtractMonth("date_joined"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    # Convertimos en diccionario con claves de 1 a 12 (meses)
    data_for_month = defaultdict(int, {item["month"]: item["total"] for item in notes_by_month})

    return {
        "labels": list(data_for_month.keys()),
        "values": list(data_for_month.values())
    }

def get_top_patients():
    return (
        Patient.objects.annotate(visit_count=Count("notes"))
        .order_by("-visit_count")[:5]
    )

def get_patients_by_reasons():
    """
    Cuenta la cantidad de pacientes según el tipo de consulta en 'reason' en Notes.
    Agrupa las categorías menos frecuentes en 'Otros'.
    """

    # Diccionario para almacenar los resultados
    data_query = defaultdict(int)

    # Si la categoría está en la lista de relevantes, la guardamos directamente
    for reason in REASONS:
        data_query[reason] = len(Patient.objects.filter(notes__reason__icontains=reason).distinct())

    data_query["Otros"] = len(
        Patient.objects.exclude(
            Q(notes__reason__icontains="Nutrición") |
            Q(notes__reason__icontains="Seguimiento") |
            Q(notes__reason__icontains="Tratamiento") |
            Q(notes__reason__icontains="Laboratorio") |
            Q(notes__reason__icontains="Eliminación") |
            Q(notes__reason__icontains="Antiinflamatorio") |
            Q(notes__reason__icontains="Comentario") |
            Q(notes__reason__icontains="Inbody") |
            Q(notes__reason__icontains="Consulta") |
            Q(notes__reason__icontains="Receta") |
            Q(notes__reason__icontains="Obesidad") |
            Q(notes__reason__icontains="Dieta")
        ).distinct()
    )  # Agrupamos el resto de reasons

    return {
        "labels": list(data_query.keys()),  # Lista de nombres de consultas
        "values": list(data_query.values())  # Lista de cantidades
    }

def get_notes_by_reasons():
    """
    Cuenta la cantidad de notas según el tipo de consulta en 'reason' en Notes.
    Agrupa las categorías menos frecuentes en 'Otros'.
    """
    conteo_consultas = Note.objects.values("reason").annotate(total=Count("id"))

    # Diccionario para almacenar los resultados
    datos_consulta = defaultdict(int)

    for consulta in conteo_consultas:
        tipo = consulta["reason"]
        cantidad = consulta["total"]

        # Si la categoría está en la lista de relevantes, la guardamos directamente
        if tipo in REASONS:
            datos_consulta[tipo] += cantidad
        else:
            datos_consulta["Otros"] += cantidad  # Agrupamos los menos relevantes

    return {
        "labels": list(datos_consulta.keys()),  # Lista de nombres de consultas
        "values": list(datos_consulta.values())  # Lista de cantidades
    }
