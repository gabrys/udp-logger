#!/usr/bin/env python3

'''
Simple udp-logger client:

udp-log.py key=value key1=value1
'''

import json
import socket
import sys


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 10000


data = dict([arg.split('=', 1) for arg in sys.argv[1:] if '=' in arg])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (SERVER_HOST, SERVER_PORT)
sock.sendto(json.dumps(data).encode('utf-8'), server_address)
