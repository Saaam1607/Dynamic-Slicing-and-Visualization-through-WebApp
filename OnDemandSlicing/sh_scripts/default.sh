#!/bin/sh

# S1
echo ' ---------------------------------------------- '
echo '*** Network Slicing: Creating 2 slices of 10 Mbps each ...'
echo 'Switch 1:'
sudo ovs-vsctl -- \
set port s1-eth1 qos=@newqos -- \
set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:123=@1q \
queues:234=@2q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=10000000 -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=10000000

# S2
echo 'Switch 2:'
sudo ovs-vsctl -- \
set port s2-eth1 qos=@newqos -- \
set port s2-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:123=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=10000000

# S3
echo 'Switch 3:'
sudo ovs-vsctl -- \
set port s1-eth1 qos=@newqos -- \
set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:234=@2q -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=10000000

# S4
echo 'Switch 4:'
sudo ovs-vsctl -- \
set port s4-eth1 qos=@newqos -- \
set port s4-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:123=@1q \
queues:234=@2q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=10000000 -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=10000000

echo '*** End of Creating the Slices ...'
echo ' ---------------------------------------------- '

# [SWITCH 1]
sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=3,idle_timeout=0,actions=set_queue:123,output:1
sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=1,idle_timeout=0,actions=set_queue:123,output:3
sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=4,idle_timeout=0,actions=set_queue:234,output:2
sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=2,idle_timeout=0,actions=set_queue:234,output:4
sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=5,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=6,idle_timeout=0,actions=drop


# [SWITCH 2]
sudo ovs-ofctl add-flow s2 table=0,priority=65500,in_port=1,actions=set_queue:123,output:2
sudo ovs-ofctl add-flow s2 table=0,priority=65500,in_port=2,actions=set_queue:123,output:1

# [SWITCH 3]
sudo ovs-ofctl add-flow s3 table=0,priority=65500,in_port=1,actions=set_queue:234,output:2
sudo ovs-ofctl add-flow s3 table=0,priority=65500,in_port=2,actions=set_queue:234,output:1

# [SWITCH 4]
sudo ovs-ofctl add-flow s4 ip,priority=65500,in_port=1,idle_timeout=0,actions=set_queue:123,output:3
sudo ovs-ofctl add-flow s4 ip,priority=65500,in_port=3,idle_timeout=0,actions=set_queue:123,output:1
sudo ovs-ofctl add-flow s4 ip,priority=65500,in_port=2,idle_timeout=0,actions=set_queue:234,output:4
sudo ovs-ofctl add-flow s4 ip,priority=65500,in_port=4,idle_timeout=0,actions=set_queue:234,output:2
sudo ovs-ofctl add-flow s4 ip,priority=65500,in_port=6,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow s4 ip,priority=65500,in_port=5,idle_timeout=0,actions=drop
