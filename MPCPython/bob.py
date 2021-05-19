#!/usr/bin/env python3
import socket, argparse
import circuit, ot
from fpga import get_fpga

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
parser.add_argument("-n", "--no-fpga", dest="no_fpga", action='store_true',
					help="do not use the connected FPGA")
args = parser.parse_args()

print("  --  Bob  --\n")

fpga = None
if args.no_fpga:
	print("Ignoring FPGA")
else:
	fpga = get_fpga()

if fpga and not fpga.emu:
	print("Running with acceleration\n")
else:
	print("Running without acceleration\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((args.address, args.port))

	print("Reading circuit file")
	c = circuit.read_from_file(args.CIRCUIT)

	print("Receiving Alice's input")
	inputs_a = circuit.get_garbler_input(s, c, fpga)

	print("OT-ing my input...")
	inputs_b = circuit.get_evaluator_input(s, c, args.INPUT, fpga)

	print("Evaluating circuit...")
	inputs = []
	if inputs_a:
		inputs = inputs_a + inputs_b
	result = circuit.evaluate(s, c, inputs, fpga)

	print(f"Result:\n{result}")
