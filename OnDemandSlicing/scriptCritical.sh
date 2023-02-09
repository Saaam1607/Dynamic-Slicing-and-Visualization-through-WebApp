#!/bin/sh

# S1-eth1
echo ' ---------------------------------------------- '
echo '*** Network Slicing: Creating 3 slices of 5, 5, 10 Mbps each ...'
echo 'Switch 1:'
sudo ovs-vsctl -- \
set port s1-eth1 qos=@newqos -- \
set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:123=@1q queues:234=@2q queues:345=@3q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=10000000

# S2
echo 'Switch 2:'
sudo ovs-vsctl -- \
set port s2-eth1 qos=@newqos -- \
set port s2-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:123=@1q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \


# S3
echo 'Switch 3:'
sudo ovs-vsctl -- \
set port s1-eth1 qos=@newqos -- \
set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:234=@2q queues:345=@3q -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=10000000

# S4
echo 'Switch 4:'
sudo ovs-vsctl -- \
set port s4-eth1 qos=@newqos -- \
set port s4-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:123=@1q queues:234=@2q queues:345=@3q -- \
--id=@1q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \
--id=@2q create queue other-config:min-rate=1000000 other-config:max-rate=5000000 -- \
--id=@3q create queue other-config:min-rate=1000000 other-config:max-rate=10000000

echo '*** End of Creating the Slices ...'
echo ' ---------------------------------------------- '

# [SWITCH 1]
# h1 -> p1 [h4] (123)
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.1,idle_timeout=0,actions=set_queue:123,output:1
# p1 [h4] -> p3 [h1] (123)
sudo ovs-ofctl add-flow s1 ip,priority=65500,in_port=1,idle_timeout=0,actions=set_queue:123,output:3
# h2 -> p2 [h5] (234)
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.2,idle_timeout=0,actions=set_queue:234,output:2
# h5 -> p4 [h2] (234)
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.5,idle_timeout=0,actions=set_queue:234,output:4
# h3 -> p2 [h6] (345)
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.3,idle_timeout=0,actions=set_queue:345,output:2
# h6 -> p5 [h3] (345)
sudo ovs-ofctl add-flow s1 ip,priority=65500,nw_src=10.0.0.6,idle_timeout=0,actions=set_queue:345,output:5

# [SWITCH 2]
sudo ovs-ofctl add-flow s2 ip,table=0,priority=65500,in_port=1,actions=set_queue:123,output:2
sudo ovs-ofctl add-flow s2 ip,table=0,priority=65500,in_port=2,actions=set_queue:123,output:1

# [SWITCH 3]
# h2 -> p2 [h5]
sudo ovs-ofctl add-flow s3 ip,table=0,priority=65500,nw_src=10.0.0.2,actions=set_queue:234,output:2
# h5 -> p1 [h2]
sudo ovs-ofctl add-flow s3 ip,table=0,priority=65500,nw_src=10.0.0.5,actions=set_queue:234,output:1
# h3 -> p2 [h6]
sudo ovs-ofctl add-flow s3 ip,table=0,priority=65500,nw_src=10.0.0.3,actions=set_queue:345,output:2
# h6 -> p1 [h3]
sudo ovs-ofctl add-flow s3 ip,table=0,priority=65500,nw_src=10.0.0.6,actions=set_queue:345,output:1

# [SWITCH 4]
# p3 [h4] -> p1 [h1] (123)
sudo ovs-ofctl add-flow s4 priority=65500,in_port=3,idle_timeout=0,actions=set_queue:123,output:1
# p1 [h1] -> p3 [h4] (123)
sudo ovs-ofctl add-flow s4 priority=65500,in_port=1,idle_timeout=0,actions=set_queue:123,output:3
# p4 [h5] -> p2 [h2]
sudo ovs-ofctl add-flow s4 priority=65500,in_port=4,idle_timeout=0,actions=set_queue:234,output:2
# h2 -> p4 [h5]
sudo ovs-ofctl add-flow s4 ip,table=0,priority=65500,nw_src=10.0.0.2,actions=set_queue:234,output:4
# p5 [h6] -> p2 [h3]
sudo ovs-ofctl add-flow s4 priority=65500,in_port=5,idle_timeout=0,actions=set_queue:345,output:2
# h3 -> p5 [h6]
sudo ovs-ofctl add-flow s4 ip,table=0,priority=65500,nw_src=10.0.0.3,actions=set_queue:345,output:5
