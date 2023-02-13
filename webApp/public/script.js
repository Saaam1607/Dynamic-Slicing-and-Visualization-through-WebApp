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
        // alert("Errore: Username o Password errati")

        // Reset input fields
        document.getElementById("Username").value = "";
        document.getElementById("Password").value = "";
        document.getElementById("Username").focus();
        document.getElementById("loginError").innerHTML = "Incorrect username or password";
    }
}

function changeScenario(){
    // console.log("SOS Scenario");

    let img = document.getElementById("topology");
    let imgScenario = img.src.split("/").pop();
    // console.log(img);

    // Change topology
    let std_topology = STD_TOPOLOGY.split("/").pop();
    if (imgScenario == std_topology){
        // Change to sos topology
        img.src = SOS_TOPOLOGY;

        fetch('api/v1/sosScenario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "sos": true })
        })
        .then(resp => resp.json())
        .then(function(data) {
            if (data.success){
                document.getElementById("start_stop").innerHTML = "SOS scenario";
            }
        });

    }else{
        // Change to standard topology
        img.src = STD_TOPOLOGY;

        fetch('api/v1/standardScenario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "sos": false })
            });
    }
}

function networkInfo(){
    
    fetch('http://192.168.56.2:8080/stats/switches', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(resp => resp.json())
    .then(function(data) {
        console.log(data);
    });
}

function logout(){
    console.log("Logout");
    window.location.href = "index.html";
}
