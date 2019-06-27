function searchInfos(search){
    let searchForm = new FormData();
    searchForm.append("search", search);
    let req = new XMLHttpRequest();
    req.open("POST", "/search");
    let section = document.getElementById("dialogBot");
    let selectLastP = section.firstChild;
    let wait = document.createElement("div");
    wait.className = "row col-12 col-sm-4 offset-sm-8 col-md-2 offset-md-10";
    wait.id = "Wait";
    section.insertBefore(wait, selectLastP);

    let divWait = section.firstChild;

    let pWait = document.createElement("div");
    pWait.className = "shadow-sm boxbot rounded";
    pWait.innerHTML += '<img src="../static/img/wait.gif" alt="Wait" class="img-fluid float-right" width="40" />';
    divWait.appendChild(pWait);

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
    if (user){
        let section = document.getElementById("dialogBot");
        let selectLastP = section.firstChild;
        let divDialogUser = document.createElement("div");
        divDialogUser.className ="row col-12 p-1 offset-sm-0 col-sm-8";
        
        section.insertBefore(divDialogUser, selectLastP);
    
        let pDialogUser = section.firstChild;
        let dialogUser = document.createElement("p");
        dialogUser.className ="text-justify shadow-sm text-left rounded boxuser";
        dialogUser.innerHTML = receive;
        pDialogUser.appendChild(dialogUser);
    }else if(user === false){
        let recvjson = JSON.parse(receive);
        let section = document.getElementById("dialogBot");
        let selectLastP = section.firstChild;
        let dialogBotMess = document.createElement("p");
        dialogBotMess.className = "row shadow-sm text-justify col-12 offset-sm-4 col-sm-8 boxbot rounded";

        if (recvjson.existAdress){
            dialogBotMess.innerHTML += recvjson.phBotAdre + "<br /> <br />";
            dialogBotMess.innerHTML += recvjson.name +"<br />";
            dialogBotMess.innerHTML += recvjson.adress.num +" " + recvjson.adress.rue + "<br />";
            dialogBotMess.innerHTML += recvjson.adress.code_postale +" "+ recvjson.adress.ville + "<br />";
            section.insertBefore(dialogBotMess, selectLastP);
            let lastP = section.firstChild;
            let mapBot = document.createElement("div");
            let nameid = "map"+i;
            mapBot.id = nameid;
            mapBot.className= "row shadow-sm rounded m-3";
            mapBot.style= "width:100%; height:300px;";
            lastP.appendChild(mapBot);
            if(recvjson.existWiki){
                dialogBotMess.innerHTML += recvjson.phBotWik + "<br /><br />";
                dialogBotMess.innerHTML += recvjson.search_detail_wiki;
                section.insertBefore(dialogBotMess, selectLastP);
            }else{
                dialogBotMess.innerHTML += recvjson.phBotWik;
                section.insertBefore(dialogBotMess, selectLastP);
            }
            initMap(recvjson.lat, recvjson.lng, nameid);
            i++;
        }else{
            dialogBotMess.innerHTML += recvjson.phBotAdre;
            section.insertBefore(dialogBotMess, selectLastP);
        }
    }
}

let form = document.querySelector("form");
let i = 0;
form.addEventListener("submit", function (e) {
    let search = form.elements.search.value;
    upgradeContainer(search);
    searchInfos(search);
    e.preventDefault();
    form.elements.search.value = "";
});