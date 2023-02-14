const express = require('express');
const app = express();
const bodyParser = require("body-parser");
const request = require("request");
const {spawn} = require('child_process');
const {exec} = require('child_process');

// URL site: http://192.168.56.2:8081
const PORT = 8081;

const launcherPath = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/launcher.sh';
const stdScenario = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/script.sh';
const resetScript = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/reset.sh';
const sosScenario = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/scriptCritical.sh';

//PID of child process
PID = 0;

app.use(express.static('public'));

// Used to parse the JSON data in the request body
app.use(bodyParser.json());

app.use('/api/v1/startNetwork', function(req, res) {

    //Spawn child process to execute bash script
    const child = spawn('bash', [launcherPath]);

    //Get PID of child process
    PID = child.pid;

    //Redirect input from terminal (father) to child process
    process.stdin.pipe(child.stdin);

    //Redirect output from child process to terminal (father)
    child.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    child.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    //When child process terminates
    child.on('exit', function(code, signal) {
        console.log('Child terminated with code: ' + code);
    });

    if (child.pid){
        setTimeout(function(){
            res.json({success: true});
        }, 6000);
    }else{
        res.json({success: false});
    }
});

app.use('/api/v1/stopNetwork', function(req, res) {

    exec('kill ' + PID, (error, stdout, stderr) => {
        if (error) {
            console.error(`Errore: ${error.message}`);
            res.json({success: false});
        }else{
            console.log("Child process terminated");
            res.json({success: true});
        }
    });
});

app.post('/api/v1/stdScenario', function(req, res) {

    console.log("Standard scenario");

    //Reset network
    exec('bash ' + resetScript, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            res.json({success: false});
        }else{
            console.log(`Process output: ${stdout}`);
        }
    });

    //Start standard scenario
    exec('bash ' + stdScenario, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            res.json({success: false});
        }else{
            console.log(`Process output: ${stdout}`);
            res.json({success: true});
        }
    });
});

app.post('/api/v1/sosScenario', function(req, res) {

    console.log("SOS scenario");

    //Reset network
    exec('bash ' + resetScript, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            res.json({success: false});
        }else{
            console.log(`Process output: ${stdout}`);
        }
    });

    //Start sos scenario
    exec('bash ' + sosScenario, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }else{
            console.log(`Process output: ${stdout}`);
            res.json({success: true});
        }
    });
});

app.use('/api/v1/resetNetwork', function(req, res) {

    console.log("Reset network");

    //Reset network
    exec('bash ' + resetScript, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            res.json({success: false});
        }else{
            console.log(`Process output: ${stdout}`);
            res.json({success: true});
        }
    });
});

app.get('/api/v1/networkInfo', function(req, res) {
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
});

app.listen(PORT, function() {
    console.log('Server is listening on Port: ', PORT);
});
