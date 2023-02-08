#!/usr/bin/python3

from comnetsemu.cli import CLI
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

from subprocess import check_output

# OBBIETTIVO DEL PROGRAMMA: creazione dell'infrastruttura di rete sssssssssssssssssssssssssssssssssicuramente

def topology():
    
    net = Containernet(controller=Controller, link=TCLink, xterms=False)

    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding hosts\n")
    h1 = net.addDockerHost(
        'h1',
        dimage="dev_test",
        ip='10.0.0.11/24',
        docker_args={"hostname": "h1"} # :O :(
    )
    h2 = net.addDockerHost(
        "h2",
        dimage="dev_test",
        ip="10.0.0.12/24",
        docker_args={"hostname": "h2"}
    )
    h3 = net.addDockerHost(
        "h3",
        dimage="dev_test",
        ip="10.0.0.13/24",
        docker_args={"hostname": "h3"}
    )
    h4 = net.addDockerHost(
        "h4",
        dimage="dev_test",
        ip="10.0.0.14/24",
        docker_args={"hostname": "h4"}
    )
    h5 = net.addDockerHost(
        "h5",
        dimage="dev_test",
        ip="10.0.0.15/24",
        docker_args={"hostname": "h5"}
    )
    h6 = net.addDockerHost(
        "h6",
        dimage="dev_test",
        ip="10.0.0.16/24",
        docker_args={"hostname": "h6"}
    )

    info("*** Adding switch\n")
    for i in range(2):
        sconfig = {"dpid": "%016x" % (i + 1)}
        net.addSwitch("s%d" % (i + 1), **sconfig)

    s1 = net.get("s1")
    s2 = net.get("s2")
    
    info("*** Creating links\n")
    net.addLink(h1, s1, bw=10)
    net.addLink(s1, h2, bw=10)
    net.addLink(h3, s1, bw=10)
    net.addLink(h4, s2, bw=10)
    net.addLink(h5, s2, bw=10)
    net.addLink(h6, s2, bw=10)
    net.addLink(s1, s2, bw=10)

    info("*** Starting network\n")
    net.start()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


topos = {"topology": (lambda: topology())}

if __name__ == "__main__": # effetto: il codice verrà eseguito solo quando il programma verrà eseguito come uno script (ex. da terminale)
    print("culone")  # stampa di controllo

    check_output("sudo mn -c", shell=True) # pulizia del mininet
    try:
        check_output("docker kill h1 h2 h3 h4 h5 h6", shell=True)
    except Exception:
        print("Error closing containers")

    topology()
