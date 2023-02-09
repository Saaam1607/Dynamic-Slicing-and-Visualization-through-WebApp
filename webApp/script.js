
function login(){

    username = document.getElementById("Username").value;
    password = document.getElementById("Password").value;
    // console.log(username);
    // console.log(password);

    if (username == "admin" && password == "admin"){
        window.location.href = "home.html";
    }
}
