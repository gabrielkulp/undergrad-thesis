#!/usr/bin/env python3
import socket
import circuit

# client

host = '127.0.0.1'
port = 65432

print("  --  Bob  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((host, port))

	print("Reading circuit file...")
	c = circuit.read_from_file("divide64.txt")

	print("Receiving Alice's input...")
	inputs = [None] * sum(c.input_counts)
	for i in range(sum(c.input_counts)):
		inputs[i] = int.from_bytes(s.recv(16), "big")

	#print("OT-ing my input...")

	print("Evaluating circuit...")
	result = circuit.evaluate(s, c, inputs)

	print("Result:", result)
