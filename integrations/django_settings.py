SECRET_KEY = "vpn-projeto-wireguard"
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    "rest_framework",
]
MIDDLEWARE = []
ROOT_URLCONF = "integrations.urls"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
USE_TZ = True
