from socket import socket
import ot
from .circuit import Circuit, GarbledCircuit, GateType, hash_pair, c_idx, int_to_wires, wires_to_int

def get_garbler_input(sock: socket, circuit: Circuit):
	inputs = [int.from_bytes(sock.recv(16), "big") for _ in range(circuit.input_sizes[0])]
	return inputs


def get_evaluator_input(sock: socket, circuit: Circuit, circuit_input: int):
	inputs = [None] * circuit.input_sizes[1]
	wires = int_to_wires(circuit_input, circuit.input_sizes[1])
	for i in range(circuit.input_sizes[1]):
		choice = wires[i]
		inputs[i] = ot.receive(sock, choice)
	return inputs

def evaluate(sock: socket, circuit: Circuit, input_wires: list[int]):
	active_labels = input_wires

	active_labels += [None] * circuit.gate_count

	# instantiate ciphertext generator
	# (will come from network later)
	next_ctxt = lambda: (
		int.from_bytes(sock.recv(16), "big"),
		int.from_bytes(sock.recv(16), "big"),
		int.from_bytes(sock.recv(16), "big")
	)

	for gate in circuit.gates():
		if gate.type == GateType.XOR:
			A = active_labels[gate.inputs[0]]
			B = active_labels[gate.inputs[1]]
			out_label = A ^ B
			active_labels[gate.id] = out_label

		elif gate.type == GateType.AND:
			table = next_ctxt()
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

	# now get the output map from the same connection
	result = list()

	for label in range(circuit.first_output, circuit.wire_count):
		label_hash = int.from_bytes(sock.recv(16), "big")
		if hash(active_labels[label]) == label_hash:
			result.append(0)
		else:
			result.append(1)

	return wires_to_int(result, circuit.output_size)
