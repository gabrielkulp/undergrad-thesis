#!/usr/bin/env python3
import socket
import circuit

# server

host = '127.0.0.1'
port = 65432

print("  --  Alice  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
	sock.bind((host, port))
	sock.listen()
	conn, addr = sock.accept()

	with conn as s:
		print("Reading circuit file...")
		c = circuit.read_from_file("divide64.txt")

		print("Generating input labels...")
		gc = circuit.garble(c)

		print("Garbling my own inputs...")
		garbled_inputs = circuit.garble_inputs(gc, [-234, 43])

		#print("OT-ing Bob's inputs...")

		print("Sending my inputs...")
		for inp in garbled_inputs:
			s.sendall(inp.to_bytes(16, "big"))

		print("Generating and sending ctxts...")
		ctxts = gc.ctxts()
		for ctxt in ctxts:
			if ctxt == None:
				s.sendall(bytes(16))
				break
			s.sendall(ctxt[0].to_bytes(16, "big"))
			s.sendall(ctxt[1].to_bytes(16, "big"))
			s.sendall(ctxt[2].to_bytes(16, "big"))

		print("Generating and sending output map...")
		output_map = next(ctxts)

		for output in output_map:
			s.sendall(output.to_bytes(16, "big"))
		
		s.recv(1) # listen for client close
		print("Done!")
