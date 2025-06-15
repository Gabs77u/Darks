import os
import django
from django.core.management import execute_from_command_line
from crypto.security_protocols import generate_self_signed_cert


def start_django_api():
    # Garante que a API use TLS/SSL se necessário
    generate_self_signed_cert("api_cert.pem", "api_key.pem")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "integrations.django_settings")
    django.setup()
    execute_from_command_line(["manage.py", "runserver", "8000"])


if __name__ == "__main__":
    start_django_api()
