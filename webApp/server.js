const express = require('express');
const app = express();
const bodyParser = require("body-parser");
const {spawn} = require('child_process');
const {exec} = require('child_process');

// URL site: http://192.168.56.2:8081
const PORT = 8081;

const launcherPath = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/launcher.sh';
const stdScenario = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/sh_scripts/default.sh';
const upperCritical = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/sh_scripts/upperCritical.sh';
const lowerCritical = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/sh_scripts/lowerCritical.sh';
const bothCritical = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/sh_scripts/bothCritical.sh';
const resetScript = '/home/vagrant/comnetsemu/progettoNet2/OnDemandSlicing/sh_scripts/reset.sh';

//PID of child process
PID = 0;

function resetNetwork(){
    return new Promise((resolve, reject) => {
        var ok = false;
        exec('bash ' + resetScript, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error: ${error.message}`);
                reject(error);
            } else {
                console.log(`Process output: ${stdout}`);
                ok = true;
                resolve(ok);
            }
        });
    });
}

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
    resetNetwork();

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

app.post('/api/v1/upperCritical', function(req, res) {

    console.log("SOS upper critical scenario");

    //Reset network
    resetNetwork();

    //Start sos scenario
    exec('bash ' + upperCritical, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }else{
            console.log(`Process output: ${stdout}`);
            res.json({success: true});
        }
    });
});

app.post('/api/v1/lowerCritical', function(req, res) {

    console.log("SOS lower critical scenario");

    //Reset network
    resetNetwork();

    //Start sos scenario
    exec('bash ' + lowerCritical, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }else{
            console.log(`Process output: ${stdout}`);
            res.json({success: true});
        }
    });
});

app.use('/api/v1/bothCritical', function(req, res) {

    console.log("SOS both critical scenario");

    //Reset network
    resetNetwork();

    //Start sos scenario
    exec('bash ' + bothCritical, (error, stdout, stderr) => {
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
    resetNetwork()
        .then((ok) => {
            res.json({success: ok})
        })
        .catch((err) => {
            res.json({success: false})
        });
});

app.listen(PORT, function() {
    console.log('Server is listening on Port: ', PORT);
});
