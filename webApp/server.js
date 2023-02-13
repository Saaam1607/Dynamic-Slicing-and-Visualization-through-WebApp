const express = require('express');
const app = express();
const bodyParser = require("body-parser");

// URL sito: http://192.168.56.2:8081
PORT = 8081;

app.use(express.static('public'));

// Used to parse the JSON data in the request body
app.use(bodyParser.json());

app.post('/api/v1/sosScenario', function(req, res) {
});

app.post('/api/v1/standardScenario', function(req, res) {
});

app.listen(PORT, function() {
    console.log('Server is listening on Port: ', PORT);
});
