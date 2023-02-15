#!/usr/bin/env python3

from mininet.topo import Topo
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.net import Mininet
from mininet.link import TCLink

from mininet.cli import CLI

import os

class OnDemandSlicingTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        link_config = {}
        switch_link_config = {}

        # Add switches
        for i in range(4):
            sconfig = {'dpid': "%016x" % (i + 1)}
            self.addSwitch('s%d' % (i + 1), **sconfig)
        # Add hosts
        for i in range(8):
            self.addHost('h%d' % (i + 1))
        
        # Add links for switch
        self.addLink('s1', 's2', **switch_link_config)
        self.addLink('s1', 's3', **switch_link_config)
        self.addLink('s2', 's4', **switch_link_config)
        self.addLink('s3', 's4', **switch_link_config)

        # Add links for host
        self.addLink('h1', 's1', **link_config)
        self.addLink('h2', 's1', **link_config)
        self.addLink('h3', 's1', **link_config)
        self.addLink('h4', 's4', **link_config)
        self.addLink('h5', 's4', **link_config)
        self.addLink('h6', 's4', **link_config)
        self.addLink('h7', 's1', **link_config)
        self.addLink('h8', 's4', **link_config)

topos = {'on_demand_slicing_topo': (lambda: OnDemandSlicingTopo())}

if __name__ == '__main__':
    
    topo = OnDemandSlicingTopo()
    net = Mininet(topo=topo, link=TCLink, controller=RemoteController('c0', ip='127.0.0.1'), switch=OVSKernelSwitch, build=False ,autoSetMacs=True, autoStaticArp=True)
    net.build()
    net.start()

    CLI(net)
    net.stop()
    os.system('sudo mn -c')
