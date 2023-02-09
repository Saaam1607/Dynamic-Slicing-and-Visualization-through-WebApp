#!/usr/bin/env bash

# run ryu controller
ryu-manager controller.py &
# sleep 1 second
sleep 1
# run mininet
sudo python3 topology.py
