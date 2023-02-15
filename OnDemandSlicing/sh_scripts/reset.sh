#!/bin/sh

echo "Cleaning switches flow entries"
sudo ovs-ofctl --strict del-flows s1
sudo ovs-ofctl --strict del-flows s2
sudo ovs-ofctl --strict del-flows s3
sudo ovs-ofctl --strict del-flows s4