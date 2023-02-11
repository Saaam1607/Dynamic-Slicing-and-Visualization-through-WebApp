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
    // console.log(img)

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

function startNetwork(){
    
    document.getElementById("start_stop").innerHTML = "Starting network...";
    document.getElementById("startNetwork").disabled = true;
    document.getElementById("stopNetwork").disabled = false;

    // Call API to start network
    fetch('api/v1/startNetwork', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "start": true })
    })
    .then(resp => resp.json())
    .then(function(data) {

        setTimeout(function(){ //Timeout to simulate network start

        if (data.success){
            document.getElementById("danger-outlined").disabled = false; // sos button
            document.getElementById("start_stop").innerHTML = "Network started";
        }else{
            document.getElementById("start_stop").innerHTML = "Error: network not started";
            document.getElementById("startNetwork").disabled = false;
            document.getElementById("stopNetwork").disabled = true;
        }
        }, 3000);
    })
}

function stopNetwork(){

    document.getElementById("start_stop").innerHTML = "Stopping network...";
    document.getElementById("startNetwork").disabled = false;
    document.getElementById("stopNetwork").disabled = true;
    document.getElementById("danger-outlined").checked = false;
    document.getElementById("danger-outlined").disabled = true; // sos button

    // Switch to default topology
    document.getElementById("topology").src = STD_TOPOLOGY;

    // Call API to stop network
    fetch('api/v1/stopNetwork', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "stop": true })
    })
    .then(resp => resp.json())
    .then(function(data) {

        setTimeout(function(){ //Timeout to simulate network stop

        if (data.success){
            document.getElementById("start_stop").innerHTML = "Network stopped";
        }else{
            document.getElementById("start_stop").innerHTML = "Error: network not stopped";
        }
        }, 3000);
    });
}

function logout(){
    console.log("Logout");
    window.location.href = "index.html";
}
