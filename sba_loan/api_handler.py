import requests
import os
from dotenv import load_dotenv, set_key

load_dotenv()

def login():
    
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    
    if not username or not password:
        raise Exception("Please set API_USERNAME and API_PASSWORD in your .env file")
    
    url = os.getenv("BASE_URL")+"/api/login"
    
    data = {
        "username": username,
        "password": password
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Réponse de l'API :")
        print(response.json())
        token = response.json()["access_token"]
        
        if os.getenv("LOCAL") != "0":
            set_key("../.env", "TOKEN", response.json()["access_token"])
        else:
            os.environ["ACCESS_TOKEN"] = response.json()["access_token"]
        return token
    else:
        print(f"Erreur : {response.status_code}")
        print(response.text)
        raise Exception("Failed to login.")

def make_prediction(data:dict):
    
    if os.getenv("LOCAL") != "0":
        token = os.getenv("TOKEN")
    else:
        token = os.environ.get("ACCESS_TOKEN")
    if not token:
        token = login()
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(
            f"{os.getenv("BASE_URL")}/api/loans/predict",
            json=data,
            headers=headers
        )
        print(response.json)
        response.raise_for_status() #Lève une exception si status != 200
        
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            # Token expired or invalid
            token = login()
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = requests.post(
                f"{os.getenv("BASE_URL")}/api/loans/predict",
                json=data,
                headers=headers
            )
            response.raise_for_status()
        else:
            # Other HTTP error
            raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")
    
    return response.json()

if __name__ == "__main__":
    
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
    
    print(make_prediction(data=data))

    print("DATA : ", data)
