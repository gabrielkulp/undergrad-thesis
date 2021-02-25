import os # for generating wire labels with urandom
import aes
import random # for generating colors
from .types import Circuit, GarbledCircuit, _Gate, _GateType


#aes_key = bytearray.fromhex("00000000000000000000000000000000")
# Placeholder hash. Replace with aes.encrypt(aes_key, bytearray(x))
hash = lambda x: ~x[0]
hash_pair = lambda x, y: (hash(x)) ^ (hash(y))
encrypt = lambda l1, l2, out:  (hash_pair(l1,l2)^out[0],  l1[1]^l2[1]^out[1])
decrypt = lambda l1, l2, ctxt: (hash_pair(l1,l2)^ctxt[0], l1[1]^l2[1]^ctxt[1])

def _generate_wire_label():
	r = os.urandom(16)
	label = int.from_bytes(r, "little")
	color = random.getrandbits(1)
	return (label, color)


def garble(circuit: Circuit):
	# Build and reference array of label<->wire mappings.
	# Index in the array is wire ID, value is False label.
	labels = [None] * circuit.wire_count

	# The secret difference between True and False labels
	delta = _generate_wire_label()[0]

	# utility functions for working with wire labels
	inv_wire = lambda w: (w[0]^delta, 1-w[1])
	c_idx = lambda w1,w2: 2*w1[1] + w2[1]

	# The garbled truth tables for all gates
	ctxts = list()

	# generate input wire labels
	input_labels = list()
	for i in range(sum(circuit.input_counts)):
		f_label = _generate_wire_label()
		t_label = inv_wire(f_label)
		labels[i] = f_label
		input_labels.append((f_label,t_label))

	for gate in circuit.gates:
		# compute wire labels
		if gate.type == _GateType.XOR:
			# free XOR means no hash/AES needed here!
			in_1_f = labels[gate.inputs[0]]
			in_2_f = labels[gate.inputs[1]]
			out_f  = (in_1_f[0] ^ in_2_f[0], in_1_f[1] ^ in_2_f[1])
			labels[gate.id] = out_f
			# no ctxt table to append
		
		elif gate.type == _GateType.AND:
			# compute next ctxts in the array
			in_1_f = labels[gate.inputs[0]]
			in_2_f = labels[gate.inputs[1]]
			out_f  = _generate_wire_label()
			labels[gate.id] = out_f

			in_1_t  = inv_wire(in_1_f)
			in_2_t  = inv_wire(in_2_f)
			out_t   = inv_wire(out_f)

			table = (
				( encrypt(in_1_f, in_2_f, out_f), c_idx(in_1_f, in_2_f) ),
				( encrypt(in_1_f, in_2_t, out_f), c_idx(in_1_f, in_2_t) ),
				( encrypt(in_1_t, in_2_f, out_f), c_idx(in_1_t, in_2_f) ),
				( encrypt(in_1_t, in_2_t, out_t), c_idx(in_1_t, in_2_t) )
			)
			sorted_table = sorted(table, key=lambda x: x[1])
			ctxts.append([x[0] for x in sorted_table]) # don't append sorted colors
		
		elif gate.type == _GateType.INV:
			in_f = labels[gate.inputs[0]]
			out_f = _generate_wire_label()
			labels[gate.id] = out_f

			in_t  = inv_wire(in_f)
			out_t = inv_wire(out_f)

			table = (
				(hash(in_f) ^ out_t[0], in_f[1]^out_t[1]),
				(hash(in_t) ^ out_f[0], in_t[1]^out_f[1])
			)
			sorted_table = sorted(table, key=lambda x: x[1])
			ctxts.append(sorted_table)


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
			in_1_f = active_labels[gate.inputs[0]]
			in_2_f = active_labels[gate.inputs[1]]
			out_f  = (in_1_f[0] ^ in_2_f[0], in_1_f[1] ^ in_2_f[1])
			active_labels[gate.id] = out_f


		elif gate.type == _GateType.AND:
			table = gc.ctxts[ctxt_counter]
			ctxt_counter += 1
			wire1 = active_labels[gate.inputs[0]]
			wire2 = active_labels[gate.inputs[1]]
			color_idx = 2*wire1[1] + wire2[1]
			active_labels[gate.id] = decrypt(wire1, wire2, table[color_idx])
		
		elif gate.type == _GateType.INV:
			table = gc.ctxts[ctxt_counter]
			ctxt_counter += 1
			wire = active_labels[gate.inputs[0]]
			active_labels[gate.id] = hash(wire) ^ table[wire[1]][0], wire[1]^table[wire[1]][1]
		
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
