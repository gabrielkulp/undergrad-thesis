#!/usr/bin/env python3
import socket, sys
import circuit, ot

# evaluator (client)
# test.py executes this script and reads its exit code
# and last line of output (the calculation result)

host = "127.0.0.1"
port = 65432
circuit_name  = sys.argv[1]
circuit_input = int(sys.argv[2])

print("  --  Bob  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((host, port))

	print("Reading circuit file...")
	c = circuit.read_from_file(circuit_name)

	print("Receiving Alice's input...")
	inputs = circuit.get_garbler_input(s, c)
	
	print("OT-ing my input...")
	inputs += circuit.get_evaluator_input(s, c, circuit_input)
	
	print("Evaluating circuit...")
	result = circuit.evaluate(s, c, inputs)

	print(f"Result:\n{result}")
