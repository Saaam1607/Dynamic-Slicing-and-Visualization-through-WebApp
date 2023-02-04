#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Basic example of service (running inside a APPContainer) migration.
"""

import os
import shlex
import time

from subprocess import check_output

from comnetsemu.cli import CLI
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller

def get_ofport(ifce: str):
    """Get the openflow port based on the iterface name.

    :param ifce (str): Name of the interface.
    """
    return (
        check_output(shlex.split("ovs-vsctl get Interface {} ofport".format(ifce)))
        .decode("utf-8")
        .strip()
    )


if __name__ == "__main__":

    # Only used for auto-testing.
    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    setLogLevel("info")

    net = Containernet(controller=Controller, link=TCLink, xterms=False)
    mgr = VNFManager(net)

    info("*** Add the default controller\n")
    net.addController("c0")

    info("*** Creating the client and hosts\n")
    h1 = net.addDockerHost( #host for client
        "h1",
        dimage="dev_test",
        ip="10.0.0.11/24",
        docker_args={"hostname": "h1"}
    )

    h2 = net.addDockerHost( #host for server
        "h2",
        dimage="dev_test",
        ip="10.0.0.12/24",
        docker_args={"hostname": "h2", "pid_mode": "host"},
    )
    h3 = net.addDockerHost( #host for server
        "h3",
        dimage="dev_test",
        ip="10.0.0.12/24",
        docker_args={"hostname": "h3", "pid_mode": "host"},
    )

    info("*** Adding switch and links\n")
    s1 = net.addSwitch("s1")
    net.addLinkNamedIfce(s1, h1, bw=1000, delay="5ms") #connect client to switch
    # Add the interfaces for service traffic.
    net.addLinkNamedIfce(s1, h2, bw=1000, delay="5ms") #connect server to switch
    net.addLinkNamedIfce(s1, h3, bw=1000, delay="5ms") #connect server to switch
    # Add the interface for host internal traffic (connection used to migrate the server).
    net.addLink(s1, h2, bw=1000, delay="1ms", intfName1="s1-h2-int", intfName2="h2-s1-int")
    net.addLink(s1, h3, bw=1000, delay="1ms", intfName1="s1-h3-int", intfName2="h3-s1-int")

    info("\n*** Starting network\n")
    net.start()

    s1_h1_port_num = get_ofport("s1-h1") #port of the interface that connects the client
    s1_h2_port_num = get_ofport("s1-h2") #port of the interface that connects the server
    s1_h3_port_num = get_ofport("s1-h3") #port of the interface that connects the server1
    h2_mac = h2.MAC(intf="h2-s1") #MAC address of the interface that connects the server
    h3_mac = h3.MAC(intf="h3-s1") #MAC address of the interface that connects the server

    h2.setMAC("00:00:00:00:00:12", intf="h2-s1") #set the MAC address of the interface that connects to the switch.
    h3.setMAC("00:00:00:00:00:12", intf="h3-s1")

    info("*** Use the subnet 192.168.0.0/24 for internal traffic between h2 and h3.\n")
    print("- Internal IP of h2: 192.168.0.12")
    print("- Internal IP of h3: 192.168.0.13")
    h2.cmd("ip addr add 192.168.0.12/24 dev h2-s1-int") #add the internal IP address of h2 to the interface that connects to the switch.
    h3.cmd("ip addr add 192.168.0.13/24 dev h3-s1-int") #add the internal IP address of h3 to the interface that connects to the switch.
    h2.cmd("ping -c 3 192.168.0.13") #h2 ping h3 to make sure the internal connection is working.

    # INFO: For the simplicity, OpenFlow rules are managed directly via
    # `ovs-ofctl` utility provided by the OvS.
    # For realistic setup, switches should be managed by a remote controller.
    info("*** Add flow to forward traffic from h1 to h2 to switch s1.\n")
    #check_output runs a shell command and returns the stdout of the command as a byte string.
    check_output(
        shlex.split( #shlex.split is used to split the string into a list of arguments that can be passed to the check_output function.
            'ovs-ofctl add-flow s1 "in_port={}, actions=output:{}"'.format(
                s1_h1_port_num, s1_h2_port_num #flow from h1 to h2
            )
        )
    )
    check_output(
        shlex.split(
            'ovs-ofctl add-flow s1 "in_port={}, actions=output:{}"'.format(
                s1_h2_port_num, s1_h1_port_num #flow from h2 to h1
            )
        )
    )
    check_output(
        shlex.split(
            'ovs-ofctl add-flow s1 "in_port={}, actions=output:{}"'.format(
                s1_h3_port_num, s1_h1_port_num #flow from h3 to h1
            )
        )
    )

    info("*** h1 ping 10.0.0.12 with 3 packets: \n") #ping from h1 to h2 ip
    ret = h1.cmd("ping -c 3 10.0.0.12")
    print(ret)

    info("*** Deploy counter service on h2.\n") #deploy server on h2
    counter_server_h2 = mgr.addContainer(
        "counter_server_h2", "h2", "service_migration", "python /home/server.py h2"
    )
    time.sleep(3)
    info("*** Deploy client app on h1.\n")
    client_app = mgr.addContainer(
        "client", "h1", "service_migration", "python /home/client.py"
    )
    time.sleep(10)
    client_log = client_app.getLogs()
    print("\n*** Setup1: Current log of the client: \n{}".format(client_log))

    info("*** Migrate (Re-deploy) the couter service to h3.\n") #migrate server from h2 to h3
    counter_server_h3 = mgr.addContainer(
        "counter_server_h3", "h3", "service_migration", "python /home/server.py h3 --get_state",
    )
    info("*** Send SEGTERM signal to the service running on the h2.\n"
         "Let it transfer its state through the internal network.\n"
    )
    pid_old_service = (
        check_output(shlex.split("pgrep -f '^python /home/server.py h2$'")) #check_outpu() runs a bash command and returns the output as a byte string
        .decode("utf-8") #decode from bytes to string
        .strip() #remove line breaks
    )
    for _ in range(3):
        check_output(shlex.split("kill {}".format(pid_old_service))) #send the SIGTERM signal to the old service
        # Wait a little bit to let the signal work.
        time.sleep(1)

    service_log = counter_server_h3.getLogs()
    print("\n*** Current log of the service on h3: \n{}".format(service_log))

    mgr.removeContainer("counter_server_h2")

    info("*** Mod the added flow to forward traffic from h1 to h3 to switch s1.\n")
    check_output(
        shlex.split(
            'ovs-ofctl mod-flows s1 "in_port={}, actions=output:{}"'.format(
                s1_h1_port_num, s1_h3_port_num #flow from h1 to h3
            )
        )
    )

    time.sleep(10)
    client_log = client_app.getLogs()
    print("\n*** Setup2: Current log of the client: \n{}".format(client_log))

    info("*** Migrate (Re-deploy) the couter service back to h2.\n")
    counter_server_h2 = mgr.addContainer(
        "counter_server_h2", "h2", "service_migration","python /home/server.py h2 --get_state",
    )
    pid_old_service = (
        check_output(shlex.split("pgrep -f '^python /home/server.py h3 --get_state$'"))
        .decode("utf-8")
        .strip()
    )
    print(f"The PID of the old service: {pid_old_service}")
    for _ in range(3):
        check_output(shlex.split("kill {}".format(pid_old_service)))
        # Wait a little bit to let the signal work.
        time.sleep(1)

    service_log = counter_server_h2.getLogs()
    print("\n*** Current log of the service on h2: \n{}".format(service_log))
    mgr.removeContainer("counter_server_h3")

    info("*** Mod the added flow to forward traffic from h1 back to h2 to switch s1.\n")
    check_output(
        shlex.split(
            'ovs-ofctl mod-flows s1 "in_port={}, actions=output:{}"'.format(
                s1_h1_port_num, s1_h2_port_num #flow from h1 to h2
            )
        )
    )

    time.sleep(10)
    client_log = client_app.getLogs()
    print("\n*** Setup3: Current log of the client: \n{}".format(client_log))

    if not AUTOTEST_MODE: #if AUTOTEST_MODE = 0 give the terminal to the user
        CLI(net)

    try:
        mgr.removeContainer("counter_server_h2")
        mgr.removeContainer("counter_server_h3")
    except Exception as e:
        print(e)
    finally:
        net.stop()
        mgr.stop()
