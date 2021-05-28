from socket import socket
import ot
from .circuit import Circuit, GarbledCircuit, GateType, hash_pair, c_idx, int_to_wires, wires_to_int
from fpga import FPGA, get_fpga, Cmd

def _to_addr(x): return x.to_bytes((x.bit_length()+7)//8, "little")[:2]
#fpga = get_fpga()


def get_garbler_input(sock: socket, circuit: Circuit, fpga: FPGA = None):
	if fpga:
		write_addr = 0
		for _ in range(circuit.input_sizes[0]):
			fpga.send_bytes(Cmd.addr, _to_addr(write_addr))
			data = sock.recv(16)
			fpga.send_bytes(Cmd.write, data)
			write_addr += 1
		return None
	else:
		inputs = [int.from_bytes(sock.recv(16), "little") for _ in range(circuit.input_sizes[0])]
		return inputs


def get_evaluator_input(sock: socket, circuit: Circuit, circuit_input: int, fpga: FPGA = None):
	wires = int_to_wires(circuit_input, circuit.input_sizes[1])
	
	if fpga:
		write_addr = circuit.input_sizes[0]
		for i in range(circuit.input_sizes[1]):
			choice = wires[i]
			fpga.send_bytes(Cmd.addr, _to_addr(write_addr))
			fpga.send_bytes(Cmd.write, ot.receive(sock, choice).to_bytes(16, "little"))
			write_addr += 1
		return None
	else:
		inputs = [None] * circuit.input_sizes[1]
		for i in range(circuit.input_sizes[1]):
			choice = wires[i]
			inputs[i] = ot.receive(sock, choice)
		return inputs


def evaluate(sock: socket, circuit: Circuit, input_wires: list[int], fpga: FPGA = None):
	if fpga:
		return _evaluate_fpga(sock, circuit, fpga)

	active_labels = input_wires

	active_labels += [None] * circuit.gate_count

	# instantiate ciphertext generator
	# (will come from network later)
	next_ctxt = lambda: (
		int.from_bytes(sock.recv(16), "little"),
		int.from_bytes(sock.recv(16), "little"),
		int.from_bytes(sock.recv(16), "little")
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

		elif gate.type == GateType.INV or gate.type == GateType.BUF:
			# INV swapped for free during garbling. Just treat as buffer
			active_labels[gate.id] = active_labels[gate.inputs[0]]

		else:
			raise NotImplementedError(f"Gate type {gate.type} not evaluated")

#	for label_idx in range(circuit.first_output):
#		print(active_labels[label_idx])


	# now get the output map from the same connection
	result = list()
	for label_idx in range(circuit.first_output, circuit.wire_count):
		label_hash = int.from_bytes(sock.recv(16), "little")
#		print(active_labels[label_idx])
		if hash(active_labels[label_idx]) == label_hash:
			result.append(0)
		else:
			result.append(1)

	return wires_to_int(result, circuit.output_size)

import time
def _evaluate_fpga(sock: socket, circuit: Circuit, fpga: FPGA):
	for gate in circuit.gates():
		if gate.type == GateType.XOR:
			fpga.send_bytes(Cmd.gates, b'\x01' +
				_to_addr(gate.inputs[0]) +
				_to_addr(gate.inputs[1]) +
				_to_addr(gate.id))
		elif gate.type == GateType.AND:
			fpga.send_bytes(Cmd.gates, b'\x00' +
				_to_addr(gate.inputs[0]) +
				_to_addr(gate.inputs[1]) +
				sock.recv(16) +
				sock.recv(16) +
				sock.recv(16) +
				_to_addr(gate.id))
		elif gate.type == GateType.INV or gate.type == GateType.BUF:
			fpga.send_bytes(Cmd.gates, b'\x02' +
			_to_addr(gate.inputs[0]) +
			_to_addr(gate.id))
		else:
			raise NotImplementedError(f"Gate type {gate.type} not evaluated")
		#time.sleep(.01)
	
	# now get results
#	for label_idx in range(circuit.first_output):
#		fpga.send_bytes(Cmd.addr, _to_addr(label_idx))
#		print(int.from_bytes(fpga.recv_bytes(Cmd.read, 16), "little"))
	result = list()
	for label_idx in range(circuit.first_output, circuit.wire_count):
		label_hash = int.from_bytes(sock.recv(16), "little")

		fpga.send_bytes(Cmd.addr, _to_addr(label_idx))
		label = int.from_bytes(fpga.recv_bytes(Cmd.read, 16), "little")
#		print(label)
		if hash(label) == label_hash:
			result.append(0)
		else:
			result.append(1)

	return wires_to_int(result, circuit.output_size)
