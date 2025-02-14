from django.contrib.auth.models import Group, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupCore(Group):
    description = models.CharField(max_length=150, null=True, blank=True, verbose_name=_("description"))

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.description or self.name


class User(AbstractUser):
    username = models.CharField(max_length=225, null=True, default=None, blank=True, verbose_name=_("username"))
    email = models.EmailField(max_length=225, unique=True, verbose_name=_("email"))
    phone = models.CharField(max_length=25, unique=True, verbose_name=_("phone"))
    image = models.ImageField(upload_to="img/clients", null=True, default=None, blank=True, verbose_name=_("image"))
    groups = models.ManyToManyField(
        GroupCore,
        verbose_name=_('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
