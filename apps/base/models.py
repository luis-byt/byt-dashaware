from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


GENDER_CHOICES = (
    ("SE", "No especificado"),
    ("M", "Masculino"),
    ("F", "Femenino"),
    ("B", "Binario"),
    ("NB", "No Binario"),
    ("H", "Homosexual"),
    ("T", "Transexual"),
)


class Patient(models.Model):
    id = models.CharField(max_length=36, verbose_name=_("id"), primary_key=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    modified_date = models.DateTimeField(_("modified date"), default=timezone.now)
    first_name = models.CharField(_("first name"), max_length=150, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, null=True, blank=True)
    phone_home = models.CharField(_("phone home"), max_length=130, null=True, blank=True)
    phone_mobile = models.CharField(_("mobile"), max_length=130, null=True, blank=True)
    email = models.EmailField(_("email"), null=True, blank=True, default=None)
    birthdate = models.DateTimeField(_("birthdate"), default=None, null=True, blank=True)
    gender = models.CharField(_("gender"), choices=GENDER_CHOICES, max_length=20, default='SE')
    referred_by = models.CharField(
        _("referred by"),
        max_length=150,
        null=True,
        blank=True,
        help_text=_("Enter the name of the person or entity who referred you to our clinic (optional).")
    )

    class Meta:
        verbose_name = _("patient")
        verbose_name_plural = _("patients")
        ordering = ("-date_joined", "first_name", "last_name")

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return "{first_name}{last_name}".format(
            first_name=f"{self.first_name} " if self.first_name else "",
            last_name=f"{self.last_name} " if self.last_name else ""
        )

    def get_str_gender(self):
        return dict(GENDER_CHOICES).get(self.gender, GENDER_CHOICES[0][1])

    def get_phones(self):
        phones = list()

        if self.phone_home:
            phones.append(self.phone_home)
        if self.phone_mobile:
            phones.append(self.phone_mobile)

        return phones

class Note(models.Model):
    id = models.CharField(max_length=36, verbose_name=_("id"), primary_key=True)
    patient = models.ForeignKey(
        Patient, verbose_name=_("patient"), on_delete=models.SET_NULL,
        related_name='notes', null=True, blank=True
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    modified_date = models.DateTimeField(_("modified date"), default=timezone.now)
    reason = models.CharField(max_length=255, verbose_name=_("reason"))
    description = models.TextField(
        verbose_name=_("description"),
        help_text=_("a brief description of the patient's reason and/or objective in the clinic"),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("note")
        verbose_name_plural = _("notes")
        ordering = ("-date_joined", "reason")

    def __str__(self):
        return self.reason
