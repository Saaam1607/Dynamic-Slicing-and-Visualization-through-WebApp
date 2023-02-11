#!/usr/bin/env bash

# run ryu controller
ryu-manager ~/ProgettoNet2/OnDemandSlicing/controller.py &
# sleep 1 second
sleep 1
# run mininet
sudo python3 ~/ProgettoNet2/OnDemandSlicing/topology.py
