import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projadocato.settings')
django.setup()

def run():

    User = get_user_model()
    username = 'professor'
    password = os.environ.get('ADMIN_PASSWORD')

    if not password:
        print("Erro: variável de ambiente ADMIN_PASSWORD não definida.")
        exit(1)

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
        print(f"Superusuário '{username}' criado com sucesso.")
    else:
        print(f"Superusuário '{username}' já existe.")