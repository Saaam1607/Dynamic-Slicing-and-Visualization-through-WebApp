document.addEventListener("keydown", function(event) {
    if (event.keyCode === 13) {
        login()
    }
});

function login(){

    username = document.getElementById("Username").value;
    password = document.getElementById("Password").value;

    if (username == "admin" && password == "admin"){
        window.location.href = "home.html";
    } else{
        alert("Errore: Username o Password errati")
    }
}
