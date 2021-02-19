from .types import Circuit, _Gate, _GateType

# Bristol Fashion circuit format
# https://homes.esat.kuleuven.be/~nsmart/MPC/

def read_from_file(filename):
	with open(filename, "r") as f:
		# first line is the number of gates and the number of wires
		gate_count, wire_count = map(int, f.readline().split())

		
		# the next line is the number of input variables, followed by the
		# bit counts of each input. Then the same for outputs.
		input_counts  = tuple(map(int, f.readline().split()))[1:]
		output_counts = tuple(map(int, f.readline().split()))[1:]

		# then a newline to consume
		f.readline()

		# quick sanity check: input bits + gates should be wires
		if sum(input_counts) + gate_count != wire_count:
			raise ValueError("Circuit metadata is inconsistent")

		circuit = Circuit(input_counts, output_counts, gate_count, wire_count, list())

		# next come all the gates. One line per gate
		for _ in range(gate_count):
			line = f.readline().split()

			# the first two numbers are the input and output wire counts
			wires_in  = int(line[0])
			wires_out = int(line[1])
			
			# the MAND gate has multiple outputs but I don't implement it
			if wires_out != 1:
				raise NotImplementedError("Only gates with 1 output are allowed")

			# next we read 1 or 2 input wire IDs
			gate_inputs = tuple(map(int, line[2:2+wires_in]))
			
			# and the output wire ID is the gate ID
			gate_id     = int(line[-2])

			# then the line ends with the gate name. I also included
			# sanity checks on the input counts so I can assume they're
			# correct when garbling or evaluating the circuit later.
			if line[-1] == "XOR":
				gate_type = _GateType.XOR
				if wires_in != 2:
					raise ValueError("XOR gates have 2 inputs")

			elif line[-1] == "AND":
				gate_type = _GateType.AND
				if wires_in != 2:
					raise ValueError("AND gates have 2 inputs")

			elif line[-1] == "INV":
				gate_type = _GateType.INV
				if wires_in != 1:
					raise ValueError("INV gates have 1 input")
			
			elif line[-1] == "EQW":
				gate_type = _GateType.EQW
				if wires_in != 1:
					raise ValueError("EQW gates have 1 input")

			else:
				raise NotImplementedError(f"Unknown gate type: {line[-1]}")
			
			# now the gate has been fully defined, so add it to the list
			gate = _Gate(gate_type, gate_inputs, gate_id)
			circuit.gates.append(gate)

	return circuit