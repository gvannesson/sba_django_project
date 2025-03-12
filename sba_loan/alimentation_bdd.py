from django.contrib.auth.hashers import PBKDF2PasswordHasher
import pandas as pd
import os
import django
from django.db import IntegrityError
# Configurer l'environnement Django avec le bon chemin vers settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sba_loan.settings")

# Initialiser Django
django.setup()

# Importer ton modèle User
from sba_website.models import User, LoanRequest

# Initialiser le hasher PBKDF2
hasher = PBKDF2PasswordHasher()

# Charger ton fichier CSV
df = pd.read_csv('clients_projet_bank.csv')

# Insérer les données dans la base de données (exemple de traitement)
i = 0
for index, row in df.iterrows():
    email = f'{row["LoanNr_ChkDgt"]}@gmail.com'
    
    # Hacher le mot de passe 'azerty' pour chaque utilisateur
    hashed_password = hasher.encode('azerty', hasher.salt())

    # Créer un utilisateur avec un email unique et sans username
    user = User(
        email=email,
        username='',  # Laisser le username vide
        password=hashed_password,  # Utiliser le mot de passe haché
        company_name=row['Name'],
        state=row['State'],
        NAICS=row['NAICS'],
        urbanrural=row['UrbanRural'],
        franchisecode=row['FranchiseCode'],
        role=0,  # Rôle par défaut
    )
    
    try:
        user.save()  # Sauvegarder l'utilisateur
    except IntegrityError as e:
        print(f"Erreur lors de l'insertion de l'utilisateur avec l'email {email}: {e}")
        continue  # Passer à l'itération suivante si l'utilisateur existe déjà

    # Créer un LoanRequest et associer l'utilisateur
    loan_request = LoanRequest(
        bank_loan=row['bank_loan_float'],
        sba_loan=row['SBA_loan_float'],
        lowdoc=row['LowDoc'],
        revlinecr=row['RevLineCr'],
        term=row['Term'],
        user_id=user  # Associer l'utilisateur créé au LoanRequest
    )

    try:
        loan_request.save()  # Sauvegarder la demande de prêt
        i += 1
    except IntegrityError as e:
        print(f"Erreur lors de l'insertion de la demande de prêt pour l'utilisateur {email}: {e}")
        continue  # Passer à l'itération suivante en cas d'erreur
