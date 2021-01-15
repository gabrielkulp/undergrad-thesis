#!/usr/bin/env python3
import socket
import ot

# server

host = '127.0.0.1'
port = 65432

print("\x1b[2J\x1b[H" + "  --  Alice  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host, port))
	s.listen()
	conn, addr = s.accept()
	#print("connection from", addr)

	with conn as c:
		m0 = "Hello".encode()
		m1 = "World".encode()
		
		ot.send(c, m0, m1)

		c.recv(1) # listen for client close
