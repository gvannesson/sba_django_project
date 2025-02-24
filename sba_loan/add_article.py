import os
import django
import datetime

# Configurer l'environnement Django avec le bon chemin vers settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sba_loan.settings")

# Initialiser Django
django.setup()

# Maintenant tu peux importer ton modèle User
from sba_website.models import News  # Assure-toi d'importer ton modèle User
import pandas as pd

items= 'Bundestag'
date_news = datetime.datetime(2025, 2, 23)
new_url = 'https://www.economist.com/europe/2025/02/23/merz-wins-a-messy-election-then-calls-for-independence-from-america'
new_entry = News(items=items, date_news=date_news, news_url=new_url)
new_entry.save()