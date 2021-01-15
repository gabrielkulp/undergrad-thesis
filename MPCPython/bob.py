#!/usr/bin/env python3
import socket
import ot

# client

host = '127.0.0.1'
port = 65432

print("\x1b[2J\x1b[H" + "  --  Bob  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((host, port))

	m = ot.receive(s, 0)

	if m:
		print("Decoded:", m.decode())
