import os
import aes
import random # for generating colors
from .types import Circuit, GarbledCircuit, _Gate, _GateType


aes_key = bytearray.fromhex("00000000000000000000000000000000")
hash = lambda x: aes.encrypt(aes_key, bytearray(x))


def _generate_colors():
	in_order = [[0,0],[0,1],[1,0],[1,1]]
	return random.sample(in_order, 4)


def _generate_wire_label():
	r = os.urandom(16)
	return int.from_bytes(r, "little")


def garble(circuit: Circuit):
	# Build and reference array of label<->wire mappings.
	# Index in the array is wire ID, value is False label.
	labels = list()

	# The secret difference between True and False labels
	delta = _generate_wire_label()

	# The garbled truth tables for all gates
	ctxts = list()

	for _ in range(sum(circuit.input_counts)):
		labels.append(_generate_wire_label())

	for gate in circuit.gates:
		# compute wire labels
		
		if gate.type == _GateType.AND:
			# compute next ctxts in the array
			in_1_false = labels[gate.input1]
			in_1_true  = in_1_false ^ delta
			in_2_false = labels[gate.input2]
			in_2_true  = in_2_false ^ delta
			out_false  = _generate_wire_label()
			out_true   = out_false ^ delta

			table = list()
			table.append(hash(in_1_false^in_2_false) ^ out_false)
			table.append(hash(in_1_false^in_2_true ) ^ out_false)
			table.append(hash(in_1_true ^in_2_false) ^ out_false)
			table.append(hash(in_1_true ^in_2_true ) ^ out_true)
			ctxts.append(table)

	output_map = list()
	first_output_wire = circuit.wire_count - sum(circuit.output_counts)
	
	for wire in range(first_output_wire, circuit.wire_count):
		label = ctxts[wire]
		# record mapping of output wire IDs to output labels
		output_map.append(hash(label))
	return ctxts, output_map


def gc_evaluate(gc: GarbledCircuit):
	pass # this function is barely pseudocode right now
	active_labels = gc.input_labels

	ctxt_counter = 0
	for gate in gc.circuit.gates:
		if gate.type == _GateType.XOR:
			active_labels.append(active_labels[gate.input1] ^ active_labels[gate.input2])

		if gate.type == _GateType.AND:
			table = gc.ctxts[ctxt_counter]
			ctxt_counter += 1
			key = hash(active_labels[gate.input1] ^ active_labels[gate.input2])
			active_labels.append(table[0] ^ key)

	result = list()
	first_output_wire = gc.circuit.wire_count - sum(gc.circuit.output_counts)
	output_wires = range(first_output_wire, gc.circuit.wire_count)
	
	for (label_hash, label) in zip(gc.output_map, output_wires):
		if hash(label) == label_hash:
			result.append(True)
		else:
			result.append(False)

	return result


def evaluate(circuit: Circuit, inputs: list[int]):
	if len(circuit.input_counts) != len(inputs):
		raise ValueError("Input count doesn't match circuit")

	labels = list()
	print("")

	# first we convert the inputs into wire labels
	for i,c in zip(inputs, circuit.input_counts):
		input_wires = int_to_wires(i, c)
		print("".join(map(str,input_wires)))
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

	print("".join(map(str,labels[-sum(circuit.output_counts):])))

	result = wires_to_int(labels[-sum(circuit.output_counts):], sum(circuit.output_counts))
	
	print(f"{inputs[0]} + {inputs[1]} = {inputs[0]+inputs[1]}, got {result}")
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
