from django.utils.dateparse import parse_time
from unfold.templatetags.unfold_list import results

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
