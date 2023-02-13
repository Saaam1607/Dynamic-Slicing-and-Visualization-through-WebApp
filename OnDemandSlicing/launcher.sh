#!/usr/bin/env bash

#clear mininet
sudo mn -c
#sleep 1 second
sleep 1
# run ryu controller
ryu-manager ~/comnetsemu/progettoNet2/OnDemandSlicing/controller.py &
#sleep 1 second
sleep 1
#run mininet
cd ~/comnetsemu/progettoNet2/OnDemandSlicing
sudo python3 ~/comnetsemu/progettoNet2/OnDemandSlicing/topology.py
