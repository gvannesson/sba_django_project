import os
import django
from django.contrib.auth.hashers import PBKDF2PasswordHasher
import pandas as pd

# Configurer l'environnement Django avec le bon chemin vers settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sba_loan.settings")

# Initialiser Django
django.setup()

# Importer ton modèle User
from sba_website.models import User, LoanRequests

# Initialiser le hasher PBKDF2
hasher = PBKDF2PasswordHasher()

# Charger ton fichier CSV
df = pd.read_csv('clients_projet_bank.csv')

# Insérer les données dans la base de données (exemple de traitement)
for index, row in df.iterrows():
    # Hacher le mot de passe 'azerty' pour chaque utilisateur
    hashed_password = hasher.encode('azerty', hasher.salt())

    user = User(
        username=row['LoanNr_ChkDgt'],  # Assure-toi que la colonne 'username' existe dans ton CSV
        password=hashed_password,  # Utiliser le mot de passe haché
        name=row['Name'],
        email = f'{row['LoanNr_ChkDgt']}@gmail.com',
        state=row['State'],
        NAICS=row['NAICS'],
        urbanrural=row['UrbanRural'],
        franchisecode=row['FranchiseCode'],
        role=0,
    )

    loan_request = LoanRequests(
        name_company = row['Name'],
        username=row['LoanNr_ChkDgt'], 
        bank_loan=row['bank_loan_float'],
        sba_loan=row['SBA_loan_float'],
        lowdoc=row['LowDoc'],
        revlinecr=row['RevLineCr'],
        term=row['Term'],

    )
    user.save()  # Enregistrer chaque utilisateur
    loan_request.save()
