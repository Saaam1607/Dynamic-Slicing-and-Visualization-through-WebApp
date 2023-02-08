#!/bin/sh

# S1
sudo ovs-vsctl -- \ 
set port s1-eth1 qos=@newqos -- \
set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:queue1=@q1 \
queues:queue2=@q2 -- \
--id=@q1 create queue other-config:min-rate=1000000 other-config:max-rate=10000000 -- \
--id=@q2 create queue other-config:min-rate=1000000 other-config:max-rate=10000000
# S2
sudo ovs-vsctl -- \ 
set port s2-eth1 qos=@newqos -- \
set port s2-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:queue1=@q1 \
--id=@q1 create queue other-config:min-rate=1000000 other-config:max-rate=10000000
# S3
sudo ovs-vsctl -- \ 
set port s1-eth1 qos=@newqos -- \
set port s1-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:queue1=@q1 \
queues:queue2=@q2 -- \
--id=@q1 create queue other-config:min-rate=1000000 other-config:max-rate=10000000 -- \
--id=@q2 create queue other-config:min-rate=1000000 other-config:max-rate=10000000
# S4
sudo ovs-vsctl -- \ 
set port s4-eth1 qos=@newqos -- \
set port s4-eth2 qos=@newqos -- \
--id=@newqos create QoS type=linux-htb \
other-config:max-rate=20000000 \
queues:queue2=@q2 -- \
--id=@q2 create queue other-config:min-rate=1000000 other-config:max-rate=10000000

# h1 deve raggiungere h4, utilizzando q1
# h2 deve raggiungere h5, utilizzando q2
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.4,idle_timeout=0,actions=set_queue:queue1,normal
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.1,idle_timeout=0,actions=set_queue:queue1,normal
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.2,idle_timeout=0,actions=set_queue:queue2,normal
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.5,idle_timeout=0,actions=set_queue:queue2,normal

# droppiamo altre combinazioni
# SRC h1
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.3,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.5,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.1,nw_dst=10.0.0.6,idle_timeout=0,actions=drop
# SRC h2
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.3,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.4,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.2,nw_dst=10.0.0.6,idle_timeout=0,actions=drop
# SRC h3
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.4,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.5,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.3,nw_dst=10.0.0.6,idle_timeout=0,actions=drop
# SRC h4
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.3,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.5,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.4,nw_dst=10.0.0.6,idle_timeout=0,actions=drop
# SRC h5
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.3,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.4,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.5,nw_dst=10.0.0.6,idle_timeout=0,actions=drop
# SRC h6
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.1,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.2,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.3,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.4,idle_timeout=0,actions=drop
sudo ovs-ofctl add-flow r1 ip,priority=65500,nw_src=10.0.0.6,nw_dst=10.0.0.5,idle_timeout=0,actions=drop


