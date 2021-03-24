#!/usr/bin/env python3
import socket, argparse
import circuit, ot

# evaluator (client)
# test.py executes this script and reads its exit code
# and last line of output (the calculation result)

parser = argparse.ArgumentParser()
parser.add_argument("CIRCUIT", type=str,
					help="circuit file to evaluate (Bristol Fashion)")
parser.add_argument("INPUT", type=int,
					help="second input to circuit file (integer)")
parser.add_argument("-p", "--port", dest="port",
					type=int, default=65432,
					help="garbler's port (default: 65432)")
parser.add_argument("-a", "--addr", dest="address",
					type=str, default="127.0.0.1",
					help="garbler's IP or hostname (default: 127.0.0.1)")
args = parser.parse_args()

print("  --  Bob  --\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((args.address, args.port))

	print("Reading circuit file")
	c = circuit.read_from_file(args.CIRCUIT)

	print("Receiving Alice's input")
	inputs = circuit.get_garbler_input(s, c)

	print("OT-ing my input...")
	inputs += circuit.get_evaluator_input(s, c, args.INPUT)

	print("Evaluating circuit...")
	result = circuit.evaluate(s, c, inputs)

	print(f"Result:\n{result}")
