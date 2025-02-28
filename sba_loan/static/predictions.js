
document.addEventListener("DOMContentLoaded", function() {
    const inputs = document.querySelectorAll(".pred"); // Sélectionne tous les éléments avec la classe "pred"

    inputs.forEach(function(element) { //pour chaque input dans la liste, il y a 2 listeners, (change et keyup), quand ces événements sont enclenchés, la fonction Predict est appelée
        element.addEventListener("change", Predict); // Ajoute l'événement "change"
        element.addEventListener("keyup", Predict);
        
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function Predict() //déf de la fonction Preduct
{
    const url = JSON.parse(document.getElementById('json_url').textContent) //récupère l'url de la page

    const data_construct = {
        "date_of_birth" : document.getElementById("date_birth").value,  // récupère la valeur de l'élément dans le html avec l'ID "date_birth"
        "weight" : document.getElementById("weight").value,
        "height" : document.getElementById("height").value,
        "sex" : document.getElementById("sex").value,
        "children" : document.getElementById("children").value,
        "region" : document.getElementById("region").value,
        "smoker" : document.getElementById("smoker").value,

    }

    fetch(url, {
        method: 'POST', //envoie une requête POST
        headers: {   //définit que ça envoie du JSON
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Ajoute le token CSRF
        },
        body: JSON.stringify(data_construct) //body: les infos envoyés, càd le dictionnaire transformé en JSON (JSON.stringify trasnsforme la donnée d'entrée en JSON)
    })
    .then(response => response.json())  // Convertir la réponse en JSON
    .then(data => { // tranforme sur la page HTML la valeur de certains éléments HTML basés sur le dictionnaire reçus de django
        document.getElementById('bmi_html').innerText = data.bmi.toString(); // met dans HTML la valeur de la clé bmi dans le dictionnaire data
        discount = document.getElementById('discount_html').value;
        if (discount>0){
            document.getElementById('prediction_discount').innerText = ((data.prediction)*(1-discount/100)).toFixed(2)+ " ("+discount+"%)" 
            " and without discount $" + data.prediction.toString()+".";
        }
        else document.getElementById('prediction').innerText = data.prediction.toString();
         // Affiche le message dans la page
    })
    .catch(error => console.error('Erreur :', error));
}

document.addEventListener("DOMContentLoaded", function() { //préremplissage des champs dans le html
    const json_date_of_birth = JSON.parse(document.getElementById('json_date_of_birth').textContent); //va chercher dans le html la variable nommée json_date_of_birth pour afficher les valeurs quand on charge la page
    document.getElementById('date_birth').value=json_date_of_birth;

    const json_weight2 = JSON.parse(document.getElementById('json_weight').textContent);
    document.getElementById('weight').value=json_weight2;

    const json_height = JSON.parse(document.getElementById('json_height').textContent);
    document.getElementById('height').value=json_height;

    const json_children = JSON.parse(document.getElementById('json_children').textContent);
    document.getElementById('children').value=json_children;

    const json_sex = JSON.parse(document.getElementById('json_sex').textContent);
    if (json_sex=='male'){
        document.getElementById('sex_option_1').selected=true;

    }
    else{
        document.getElementById('sex_option_2').selected=true;
    }
    const json_smoker = JSON.parse(document.getElementById('json_smoker').textContent);
    if (json_smoker=='yes'){
        document.getElementById('smoker_option_1').selected=true;

    }
    else{
        document.getElementById('smoker_option_2').selected=true;

    }
    const json_region = JSON.parse(document.getElementById('json_region').textContent);

    switch (json_region.toString()){
        case "1":
        document.getElementById('region_option_1').selected=true;
        break;
        case "2":
        document.getElementById('region_option_2').selected=true;
        break;
        case "3":
        document.getElementById('region_option_3').selected=true;
        break;
        case "4":
        document.getElementById('region_option_4').selected=true;
        break;
        
        default:
            console.log("Bad region value")
    }

});