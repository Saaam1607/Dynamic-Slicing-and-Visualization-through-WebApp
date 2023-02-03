#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple server for counting.
"""

import argparse
import signal
import socket
import time

INTERNAL_IP_H2 = "192.168.0.12"
INTERNAL_IP_H3 = "192.168.0.13"
INTERNAL_PORT = 9999
SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888
HOST_NAME = None

def recv_state(host_name):
    """Get the latest counter state from the internal
    network between h2 and h3.
    """
    if host_name == "h2":
        recv_ip = INTERNAL_IP_H2
    else:
        recv_ip = INTERNAL_IP_H3
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((recv_ip, INTERNAL_PORT))

    state, _ = sock.recvfrom(1024)
    state = int(state.decode("utf-8"))
    return state


def run(host_name, get_state=False):
    """Run the counting service and handle sigterm signal."""
    counter = 0
    if get_state: #gets the state of the netwrok is the flag is set
        counter = recv_state(host_name)
        print("Get the init counter state: {}".format(counter))

    # Use closure to avoid using a global variable for state.
    def term_signal_handler(signum, frame): #handler of the SIGTERM signal used to migrate the host
        # Check if the server is running on the host 2.
        if host_name == "h2":
            dest_ip = INTERNAL_IP_H3
        else:
            dest_ip = INTERNAL_IP_H2
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #AF_INET: address domain of the socket(uses IPv4), SOCK_DGRAM: socket type (UDP)
        # Send duplicated packets to avoid losses.
        for _ in range(6):
            sock.sendto(str(counter).encode("utf-8"), (dest_ip, INTERNAL_PORT)) #send the counter to the other host
        sock.close()

    signal.signal(signal.SIGTERM, term_signal_handler)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVICE_IP, SERVICE_PORT)) #binds the socket to the SERVICE_IP and SERVICE_PORT that we want to listen on

    while True:
        # Block here waiting for data input.
        _, addr = sock.recvfrom(1024) #returns a tuple (data, address)
        counter += 1
        sock.sendto(str(counter).encode("utf-8"), addr) #send the counter to the client
        time.sleep(0.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple counting server.")
    parser.add_argument(
        "hostname", #you have to pass the hostname as the first argument
        type=str,
        help="The name of the host on which the server is deployed.",
    )
    parser.add_argument(
        "--get_state", action="store_true", help="Get state from network." #boolean flag, if you run the script with --get_state, the value of get_state will be True
    )

    args = parser.parse_args()

    run(args.hostname, args.get_state)
