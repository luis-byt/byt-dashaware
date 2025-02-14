# Generated by Django 5.1.5 on 2025-02-13 23:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "modified_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="modified date"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="last name"
                    ),
                ),
                (
                    "phone_home",
                    models.CharField(
                        blank=True, max_length=130, null=True, verbose_name="phone home"
                    ),
                ),
                (
                    "phone_mobile",
                    models.CharField(
                        blank=True, max_length=130, null=True, verbose_name="mobile"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        default=None,
                        max_length=254,
                        null=True,
                        verbose_name="email",
                    ),
                ),
                (
                    "birthdate",
                    models.DateTimeField(
                        blank=True, default=None, null=True, verbose_name="birthdate"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("SE", "No especificado"),
                            ("M", "Masculino"),
                            ("F", "Femenino"),
                            ("B", "Binario"),
                            ("NB", "No Binario"),
                            ("H", "Homosexual"),
                            ("T", "Transexual"),
                        ],
                        default="SE",
                        max_length=20,
                        verbose_name="gender",
                    ),
                ),
                (
                    "referred_by",
                    models.CharField(
                        blank=True,
                        help_text="Enter the name of the person or entity who referred you to our clinic (optional).",
                        max_length=150,
                        null=True,
                        verbose_name="referred by",
                    ),
                ),
            ],
            options={
                "verbose_name": "patient",
                "verbose_name_plural": "patients",
                "ordering": ("-date_joined", "first_name", "last_name"),
            },
        ),
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "modified_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="modified date"
                    ),
                ),
                ("reason", models.CharField(max_length=255, verbose_name="reason")),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="a brief description of the patient's reason and/or objective in the clinic",
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="notes",
                        to="base.patient",
                        verbose_name="patient",
                    ),
                ),
            ],
            options={
                "verbose_name": "note",
                "verbose_name_plural": "notes",
                "ordering": ("-date_joined", "reason"),
            },
        ),
    ]
