#!/bin/bash

# Configuration des variables (modifiez-les selon vos besoins)
RESOURCE_GROUP=""
ACR_NAME=""  # Nom de votre Azure Container Registry
REGION="francecentral"  # Région où vous souhaitez déployer
IMAGE_NAME=""  # Nom de l'image Docker
CONTAINER_NAME=""  # Nom du conteneur
DOCKER_COMPOSE_PATH="compose.yaml"  # Le chemin vers votre fichier docker-compose
PORT=8000

. ./.env

echo $REGISTRY_USERNAME
echo $REGISTRY_PASSWORD


# 1. Authentification Azure (connectez-vous à votre compte Azure)
echo "Authentification Azure..."


# 4. Connexion à Azure Container Registry
echo "Connexion à Azure Container Registry..."
az acr login --name $ACR_NAME
az acr update -n $ACR_NAME --admin-enabled true
REGISTRY_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
REGISTRY_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

#4.5 Suppression du container existant
echo "Deleting existing container (if any)..."
az container delete --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --yes

# 5. Construction de l'image Docker avec le Dockerfile
echo "Construction de l'image Docker..."
docker compose -f $DOCKER_COMPOSE_PATH build

# 6. Taguer l'image Docker pour Azure Container Registry
echo "Taguer l'image Docker pour Azure Container Registry..."
docker tag $IMAGE_NAME $ACR_NAME.azurecr.io/$IMAGE_NAME:latest

# 7. Pousser l'image vers Azure Container Registry
echo "Pousser l'image vers Azure Container Registry..."
docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:latest

# 8. Déploiement du conteneur sur Azure Container Instances
echo "Déploiement du conteneur sur Azure Container Instances..."
az container create \
    --resource-group $RESOURCE_GROUP \
    --name $CONTAINER_NAME \
    --image $ACR_NAME.azurecr.io/$IMAGE_NAME:latest \
    --dns-name-label sthorezloandjangoweb \
    --cpu 1 \
    --memory 1.5 \
    --ip-address public \
    --ports $PORT \
    --environment-variables SECRET_KEY=$SECRET_KEY DB_HOST=$DB_HOST API_USERNAME=$API_USERNAME API_PASSWORD=$API_PASSWORD API_URL=$API_URL TOKEN=$TOKEN DB_NAME=$DB_NAME DB_USERNAME=$DB_USERNAME DB_PASSWORD=$DB_PASSWORD DB_PORT=$DB_PORT DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS DJANGO_LOGLEVEL=$DJANGO_LOGLEVEL DEBUG=$DEBUG LOCAL=$LOCAL \
    --registry-login-server $ACR_NAME.azurecr.io \
    --registry-username $REGISTRY_USERNAME \
    --registry-password $REGISTRY_PASSWORD \
    --os-type Linux


# 9. Afficher l'URL du conteneur
CONTAINER_IP=$(az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_NAME --query "ipAddress.ip" -o tsv)
echo "Le conteneur est déployé. Vous pouvez y accéder à l'adresse suivante : http://$CONTAINER_IP:$PORT"
