#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
About: Simple client.
"""

import socket
import time

SERVICE_IP = "10.0.0.12"
SERVICE_PORT = 8888

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #AF_INET: address domain of the socket(uses IPv4), SOCK_DGRAM: socket type (UDP)
    data = b"Show me the counter, please!" #string converted to bytes

    while True:
        sock.sendto(data, (SERVICE_IP, SERVICE_PORT)) #address of the socket is a tuple SERVER_IP and SERVER_PORT
        counter, _ = sock.recvfrom(1024) #recieves packets from the socket, 1024 is the buffer size, sock.recvfrom() returns a tuple (data, address)
        print("Current counter: {}".format(counter.decode("utf-8")))
        time.sleep(1) #wait for 1 sec
