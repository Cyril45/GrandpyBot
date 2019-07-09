function searchInfos(search){
    let searchForm = new FormData(); //Création d'un objet FormData utilisé pour envoi de formulaire method post.
    searchForm.append("search", search); //Ajout du champ search et sa valeur.
    let req = new XMLHttpRequest(); //Création de l'objet qui permet de créer des requêtes HTTP.
    req.open("POST", "/search"); //Configuration de la requête type POST, l'URL
    let section = document.getElementById("dialogBot"); //Sélection de l'element dialogBot
    let firstChildNode = section.firstChild; //Sélection du premier enfant du noeud
    let wait = document.createElement("div"); //Création d'un div
    wait.className = "row col-12 col-sm-2 offset-sm-8 col-md-1 offset-md-11 shadow-sm boxbot rounded"; //Ajout des classes au div.
    wait.id = "Wait"; //Ajout de l'id wait au div.
    let waitImg = document.getElementById("waitImg"); //selection de l'image
    let clonewaitImg = waitImg.cloneNode(true); //clone de l'image
    clonewaitImg.style.display="block";//modification du style pour que l'image soit visible. 
    wait.appendChild(clonewaitImg);// ajout de l'image au div "wait"

    section.insertBefore(wait, firstChildNode);

    req.addEventListener("load", function () { //Événement de type load qui permet d'indiquer la fin du traitement de la requête, la fonction est exécuté à la fin du traitement.
        upgradeContainer(req.responseText, user=false)//Exécution de la fonction upgradeContainer, envoie du retour de la requête, au format JSON.
        document.getElementById("dialogBot").removeChild(document.getElementById("Wait"));//enlève l’élément Wait(Gif de chargement).
    });
    req.send(searchForm); //Envoi du formulaire dans de la requête HTTP(préconfiguré avec Open).
}

function initMap(receiveLat, receiveLng, div) {
    new google.maps.Map(document.getElementById(div), {
        center: {lat: receiveLat, lng: receiveLng},
        zoom: 15
        });
}

function upgradeContainer(receive, user = true) {
    let section = document.getElementById("dialogBot"); //Sélection de l’élément dialogBot.
    let firstChildNode = section.firstChild; //Sélection du premier enfant du noeud.
    let contDiv = document.createElement("div"); //Création d'un élément div.
    contDiv.className ="row col-12 p-1 offset-sm-0 col-sm-8 boxbot shadow-sm offset-sm-4 mb-3" //Ajout de toutes les classes
    section.insertBefore(contDiv, firstChildNode); //Ajout du div créé avant le premier enfant du nœud.
    let dialog = section.firstChild; //Sélection du div qui vient d'être créé.

    if (user){
        contDiv.classList.remove("boxbot","shadow-sm","offset-sm-4","mb-3"); //Suppression des classes qui ne sont pas nécessaires.
        let pDialog = document.createElement("p"); //Création d'un paragraphe.
        pDialog.className ="text-justify shadow-sm text-left rounded boxuser"; //Ajout des classes au paragraphe.
        pDialog.innerHTML = receive; //Ajout de receive dans le paragraphe au format HTML.
        dialog.appendChild(pDialog); //Ajout du paragraphe dans le Div.

    }else if(user === false){
        let recvjson = JSON.parse(receive); //Utilisation de json parse pour formater les données reçues au format Json.
        contDiv.classList.remove("col-12", "p-1", "offset-sm-0", "col-sm-8"); //Suppression des classes qui ne sont pas nécessaires dans le div.

        if (recvjson.existAdress){
            let pDialog = document.createElement("p"); //Création d'un paragraphe.
            pDialog.innerHTML += recvjson.phBotAdre + "<br /> <br />"; //Ajout de la phrase aléatoire du bot.
            pDialog.innerHTML += recvjson.name +"<br />"; //Ajout du nom de ce qu'on a recherché(ex: openclassrom's).
            pDialog.innerHTML += recvjson.adress.num +" " + recvjson.adress.rue + "<br />"; //Ajout du numéro de l'adresse et de la rue
            pDialog.innerHTML += recvjson.adress.code_postale +" "+ recvjson.adress.ville + "<br />"; //Ajout du code postale et de la ville
            dialog.appendChild(pDialog); //Ajout du paragraphe dans le DIV

            let mapBot = document.createElement("div"); //Création d'un DIV qui contiendra la MAP google
            let nameid = "map"+i; //Formatage du nom de l'id
            mapBot.id = nameid; //Ajout du nom de l'id
            mapBot.className= "shadow-sm rounded m-3"; //Ajout des classes
            mapBot.style= "width:100%; height:300px;"; //Ajout d'un style(dimension de la map)
            dialog.appendChild(mapBot); //Ajout du div dans le div

            if(recvjson.existWiki){
                let pDialog = document.createElement("p"); //Création d'un paragraphe
                pDialog.innerHTML += recvjson.phBotWik + "<br /><br />"; //Ajout de la phrase du bot
                pDialog.innerHTML += recvjson.search_detail_wiki; //Ajout de la réponse wiki
                dialog.appendChild(pDialog); //Ajout du paragraphe dans le div.
            }else{
                let pDialog = document.createElement("p"); //Création d'un paragraphe
                pDialog.innerHTML += recvjson.phBotWik; //Ajout de la phrase du bot
                dialog.appendChild(pDialog);
            }
            initMap(recvjson.lat, recvjson.lng, nameid); //Initialisation de la map
            i++;
        }else{
            let pDialog = document.createElement("p"); //Création d'un paragraphe
            pDialog.innerHTML = recvjson.phBotAdre;
            dialog.appendChild(pDialog);
        }
    }
    section.scrollLeft = 0;
    section.scrollTop = 0;
}

let form = document.querySelector("form");
let i = 0;
form.addEventListener("submit", function (e) {
    let search = form.elements.search.value; //Récupération de l'information insérée par l'utilisateur.
    upgradeContainer(search); //Affichage de la demande user dans sur le site.
    searchInfos(search); //Lancement de la recherche
    e.preventDefault(); //Interromps l'envoi du formulaire.
    form.elements.search.value = ""; //Remise à 0 de la valeur du formulaire.
});