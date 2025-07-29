"""
WSGI config for caroline_dolls project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caroline_dolls.settings')

application = get_wsgi_application()



import django
from django.contrib.auth import get_user_model

django.setup()
User = get_user_model()

username = "hakheem"
email = "hakheemwyatt2@gmail.com"
password = "holli123.J"

# Only create if not already created
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Superuser created!")

