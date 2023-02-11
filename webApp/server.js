const express = require('express');
const app = express();
const bodyParser = require("body-parser");

PORT = 8080;

app.use(express.static('public'));

// Used to parse the JSON data in the request body
app.use(bodyParser.json());

app.post('/api/v1/startNetwork', function(req, res) {
    console.log('Start Network');
    let data = req.body;
    console.log(data);
    res.status(200).json({
        success: true
    });
});

app.post('/api/v1/stopNetwork', function(req, res) {
    console.log('Stop Network');
    let data = req.body;
    console.log(data);
    res.status(200).json({
        success: true
    });
});

app.post('/api/v1/sosScenario', function(req, res) {
    console.log('SOS Scenario');
    let data = req.body;
    console.log(data);
    res.status(200).json({
        success: true
    });
});

app.post('/api/v1/standardScenario', function(req, res) {
    console.log('Standard Scenario');
    let data = req.body;
    console.log(data);
    res.status(200).json({
        success: true
    });
});

app.listen(PORT, function() {
    console.log('Server is listening on Port: ', PORT);
});
