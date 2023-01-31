from django.contrib.auth.models import User


def populate():
    User.objects.create_superuser(
        username="super", email="super@neomadas.com", password="super"
    )
