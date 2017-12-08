#!/usr/bin/env python3

import datetime
import json
import socket
import sqlite3
import sys


LISTEN_HOST = '0.0.0.0'
LISTEN_PORT = 10000

SQLITE_DB = '/data/log.sqlite'
TABLE_DDL = 'CREATE TABLE log(created_at, category, data)'


conn = sqlite3.connect(SQLITE_DB)
cur = conn.cursor()


def log(category, data):
    now = datetime.datetime.utcnow().isoformat()
    cur.execute('INSERT INTO log (created_at, category, data) VALUES(?, ?, ?)', (
        now,
	category,
	json.dumps(data),
    ))
    conn.commit()

try:
    cur.execute(TABLE_DDL)
except sqlite3.OperationalError:
    pass
    
log('__system', {'msg': 'Starting udp-logger'})

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (LISTEN_HOST, LISTEN_PORT)
sock.bind(server_address)

print('Listening', file=sys.stderr)

while True:
    raw_data, address = sock.recvfrom(8192)
    try:
        data = json.loads(raw_data.decode('utf-8'))
    except (json.decoder.JSONDecodeError, UnicodeDecodeError):
        log('__system', {'msg': 'Malformed data from client', 'client_address': address})
        continue
    if type(data) is not dict:
        data = {}
    log('__default', data)

