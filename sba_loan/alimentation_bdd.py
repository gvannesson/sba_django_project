import os
import django

# Configurer l'environnement Django avec le bon chemin vers settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sba_loan.settings")

# Initialiser Django
django.setup()

# Maintenant tu peux importer ton modèle User
from sba_website.models import User  # Assure-toi d'importer ton modèle User
import pandas as pd

# Charger ton fichier CSV
df = pd.read_csv('sba_loan/clients_projet_bank.csv')

# Insérer les données dans la base de données (exemple de traitement)
for index, row in df.iterrows():
    user = User(
        username=row['LoanNr_ChkDgt'],  # Assure-toi que la colonne 'username' existe dans ton CSV
        password = 'azerty',
        name=row['Name'],
        state=row['State'],
        NAICS=row['NAICS'],
        urbanrural=row['UrbanRural'],
        lowdoc=row['LowDoc'],
        bank_loan=row['bank_loan_float'],
        sba_loan=row['SBA_loan_float'],
        franchisecode=row['FranchiseCode'],
        revlinecr=row['RevLineCr'],
        term=row['Term'],
        role = 0,
    )
    user.save()  # Enregistrer chaque utilisateur


