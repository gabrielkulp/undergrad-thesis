#!/usr/bin/env python3
import socket
import ot

# server

host = '127.0.0.1'
port = 65432

print("  --  Alice  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host, port))
	s.listen()
	conn, addr = s.accept()

	with conn as c:
		m0 = "Hello"
		m1 = "World"

		print(f"Sending \"{m0}\" or \"{m1}\"")

		ot.send(c, m0.encode(), m1.encode())

		c.recv(1) # listen for client close

		print("Sent!")
