const USERNAME = 'admin';
const PASSWORD = 'admin';

// Location of topology images
const STD_TOPOLOGY = "images/scenario1.png";
const SOS_TOPOLOGY = "images/scenario2.png";

function login(){

    let username = document.getElementById("Username").value;
    let password = document.getElementById("Password").value;

    if (username == USERNAME && password == PASSWORD){
        window.location.href = "home.html";
    }else{
        alert("Errore: Username o Password errati")
    }
}

function sosScenario(){
    // console.log("SOS Scenario");

    let img = document.getElementById("topology");
    let imgScenario = img.src.split("/").pop();
    // console.log(img)

    // Change topology
    let std_topology = STD_TOPOLOGY.split("/").pop();
    if (imgScenario == std_topology)
        img.src = SOS_TOPOLOGY;
    else
        img.src = STD_TOPOLOGY;
}

function startNetwork(){
    console.log("Start Network");

    document.getElementById("startNetwork").disabled = true;
    document.getElementById("stopNetwork").disabled = false;
    document.getElementById("danger-outlined").disabled = false; // sos button
}

function stopNetwork(){
    console.log("Stop Network");

    document.getElementById("startNetwork").disabled = false;
    document.getElementById("stopNetwork").disabled = true;
    document.getElementById("danger-outlined").disabled = true; // sos button

    // Switch to default topology
    document.getElementById("topology").src = STD_TOPOLOGY;
}

function logout(){
    console.log("Logout");
    window.location.href = "index.html";
}
