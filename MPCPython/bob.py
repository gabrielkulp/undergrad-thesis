#!/usr/bin/env python3
import socket
import ot

# client

host = '127.0.0.1'
port = 65432

print("  --  Bob  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((host, port))

	choice = 0

	print("Requesting message", choice)

	m = ot.receive(s, choice)

	if m:
		print(f"Received \"{m.decode()}\"")
	else:
		print("Error!")
