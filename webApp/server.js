const express = require('express');
const app = express();
const bodyParser = require("body-parser");
const {spawn} = require('child_process');
const {exec} = require('child_process');

const launcherPath = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/launcher.sh'

// URL sito: http://192.168.56.2:8080
PORT = 8080;

// ID of the child process that will be spawned by the startNetwork API
PID = 0;

app.use(express.static('public'));

// Used to parse the JSON data in the request body
app.use(bodyParser.json());

app.post('/api/v1/startNetwork', function(req, res) {
    console.log('Start Network');
    // let data = req.body;
    // console.log(data);

    // Spawn a child process to run the launcher script
    const child = spawn("sh", [launcherPath]);

    // ID of the child process
    PID = child.pid;

    // Redirect the input from the terminal (parent) to the child
    process.stdin.pipe(child.stdin);

    // Handles the output of the child process
    child.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
    });
    
    child.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
    });
    
    child.on("close", (code) => {
        console.log(`child process exited with code ${code}`);
    });

    // Send command to the child process
    // child.stdin.write("nodes\n");

    if (child.pid){
        setTimeout(() => {
            res.status(200).json({
                success: true
            });
        }, 7000);
    }else{
        res.status(400).json({
            success: false
        });
    }
});

app.post('/api/v1/stopNetwork', function(req, res) {
    console.log('Stop Network');
    // let data = req.body;
    // console.log(data);

    // Send a kill signal to the child process
    exec(`kill -15 ${PID}`, (err, stdout, stderr) => {
        if (err){
            // some err occurred
            console.error(err)
            res.status(400).json({
                success: false
            });
        }else{
            // the *entire* stdout and stderr (buffered)
            // console.log(`stdout: ${stdout}`);
            // console.log(`stderr: ${stderr}`);
            res.status(200).json({
                success: true
            });
        }
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
