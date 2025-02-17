from pathlib import Path
from datetime import timedelta
import os

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": 'AWARE',
    "SITE_HEADER": 'AWARE',
    "SITE_URL": "/",
    "SITE_SYMBOL": "storefront",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "byt_dashaware.settings.environment_callback",
    "DASHBOARD_CALLBACK": "apps.base.views.dashboard_callback",
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "es": "🇪🇸",
            },
        },
    },
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Dashboard"),
                "items": [
                    {
                        "title": _("Home"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "3",
                        "permission": lambda request: request.user.is_staff,
                    }
                ],
            },
            {
                "title": _("Security"),
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:core_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Groups"),
                        "icon": "diversity_3",
                        "link": reverse_lazy("admin:core_groupcore_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    }
                ],
            },
            {
                "title": _("Base"),
                "separator": True,
                "items": [
                    {
                        "title": _("Patients"),
                        "icon": "add_business",
                        "link": reverse_lazy("admin:base_patient_changelist"),
                        # "badge": "3",
                        "permission": lambda request: request.user.is_staff,
                    },
                    {
                        "title": _("Notes"),
                        "icon": "engineering",
                        "link": reverse_lazy("admin:base_note_changelist"),
                        # "badge": "3",
                        "permission": lambda request: request.user.is_staff,
                    },
            #         {
            #             "title": _("Integrations"),
            #             "icon": "rule_settings",
            #             "link": reverse_lazy("admin:base_integration_changelist"),
            #             # "badge": "3",
            #             "permission": lambda request: request.user.is_staff,
            #         },
            #         {
            #             "title": _("Categories"),
            #             "icon": "category",
            #             "link": reverse_lazy("admin:base_category_changelist"),
            #             # "badge": "3",
            #             "permission": lambda request: request.user.is_staff,
            #         },
            #         {
            #             "title": _("Products"),
            #             "icon": "inventory",
            #             "link": reverse_lazy("admin:base_product_changelist"),
            #             # "badge": "3",
            #             "permission": lambda request: request.user.is_staff,
            #         },
            #         {
            #             "title": _("Orders"),
            #             "icon": "shopping_cart_checkout",
            #             "link": reverse_lazy("admin:base_order_changelist"),
            #             # "badge": "3",
            #             "permission": lambda request: request.user.is_staff,
            #         }
                ],
            }
        ],
    },
}


def environment_callback(request):
    return ["Production", "danger"]


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-r26f@%e@%nxs^=z7+*l65)ilu#g5fv55frok5d)k+j+=v&8rz6"

DEBUG = True

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    'import_export'
]

LOCAL_APPS = [
    'apps.core',
    'apps.base',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "byt_dashaware.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "byt_dashaware.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dashawaredb',
        'USER': 'masqueradmin',
        'PASSWORD': 'masqueradmin',
        'HOST': 'localhost',
        'DATABASE_PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "es"

TIME_ZONE = 'America/Havana'

USE_I18N = True

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

USE_TZ = True

STATIC_ROOT = str(BASE_DIR / 'staticfiles')

STATIC_URL = "static/"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = '/media/'

MEDIA_ROOT = str(BASE_DIR / 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'

SUGARCRM =  {
    'HOST': '127.0.0.1', # 77.243.85.72
    'PORT': 3306,
    'DATABASE': 'wwwsugaronweb_ismcrm',
    'USER': 'awdbadm',
    'PASSWORD': 'Awkl32kl869*'
}
