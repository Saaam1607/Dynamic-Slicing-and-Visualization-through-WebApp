#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink

class NetworkSlicingTopo(Topo):
    def __init__(self):
        Topo.__init__(self)

        hostConfig = dict(inNamespace=True)
        weakLink = dict(bw=1)
        strongLink = dict(bw=5)
        hostLink = dict()

        for i in range(3):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), **sconfig) # s1, s2, s3

        for i in range(4):
            self.addHost("h%d" % (i + 1), **hostConfig) # h1, h2, h3, h4

        self.addLink("h1", "s1", **hostConfig)
        self.addLink("h2", "s1", **hostConfig)
        self.addLink("h3", "s3", **hostConfig)
        self.addLink("h4", "s3", **hostConfig)

        self.addLink("s1", "s2", **strongLink) 
        self.addLink("s2", "s3", **weakLink)

topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__ == "__main__": 

    topo = NetworkSlicingTopo() 
    
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()
