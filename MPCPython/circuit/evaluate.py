from .types import Circuit, GarbledCircuit, GateType
from .circuit import hash_pair, c_idx, int_to_wires, wires_to_int

def evaluate(gc: GarbledCircuit, inputs: list[int]):
	active_labels = list()

	for i,c in zip(inputs, gc.circuit.input_counts):
		input_wires = int_to_wires(i, c)
		for wire_value in input_wires:
			label_pair = gc.input_labels[len(active_labels)]
			active_labels.append(label_pair[wire_value])

	active_labels += [None] * gc.circuit.gate_count

	# instantiate ciphertext generator
	# (will come from network later)
	ctxts = gc.ctxts()

	for gate in gc.circuit.gates():
		if gate.type == GateType.XOR:
			A = active_labels[gate.inputs[0]]
			B = active_labels[gate.inputs[1]]
			out_label = A ^ B
			active_labels[gate.id] = out_label

		elif gate.type == GateType.AND:
			table = next(ctxts)
			A = active_labels[gate.inputs[0]]
			B = active_labels[gate.inputs[1]]
			color_idx = c_idx(A, B)
			if color_idx:
				active_labels[gate.id] = hash_pair(A, B) ^ table[color_idx-1]
			else:
				active_labels[gate.id] = hash_pair(A, B)

		elif gate.type == GateType.INV or gate.type == GateType.EQW:
			# INV swapped for free during garbling. Just treat as buffer
			active_labels[gate.id] = active_labels[gate.inputs[0]]

		else:
			raise NotImplementedError(f"Gate type {gate.type} not evaluated")

	# check that we hit the end of the ciphertexts
	assert next(ctxts) == None

	# now get the output map from the same connection
	output_map = next(ctxts)

	result = list()
	first_output_wire = gc.circuit.wire_count - sum(gc.circuit.output_counts)
	output_wires = range(first_output_wire, gc.circuit.wire_count)

	for (label_hash, label) in zip(output_map, output_wires):
		if hash(active_labels[label]) == label_hash:
			result.append(0)
		else:
			result.append(1)

	return wires_to_int(result, sum(gc.circuit.output_counts))
