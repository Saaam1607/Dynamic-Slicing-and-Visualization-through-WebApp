const express = require('express');
const app = express();
const bodyParser = require("body-parser");
const request = require("request");

// URL sito: http://192.168.56.2:8081
PORT = 8081;

app.use(express.static('public'));

var options = {
    method: 'GET',
    url: 'http://192.168.56.2:8080/stats/switches',
    headers: {
      'Content-Type': 'application/json'
    }
};
request(options, function (error, response, body) {
    if (error) throw new Error(error);
    var switches = JSON.parse(body);
    console.log(switches);
});

// Used to parse the JSON data in the request body
app.use(bodyParser.json());

app.post('/api/v1/sosScenario', function(req, res) {
});

app.post('/api/v1/standardScenario', function(req, res) {
});

app.listen(PORT, function() {
    console.log('Server is listening on Port: ', PORT);
});
