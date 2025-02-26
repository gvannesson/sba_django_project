import requests

# URL de l'API à laquelle tu veux envoyer la requête POST
url = 'http://127.0.0.1:8000/api/login'

# Données à envoyer dans la requête POST (en général sous forme de dictionnaire)
data = {
    'username': 'Admin',
    'password': 'azerty1234'
}

# Effectuer la requête POST avec les données au format JSON
response = requests.post(url, data=data)

# Vérifier si la requête a été réussie
if response.status_code == 200:
    print("Réponse de l'API :")
    print(response.json())  # Récupérer et afficher la réponse JSON de l'API
    token = response.json()["access_token"]
else:
    print(f"Erreur : {response.status_code}")
    print(response.text)  # Afficher le texte brut en cas d'erreur

# URL du endpoint que tu veux appeler
url = 'http://127.0.0.1:8000/api/loans/predict'

# Le token d'authentification que tu as obtenu avec la requête POST
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBZG1pbiIsImlkIjoxLCJleHAiOjE3NDA1ODE5MTV9.aQzjL_WGNv-R0SVtZy-kY1Ry6MUurhEFZ-vdS3jwxiQ'

data = {
                "state": "NJ",
                "term": 45,
                "no_emp": 45,
                "urban_rural": 0,
                "cat_activities": 0,
                "bank_loan_float": 600000.0,
                "sba_loan_float": 499998.0,
                "franchise_code": 0,
                "lowdoc": False,
                "bank": "NEW JERSEY ECONOMIC DEVEL"
                }

# Créer les en-têtes avec le token d'authentification (Bearer token)
headers = {
    'Authorization': f'Bearer {token}'
}

# Effectuer la requête GET en envoyant le token dans les en-têtes
response = requests.post(url, json=data, headers=headers)

# Vérification du statut de la réponse
if response.status_code == 200:
    print("Utilisateur trouvé :", response.json())  # Afficher les informations de l'utilisateur
else:
    print(f"Erreur {response.status_code}: {response.text}")  # Afficher le message d'erreur