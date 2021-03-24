import os # for generating wire labels with urandom
import aes
import random # for generating colors
import ot
from socket import socket
from .circuit import Circuit, GarbledCircuit, GateType, hash_pair, c_idx, int_to_wires


def send_garbler_input(sock: socket, gc: GarbledCircuit, inp: int):
	input_wires = int_to_wires(inp, gc.circuit.input_sizes[0])
	for wire_value, label_pair in zip(input_wires, gc.input_labels):
		active_label = label_pair[wire_value]
		sock.sendall(active_label.to_bytes(16, "big"))


def send_evaluator_input(sock: socket, gc: GarbledCircuit):
	for labels in gc.input_labels[gc.circuit.input_sizes[0]:]:
		ot.send(sock, labels[0], labels[1])


def garble(circuit: Circuit):
	# generate random labels
	_generate_wire_label = lambda: int.from_bytes(os.urandom(16), "little")

	# The secret difference between True and False labels.
	# Ensure color bit is set so T and F have opposite colors
	delta = _generate_wire_label() | 1

	# encapsulate delta in a function to invert wire labels
	inv_wire = lambda w: w^delta

	# generate input wire labels
	input_labels = list()
	for _ in range(sum(circuit.input_sizes)):
		label_f = _generate_wire_label()
		label_t = inv_wire(label_f)
		input_labels.append((label_f,label_t))

	# set up generator to produce ciphertexts
	ctxts = lambda: _garble_gates(circuit, input_labels, inv_wire)

	return GarbledCircuit(input_labels, circuit, ctxts)


def send_garbled_gates(sock: socket, gc: GarbledCircuit):
	ctxts = gc.ctxts()
	for ctxt in ctxts:
		sock.sendall(ctxt.to_bytes(16, "big"))


def _garble_gates(circuit, input_labels, inv_wire):
	# Build and reference array of label<->wire mappings.
	# Index in the array is wire ID, value is False label.
	labels = [None] * circuit.wire_count

	for i in range(sum(circuit.input_sizes)):
		labels[i] = input_labels[i][0] # add false label

	for gate in circuit.gates():
		# compute wire labels
		if gate.type == GateType.XOR:
			# free XOR means no hash/AES needed here!
			A_f = labels[gate.inputs[0]]
			B_f = labels[gate.inputs[1]]
			out_f  = A_f ^ B_f
			labels[gate.id] = out_f
			# no ctxt table to append

		elif gate.type == GateType.AND:
			# compute next ctxts in the array
			A_f = labels[gate.inputs[0]]
			B_f = labels[gate.inputs[1]]
			A_t  = inv_wire(A_f)
			B_t  = inv_wire(B_f)

			# find which ciphertext will come first
			hashes = (
				( hash_pair(A_f, B_f), c_idx(A_f, B_f) ),
				( hash_pair(A_f, B_t), c_idx(A_f, B_t) ),
				( hash_pair(A_t, B_f), c_idx(A_t, B_f) ),
				( hash_pair(A_t, B_t), c_idx(A_t, B_t) )
			)
			out_f = None
			out_t = None

			# find the one with index 0 and use it to
			# make the first ciphertext be 0 (row reduction)
			for i in range(3):
				if hashes[i][1] == 0:
					out_f = hashes[i][0]
					out_t = inv_wire(out_f)
					break
			if hashes[3][1] == 0:
				out_t = hashes[3][0]
				out_f = inv_wire(out_t)

			labels[gate.id] = out_f

			table = (
				( hashes[0][0] ^ out_f, hashes[0][1] ),
				( hashes[1][0] ^ out_f, hashes[1][1] ),
				( hashes[2][0] ^ out_f, hashes[2][1] ),
				( hashes[3][0] ^ out_t, hashes[3][1] )
			)
			sorted_table = sorted(table, key=lambda x: x[1])
			# don't append sorted colors, so just take first tuple element.
			# also don't append the first ctxt since it's zero
			for x in sorted_table[1:]:
				yield x[0]

		elif gate.type == GateType.INV:
			# semantically swap input label so evaluator can treat as buffer
			in_f = labels[gate.inputs[0]]
			labels[gate.id] = inv_wire(in_f)
			# no ciphertext to append

		elif gate.type == GateType.EQW:
			# buffer. Do nothing
			labels[gate.id] = labels[gate.inputs[0]]

		else:
			raise NotImplementedError(f"Gate type {gate.type} not garbled")

	# now generate the output map
	first_output_wire = circuit.wire_count - circuit.output_size
	for wire in range(first_output_wire, circuit.wire_count):
		# record mapping of output wire IDs to output labels
		yield hash(labels[wire])
