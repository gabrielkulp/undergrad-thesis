#!/usr/bin/env python3
import socket, sys
import circuit, ot

# garbler (server)
# test.py executes this script and reads its exit code

host = "0.0.0.0"
port = 65432
circuit_name  = sys.argv[1]
circuit_input = int(sys.argv[2])

print("  --  Alice  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((host, port))
	sock.listen()
	print("Listening...")
	conn, addr = sock.accept()

	with conn as s:
		print("Reading circuit file...")
		c = circuit.read_from_file(circuit_name)

		print("Generating input labels...")
		gc = circuit.garble(c)

		print("Garbling my own inputs...")
		garbled_inputs = circuit.garble_first_input(gc, circuit_input)

		print("Sending my inputs...")
		circuit.send_garbler_input(s, garbled_inputs)

		print("OT-ing Bob's inputs...")
		circuit.send_evaluator_input(s, gc)
		
		print("Generating and sending ctxts...")
		circuit.send_garbled_gates(s, gc)

		s.recv(1) # listen for client close
		print("Done!")
