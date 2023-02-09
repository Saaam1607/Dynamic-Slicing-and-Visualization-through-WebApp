const express = require("express");
const app = express();
const path = require("path");

PORT = 8080;

app.get("/", function(req, res) {
    var options = {
        root: path.join(__dirname)
    };
     
    var fileName = "index.html";
    res.sendFile(fileName, options, function (err) {
        if (err) {
            next(err);
        } else {
            console.log('Sent:', fileName);
        }
    });
  });

app.listen(PORT, function(err) {
    if (err) console.log(err);
    console.log("Server listening on PORT", PORT);
});
