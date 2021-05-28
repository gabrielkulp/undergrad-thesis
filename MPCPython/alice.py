#!/usr/bin/env python3
import socket, argparse
import circuit, ot
from datetime import datetime

# garbler (server)
# test.py executes this script and reads its exit code

parser = argparse.ArgumentParser()
parser.add_argument("CIRCUIT", type=str,
					help="circuit file to evaluate (Bristol Fashion)")
parser.add_argument("INPUT", type=int,
					help="first input to circuit file (integer)")
parser.add_argument("-p", "--port", dest="port",
					type=int, default=65432,
					help="port to listen on (default: 65432)")
parser.add_argument("-a", "--addr", dest="address",
					type=str, default="0.0.0.0",
					help="address to listen on (default: 0.0.0.0)")
args = parser.parse_args()

print("  --  Alice  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
	listener.bind((args.address, args.port))
	listener.listen()
	print(f"Listening on {args.address}:{args.port}...")
	try:
		conn, addr = listener.accept()
	except KeyboardInterrupt:
		print(" Shutting down")
		exit()

	print(f"\nConnected to {addr[0]}:{addr[1]}")

	with conn as s:
		print("Reading circuit file")
		c = circuit.read_from_file(args.CIRCUIT)

		print("Generating input labels")
		gc = circuit.garble(c)

		print("Garbling and sending my inputs")
		circuit.send_garbler_input(s, gc, args.INPUT)

		print("OT-ing Bob's inputs...")
		circuit.send_evaluator_input(s, gc)

		print("Generating and sending ctxts...")
		circuit.send_garbled_gates(s, gc)

		s.recv(1) # listen for client close
		print("Done!")
