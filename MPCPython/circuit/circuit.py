import os # for generating wire labels with urandom
import aes
import random # for generating colors
from .types import Circuit, GarbledCircuit, _Gate, _GateType

# faster "hash" for testing
#hash = lambda x: ~x
#hash_pair = lambda x, y: (hash(x)) ^ (hash(y))

aes_keys  = aes.get_key_schedule(bytearray.fromhex("00000000000000000000000000000000"))
_to_bytes = lambda x: bytearray(x.to_bytes(16, "little"))
hash_pair = lambda x, y: int.from_bytes(aes.encrypt(aes_keys, _to_bytes(x^y)), "little")
c_idx     = lambda w1,w2: ((w1 & 1) << 1) | (w2 & 1)

_generate_wire_label = lambda: int.from_bytes(os.urandom(16), "little")


def garble(circuit: Circuit):
	# The secret difference between True and False labels.
	# Ensure color bit is set so T and F have opposite colors
	delta = _generate_wire_label() | 1
	# encapsulate delta in a function to invert wire labels
	inv_wire = lambda w: w^delta

	# Build and reference array of label<->wire mappings.
	# Index in the array is wire ID, value is False label.
	labels = [None] * circuit.wire_count

	# The garbled truth tables for all gates
	ctxts = list()

	# generate input wire labels
	input_labels = list()
	for i in range(sum(circuit.input_counts)):
		label_f = _generate_wire_label()
		label_t = inv_wire(label_f)
		labels[i] = label_f
		input_labels.append((label_f,label_t))

	for gate in circuit.gates:
		# compute wire labels
		if gate.type == _GateType.XOR:
			# free XOR means no hash/AES needed here!
			A_f = labels[gate.inputs[0]]
			B_f = labels[gate.inputs[1]]
			out_f  = A_f ^ B_f
			labels[gate.id] = out_f
			# no ctxt table to append

		elif gate.type == _GateType.AND:
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
			# don't append sorted colors, so just take first tuple element
			ctxts.append([x[0] for x in sorted_table[1:]])

		elif gate.type == _GateType.INV:
			# semantically swap input label so evaluator can treat as buffer
			in_f = labels[gate.inputs[0]]
			labels[gate.id] = inv_wire(in_f)
			# no ciphertext to append

		else:
			raise NotImplementedError(f"Gate type {gate.type} not garbled")

	output_map = list()
	first_output_wire = circuit.wire_count - sum(circuit.output_counts)
	
	for wire in range(first_output_wire, circuit.wire_count):
		# record mapping of output wire IDs to output labels
		output_map.append(hash(labels[wire]))
	return GarbledCircuit(input_labels, ctxts, output_map, circuit)


#def gc_send(sock: socket, gc: GarbledCircuit, input_1):
#	my_wires = int_to_wires(input_1, gc.circuit.input_counts[0])
#	my_inputs = [l[int(w)] for (l,w) in zip(gc.input_labels, my_wires)]
#	
#	sock.send(my_inputs)
#	# ot their wires
#	sock.send(gc.ctxts)
#	sock.send(gc.output_map)


def gc_evaluate(gc: GarbledCircuit, inputs: list[int]):
	active_labels = list()

	for i,c in zip(inputs, gc.circuit.input_counts):
		input_wires = int_to_wires(i, c)
		for wire_value in input_wires:
			label_pair = gc.input_labels[len(active_labels)]
			active_labels.append(label_pair[wire_value])

	active_labels += [None] * gc.circuit.gate_count

	ctxt_counter = 0
	for gate in gc.circuit.gates:
		if gate.type == _GateType.XOR:
			A = active_labels[gate.inputs[0]]
			B = active_labels[gate.inputs[1]]
			out_label = A ^ B
			active_labels[gate.id] = out_label


		elif gate.type == _GateType.AND:
			table = gc.ctxts[ctxt_counter]
			ctxt_counter += 1
			A = active_labels[gate.inputs[0]]
			B = active_labels[gate.inputs[1]]
			color_idx = c_idx(A, B)
			if color_idx:
				active_labels[gate.id] = hash_pair(A, B) ^ table[color_idx-1]
			else:
				active_labels[gate.id] = hash_pair(A, B)

		elif gate.type == _GateType.INV:
			# swapped for free during garbling. Just treat as buffer
			active_labels[gate.id] = active_labels[gate.inputs[0]]

		else:
			raise NotImplementedError(f"Gate type {gate.type} not evaluated")

	result = list()
	first_output_wire = gc.circuit.wire_count - sum(gc.circuit.output_counts)
	output_wires = range(first_output_wire, gc.circuit.wire_count)

	for (label_hash, label) in zip(gc.output_map, output_wires):
		if hash(active_labels[label]) == label_hash:
			result.append(0)
		else:
			result.append(1)

	return wires_to_int(result, sum(gc.circuit.output_counts))


def evaluate(circuit: Circuit, inputs: list[int]):
	if len(circuit.input_counts) != len(inputs):
		raise ValueError("Input count doesn't match circuit")

	labels = list()

	# first we convert the inputs into wire labels
	for i,c in zip(inputs, circuit.input_counts):
		input_wires = int_to_wires(i, c)
		#print("".join(map(str,input_wires)))
		labels += input_wires

	labels += [None] * circuit.gate_count

	for gate in circuit.gates:
		if gate.type == _GateType.XOR:
			labels[gate.id] = labels[gate.inputs[0]] ^ labels[gate.inputs[1]]

		elif gate.type == _GateType.AND:
			labels[gate.id] = labels[gate.inputs[0]] & labels[gate.inputs[1]]

		elif gate.type == _GateType.INV:
			labels[gate.id] = 1-labels[gate.inputs[0]]

		elif gate.type == _GateType.EQW:
			labels[gate.id] = labels[gate.inputs[0]]

		else:
			raise NotImplementedError(f"Unknown gate type: {gate.type}")

	#print("".join(map(str,labels[-sum(circuit.output_counts):])))

	result = wires_to_int(labels[-sum(circuit.output_counts):], sum(circuit.output_counts))

	#print(f"{inputs[0]} + {inputs[1]} = {inputs[0]+inputs[1]}, got {result}")
	#print(f"-({inputs[0]}) = {-inputs[0]}, got {result}")
	#print(f"{inputs[0]} / {inputs[1]} = {inputs[0]//inputs[1]}, got {result}")

	return result


def int_to_wires(num: int, bits: int):
	wires = [0] * bits
	for i in range(bits):
		wires[bits-i-1] = num & 1
		num >>= 1
	wires.reverse()
	return wires


def wires_to_int(wires: list[int], bits: int):
	wires.reverse()
	result = 0

	# negative
	if wires[0]:
		for wire in wires:
			result <<= 1
			result |= 1-wire
		result = -(result+1)

	else: # positive
		for wire in wires:
			result <<= 1
			result |= wire

	return result
