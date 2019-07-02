function searchInfos(search){
    let searchForm = new FormData();
    searchForm.append("search", search);
    let req = new XMLHttpRequest();
    req.open("POST", "/search");
    let section = document.getElementById("dialogBot");
    let firstChildNode = section.firstChild; //Sélection du premier enfant du noeud
    let wait = document.createElement("div"); //Création d'un div
    wait.className = "row col-12 col-sm-2 offset-sm-8 col-md-1 offset-md-11 shadow-sm boxbot rounded"; //ajout des classes au div.
    wait.id = "Wait"; //ajout de l'id wait au div.
    wait.innerHTML += '<img src="../static/img/wait.gif" alt="Wait" class="img-fluid float-right" width="40" />'; //ajout du gif de chargement.

    section.insertBefore(wait, firstChildNode);

    req.addEventListener("load", function () {
        upgradeContainer(req.responseText, user=false)
        document.getElementById("dialogBot").removeChild(document.getElementById("Wait"));
    });
    req.send(searchForm);
}

function initMap(receiveLat, receiveLng, div) {
    new google.maps.Map(document.getElementById(div), {
        center: {lat: receiveLat, lng: receiveLng},
        zoom: 15
        });
}

function upgradeContainer(receive, user = true) {
    let section = document.getElementById("dialogBot"); //Sélection de l'element dialogBot.
    let firstChildNode = section.firstChild; //Sélection du premier enfant du noeud.
    let contDiv = document.createElement("div"); //Création d'un element div.
    contDiv.className ="row col-12 p-1 offset-sm-0 col-sm-8 boxbot shadow-sm offset-sm-4 mb-3" //Ajout de toutes les classes
    section.insertBefore(contDiv, firstChildNode); //Ajout du div créer avant le premier enfant du noeud.
    let dialog = section.firstChild; //Sélection du div qui vient d'être créé.

    if (user){
        contDiv.classList.remove("boxbot","shadow-sm","offset-sm-4","mb-3"); //Supression des classes qui ne sont pas necessaire.
        let pDialog = document.createElement("p"); //Création d'un paragraphe.
        pDialog.className ="text-justify shadow-sm text-left rounded boxuser"; //Ajout des classes au paragraphe.
        pDialog.innerHTML = receive; //Ajout de receive dans le paragraphe au format HTML.
        dialog.appendChild(pDialog); //Ajout du paragraphe dans le Div

    }else if(user === false){
        let recvjson = JSON.parse(receive); //Utilisation de json parse pour formaté les données reçu au format Json
        contDiv.classList.remove("col-12", "p-1", "offset-sm-0", "col-sm-8"); //Supression des classes qui ne sont pas necessaire dans le div.

        if (recvjson.existAdress){
            let pDialog = document.createElement("p"); //Création d'un paragraphe
            pDialog.innerHTML += recvjson.phBotAdre + "<br /> <br />"; //Ajout de la phrase aléatoire du bot
            pDialog.innerHTML += recvjson.name +"<br />"; //Ajout du nom de ce qu'ont recherche(ex: openclassrom's)
            pDialog.innerHTML += recvjson.adress.num +" " + recvjson.adress.rue + "<br />"; //Ajout du numéro de l'adresse et de la rue
            pDialog.innerHTML += recvjson.adress.code_postale +" "+ recvjson.adress.ville + "<br />"; //Ajout du code postale et de la ville
            dialog.appendChild(pDialog); //Ajout du paragraphe dans le DIV

            let mapBot = document.createElement("div"); //Création d'un DIV qui continedra la MAP google
            let nameid = "map"+i; //Formatage du nom de l'id
            mapBot.id = nameid; //Ajout du nom de l'id
            mapBot.className= "shadow-sm rounded m-3"; // Ajout des classes
            mapBot.style= "width:100%; height:300px;"; //Ajout d'un style(dimension de la map)
            dialog.appendChild(mapBot);// Ajout du div dans le div

            if(recvjson.existWiki){
                let pDialog = document.createElement("p");//Création d'un paragraphe
                pDialog.innerHTML += recvjson.phBotWik + "<br /><br />"; //Ajout de la phrase du bot
                pDialog.innerHTML += recvjson.search_detail_wiki; // Ajout de la réponse wiki
                dialog.appendChild(pDialog); // Ajout du paragraphe dans le div.
            }else{
                let pDialog = document.createElement("p");//Création d'un paragraphe
                pDialog.innerHTML += recvjson.phBotWik;//Ajout de la phrase du bot
                dialog.appendChild(pDialog);
            }
            initMap(recvjson.lat, recvjson.lng, nameid); //Initialisation de la map
            i++;
        }else{
            let pDialog = document.createElement("p");//Création d'un paragraphe
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
    let search = form.elements.search.value; //récupération de l'information inseré par l'utilisateur
    upgradeContainer(search);//Affichage de la demand user dans sur le site
    searchInfos(search);// lancement de la recherche
    e.preventDefault(); //interrompt l'envoi de la requequte post.
    form.elements.search.value = "";// remise a 0 de la valeur du formulaire.
});