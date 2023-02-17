# On Demand SDN Slices in ComNetsEmu
Project for the course "Softwarized and Virtualized Mobile Networks" at the University of Trento

**Samuel Casagrande Cecchin** - [s.casagrande.cecchin@studenti.unitn.it](s.casagrande.cecchin@studenti.unitn.it)

**Davide De Martini** - [davide.demartini@studenti.unitn.it](davide.demartini@studenti.unitn.it)

**Stefano Sacchet** - [stefano.sacchet@studenti.unitn.it](stefano.sacchet@studenti.unitn.it)

## Table of Contents
- [On Demand SDN Slices in ComNetsEmu](#on-demand-sdn-slices-in-comnetsemu)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Project description](#project-description)
  - [Access web application outside vagrant](#access-web-application-outside-vagrant)
  - [Project structure](#project-structure)
  - [Introduction](#introduction)
    - [How to run the project](#how-to-run-the-project)
    - [Default Scenario](#default-scenario)
    - [Bottom Critical Scenario](#bottom-critical-scenario)
    - [Upper Critical Scenario](#upper-critical-scenario)
    - [Full Critical Scenario](#full-critical-scenario)
  - [Web App fuctionalities](#web-app-fuctionalities)
  - [Testing the network](#testing-the-network)
  - [Known Issues](#known-issues)

## Requirements
- Vagrant
- VirtualBox
- NodeJS
- NPM
- Python3
- Mininet
- Ryu
- ComNetsEmu

## Project description
**GOAL:** to implement a network slicing approach to enable dynamic activation/de-activation of network slices via GUI commands.

The ComNetsEmu framework is used to implement the network and Ryu for the SDN controller.

## Access web application outside vagrant
In order to have the web server running inside the vagrant machine a private network between the host machine and the vagrant machine must be created. This can be done by following the steps below:

1) Exit the vagrant machine
2) Add this line to the vagrant file 
   ```BASH
   config.vm.network "private_network", ip: "192.168.56.2"
   ```
3) Run `vagrant reload`
4) Run `vagrant ssh`
5) Now a new ip address is assigned to the vagrant machine. The ip address will be used to access the web application from outside the vagrant machine

## Project structure
The project is structured in two main folders:
- The folder`OnDemandSlicing` contains the code of the ryu controller, the topology and the topology visualizer
- The folder `Web App` contains the web application that displays the topology and allows the user to switch between different scenarios.
```
├── [OnDemandSlicing]
|    ├── [html]
|    ├── [sh_scripts]
|    |    ├── bothCritical.sh
|    |    ├── default.sh
|    |    ├── lowerCritical.sh
|    |    ├── reset.sh
|    |    └── upperCritical.sh
|    ├── controller.py
|    ├── gui_start.py
|    ├── launcher.sh
|    └── topology.py
├── [images]
|    ├── [Iperf]
|    ├── [Pingall]
|    ├── [Scenarios]
|    └── [webapp]
└── [webApp]
     ├── [public]
     │    ├── [images]
     │    ├── home.html
     │    ├── homeStyle.css
     │    ├── index.html
     │    ├── loginStyle.css
     │    ├── script.js
     │    ├── snake
     │    └── spaceGame
     ├── package.json      
     └── server.js
```

## Introduction

### How to run the project
In order to run the project follow these steps:
```BASH
cd ~/ProgettoNet2
vagrant up
vagrant ssh
```
Once accessed the vagrant machine, run the following commands (to install all packages needed for the web app):
```BASH
cd ~/ProgettoNet2/webApp
npm install
```
Then run the web app:
```BASH
node server.js
```
Once the web app is running, open a browser and go to the following address to access the web app:
```BASH
http://192.168.56.2:8081
```

<!-- Once accessed the vagrant machine, run the following commands (for the mininet simulation):
```BASH
cd OnDemandSlicing
sudo python3 topology.py
```
In another window run the following commands (for the controller):
```BASH
cd ~/ProgettoNet2
vagrant ssh
cd OnDemandSlicing
ryu-manager --observe-links gui_start.py controller.py
```
In another window we run the following commands (for the web app):
```BASH
cd ~/ProgettoNet2
vagrant ssh
cd WebApp
sudo apt install nodejs
sudo apt install npm
npm install
node server.js
``` -->

### Default Scenario

![image](images/Scenarios/defaultScenario.png)

In the default scenario there are 4 hosts and 4 switches. Two slices are active:
- Upper slice with H1 and H4 using a 10 Mbps link
- Bottom slice with H2 and H% using a 10 Mbps link

Host H3, H6, H7 and H8 are not part of any slice and are not connected to any switch.

![image](images/Pingall/defaultScenarioPing.png)\
![image](images/Iperf/Default/1.png)\
![image](images/Iperf/Default/2.png)

### Bottom Critical Scenario
![image](images/Scenarios/bottomCritical.png)

In the lower critical scenario there are 6 hosts and 4 switches. Three slices are active:
- Upper slice with H1 and H4 using a 10 Mbps link
- H2 and H5 slice with a 3 Mbps link
- H3 and H6 slice with a 7 Mbps link
Host H7 and H8 are not part of any slice and are not connected to any switch.

![image](images/Pingall/lowerScenarioPing.png)\
![image](images/Iperf/LowerCritical/1.png)\
![image](images/Iperf/LowerCritical/2.png)\
![image](images/Iperf/LowerCritical/3.png)

### Upper Critical Scenario
![image](images/Scenarios/upperCritical.png)

In the upper critical scenario there are 6 hosts and 4 switches. Three slices are active:
- H1 and H4 slice wirh a 3 Mbps link
- H7 and H8 slice with a 7 Mbps link
- Bottom slice with H2 and H5 using a 10 Mbps link
Host H3 and H6 are not part of any slice and are not connected to any switch.

![image](images/Pingall/upperCriticalPing.png)\
![image](images/Iperf/UpperCritical/1.png)\
![image](images/Iperf/UpperCritical/2.png)\
![image](images/Iperf/UpperCritical/3.png)

### Full Critical Scenario
![image](images/Scenarios/fullCritical.png)

In the full critical scenario there are 8 hosts and 4 switches. Four slices are active:
- H1 and H4 slice wirh a 3 Mbps link
- H7 and H8 slice with a 7 Mbps link
- H2 and H5 slice with a 3 Mbps link
- H3 and H6 slice with a 7 Mbps link
All the hosts are connected.

![image](images/Pingall/fullCriticalPing.png)\
![image](images/Iperf/FullCritical/1.png)\
![image](images/Iperf/FullCritical/2.png)\
![image](images/Iperf/FullCritical/3.png)\
![image](images/Iperf/FullCritical/4.png)

## Web App fuctionalities
The Web App allows the user (ex. a network administrator) to switch between different scenarios and to see the topology of the network in real time. It requires at first a simple login with username and password: **admin**

Once the login has been performed, the user is redirected to the control page. On this page it is possible to start the network, switch between different scenarios and stop the network.

![wa2](images/webapp/wa2.jpeg)

## Testing the network

To test the network the mininet console can be used to perform some ping (for reachability tests) and iperf commands (for bandwidth tests).\
ping tests can be performed in these two ways:
```
mininet> h1 ping h2
```
```
mininet> pingall
```
iperf tests can be performed in these two ways:
```
mininet> h1 iperf h2
```
Of course h1 and h2 can be replaced with any other host in the network.

## Known Issues
* When trowing a command that do not autoterminate (like h1 ping h2) the web app functionalities stop working. In order to have the webapp working again, a restart is required.
