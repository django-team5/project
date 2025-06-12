import os
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    call_command("migrate", interactive=False)
    call_command("collectstatic", "--noinput")
except Exception as e:
    print(f"[MIGRATE ERROR] {e}")

application = get_wsgi_application()