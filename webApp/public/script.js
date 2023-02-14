const USERNAME = 'admin';
const PASSWORD = 'admin';

// Location of topology images
const STD_TOPOLOGY = "images/scenario1.png";
const SOS_TOPOLOGY = "images/scenario2.png";

// var iframe = document.getElementById('networkInfo');
// var innerDoc = iframe.contentDocument || iframe.contentWindow.document;

// var button = innerDoc.getElementById('SaveSwitchs');
// button.parentNode.removeChild(button);
// button = innerDoc.getElementById('SaveHosts');
// button.parentNode.removeChild(button);
// button = innerDoc.getElementById('SaveLinks');
// button.parentNode.removeChild(button);

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

function startNetwork(){

    document.getElementById("start_stop").innerHTML = "Starting network...";

    document.getElementById("startNetwork").disabled = true;

    fetch('api/v1/startNetwork', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "start": true })
    })
    .then(resp => resp.json())
    .then(function(data) {
        if (data.success){
            //Enable buttons
            document.getElementById("start_stop").innerHTML = "Network started";

            document.getElementById("stopNetwork").disabled = false;

            document.getElementById("success-outlined").disabled = false;
            document.getElementById("danger-outlined").disabled = false;
            document.getElementById("resetBtn").disabled = false;
        }else{
            document.getElementById("start_stop").innerHTML = "Error starting network";
            document.getElementById("startNetwork").disabled = true; //Re-enable start button
        }
    });
}

function stopNetwork(){

    document.getElementById("start_stop").innerHTML = "Stopping network...";

    document.getElementById("stopNetwork").disabled = true;

    fetch('api/v1/stopNetwork', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "stop": true })
    })
    .then(resp => resp.json())
    .then(function(data) {
        if (data.success){
            document.getElementById("start_stop").innerHTML = "Network stopped";

            document.getElementById("startNetwork").disabled = false;

            document.getElementById("success-outlined").disabled = true;
            document.getElementById("success-outlined").checked = false;

            document.getElementById("danger-outlined").disabled = true;
            document.getElementById("danger-outlined").checked = false;

            document.getElementById("resetBtn").disabled = true;

        }else{
            document.getElementById("start_stop").innerHTML = "Error stopping network";
            document.getElementById("stopNetwork").disabled = false;
        }
    });
}

function stdScenario(){
    
    fetch('api/v1/stdScenario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
        body: JSON.stringify({ "sos": false })
    })
    .then(resp => resp.json())
    .then(function(data) {
        if (data.success){
            document.getElementById("topology").src = STD_TOPOLOGY;
        }else{
            document.getElementById("start_stop").innerHTML = "Error changing topology. Restart network";
            document.getElementById("success-outlined").checked = false;
        }
    });
}

function sosScenario(){
    
    console.log("SOS Scenario");

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
            document.getElementById("topology").src = SOS_TOPOLOGY;
        }else{
            document.getElementById("start_stop").innerHTML = "Error changing topology. Restart network";
            document.getElementById("danger-outlined").checked = false;
        }
    });
}

function resetNetwork(){

    fetch('api/v1/resetNetwork', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
        body: JSON.stringify({ "reset": true })
    })
    .then(resp => resp.json())
    .then(function(data) {
        if (data.success){
            document.getElementById("start_stop").innerHTML = "Network resetted";
            document.getElementById("success-outlined").checked = false;
            document.getElementById("danger-outlined").checked = false;
        }else{
            document.getElementById("start_stop").innerHTML = "Error resetting network";
        }
    });
}

function logout(){
    console.log("Logout");
    window.location.href = "index.html";
}
