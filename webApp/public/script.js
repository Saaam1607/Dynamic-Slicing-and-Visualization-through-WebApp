const USERNAME = 'admin';
const PASSWORD = 'admin';

function login(){

    username = document.getElementById("Username").value;
    password = document.getElementById("Password").value;

    if (username == USERNAME && password == PASSWORD){
        window.location.href = "home.html";
    }else{
        alert("Errore: Username o Password errati")
    }
}
