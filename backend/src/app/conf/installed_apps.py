# Application definition

APPS = [
    "a12n",
    "app",
    "users",
    "clubs",
]

THIRD_PARTY_APPS = [
    "django_prometheus",  # Must be first for middleware wrapping
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "axes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
]

INSTALLED_APPS = THIRD_PARTY_APPS + APPS
