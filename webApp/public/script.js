const USERNAME = 'admin';
const PASSWORD = 'admin';

function login(){

    let username = document.getElementById("Username").value;
    let password = document.getElementById("Password").value;

    if (username == USERNAME && password == PASSWORD){
        window.location.href = "home.html";
    }else{
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
            //Refresh iframe
            document.getElementById("networkInfo").src = document.getElementById("networkInfo").src;

            //Enable buttons
            document.getElementById("start_stop").innerHTML = "Network started";

            document.getElementById("stopNetwork").disabled = false;

            document.getElementById("stdScenario").disabled = false;
            document.getElementById("sos1").disabled = false;
            document.getElementById("sos2").disabled = false;
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

            document.getElementById("stdScenario").checked = false;
            document.getElementById("sos1").checked = false;
            document.getElementById("sos2").checked = false;

            document.getElementById("stdScenario").disabled = true;
            document.getElementById("sos1").disabled = true;
            document.getElementById("sos2").disabled = true;

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
            document.getElementById("start_stop").innerHTML = "Standard scenario";

            document.getElementById("stdScenario").disabled = true;
            document.getElementById("sos1").disabled = false;
            document.getElementById("sos2").disabled = false;

            document.getElementById("sos1").checked = false;
            document.getElementById("sos2").checked = false;
        }else{
            document.getElementById("start_stop").innerHTML = "Error changing topology. Restart network";
            document.getElementById("stdScenario").checked = false;
        }
    });
}

function critical(){
    let sos1 = document.getElementById("sos1");
    let sos2 = document.getElementById("sos2");

    if (sos1.checked && sos2.checked){
        bothCritical();
    }else if (sos1.checked){
        upperCritical();
    }else if (sos2.checked){
        lowerCritical();
    }
}

function upperCritical(){
    
    console.log("SOS upper critical scenario");

    fetch('api/v1/upperCritical', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "sos": true })
    })
    .then(resp => resp.json())
    .then(function(data) {
        if (data.success){
            document.getElementById("start_stop").innerHTML = "Upper critical scenario";

            document.getElementById("stdScenario").disabled = false;
            // document.getElementById("sos1").disabled = true;
            document.getElementById("sos2").disabled = false;

            document.getElementById("stdScenario").checked = false;
            // document.getElementById("sos2").checked = false;
        }else{
            document.getElementById("start_stop").innerHTML = "Error changing topology. Restart network";
            document.getElementById("sos1").checked = false;
        }
    });
}

function lowerCritical(){
    
    console.log("SOS lower critical scenario");

    fetch('api/v1/lowerCritical', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "sos": true })
    })
    .then(resp => resp.json())
    .then(function(data) {
        if (data.success){
            document.getElementById("start_stop").innerHTML = "Lower critical scenario";

            document.getElementById("stdScenario").disabled = false;
            document.getElementById("sos1").disabled = false;

            document.getElementById("stdScenario").checked = false;
        }else{
            document.getElementById("start_stop").innerHTML = "Error changing topology. Restart network";
            document.getElementById("sos2").checked = false;
        }
    });
}

function bothCritical(){
    console.log("SOS both critical scenario");

    fetch('api/v1/bothCritical', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "sos": true })
    })
    .then(resp => resp.json())
    .then(function(data) {
        if (data.success){
            document.getElementById("start_stop").innerHTML = "Both critical scenario";

            document.getElementById("stdScenario").disabled = false;
            document.getElementById("sos1").disabled = false;
            document.getElementById("sos2").disabled = false;
        }else{
            document.getElementById("start_stop").innerHTML = "Error changing topology. Restart network";
            document.getElementById("danger-outlined").checked = false;
        }
    });
}

function resetNetwork(){

    console.log("Reset network");

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

            document.getElementById("stdScenario").checked = false;
            document.getElementById("sos1").checked = false;
            document.getElementById("sos2").checked = false;
        }else{
            document.getElementById("start_stop").innerHTML = "Error resetting network";
        }
    });
}

function logout(){
    console.log("Logout");
    window.location.href = "index.html";
}
