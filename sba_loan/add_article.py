import os
import django
import datetime
from django.utils import timezone
from django.contrib.auth.hashers import PBKDF2PasswordHasher

# Configurer l'environnement Django avec le bon chemin vers settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sba_loan.settings")

# Initialiser Django
django.setup()

# Maintenant tu peux importer ton modèle User
from sba_website.models import News, User  # Assure-toi d'importer ton modèle User
import pandas as pd

topic= 'Bundestag'
date_news = datetime.datetime(2025, 2, 23)
# Rendre la date "aware" (c'est-à-dire qu'elle sera liée à un fuseau horaire)
date_news = timezone.make_aware(date_news)
new_url = 'https://www.economist.com/europe/2025/02/23/merz-wins-a-messy-election-then-calls-for-independence-from-america'
content = 'reekfkefkeflfldfdfd'
new_entry = News(topic=topic, date_news=date_news, news_url=new_url, content = content)
new_entry.user_id = User.objects.all()[0]
new_entry.save()

# Créer un admin
hasher = PBKDF2PasswordHasher()
hashed_password = hasher.encode('azerty', hasher.salt())


user = User(
    email='admin1@admin.fr',
    username='admin1',
    password=hashed_password,  # Utiliser le mot de passe haché
    is_superuser = 1,
    role=1
)
user.save()