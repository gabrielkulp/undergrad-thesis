import aes
from collections import namedtuple

# Types
Circuit = namedtuple("Circuit", ["input_sizes", "output_size", "gate_count", "wire_count", "first_output", "gates"])

GarbledCircuit = namedtuple("GarbledCircuit", ["input_labels", "circuit", "ctxts"])

Gate = namedtuple("Gate", ["type", "inputs", "id"])

def enum(**named_values):
	return type("Enum", (), named_values)

GateType = enum(XOR=0, AND=1, INV=2, EQW=3)

# Utilities
_aes_keys  = aes.get_key_schedule(bytearray.fromhex("000102030405060708090a0b0c0d0e0f"))
_to_bytes = lambda x: bytearray(x.to_bytes(16, "little"))
hash_pair = lambda x, y: int.from_bytes(aes.encrypt(_aes_keys, _to_bytes((x*2)^(y*2))), "little")

c_idx     = lambda w1,w2: ((w1 & 1) << 1) | (w2 & 1)


# non-cryptographic for testing
def plain_evaluate(circuit: Circuit, inputs: list[int]):
	# convert the inputs into wire labels
	labels = list()
	for i,c in zip(inputs, circuit.input_sizes):
		input_wires = int_to_wires(i, c)
		labels += input_wires
	labels += [None] * circuit.gate_count

	# gate-wise evaluation
	for gate in circuit.gates():
		if gate.type == GateType.XOR:
			labels[gate.id] = labels[gate.inputs[0]] ^ labels[gate.inputs[1]]

		elif gate.type == GateType.AND:
			labels[gate.id] = labels[gate.inputs[0]] & labels[gate.inputs[1]]

		elif gate.type == GateType.INV:
			labels[gate.id] = 1-labels[gate.inputs[0]]

		elif gate.type == GateType.EQW:
			labels[gate.id] = labels[gate.inputs[0]]

		else:
			raise NotImplementedError(f"Unknown gate type: {gate.type}")

	# interpret result
	result = wires_to_int(labels[-circuit.output_size:], circuit.output_size)
	return result


def int_to_wires(num: int, bits: int):
	wires = [0] * bits
	for i in range(bits):
		wires[bits-i-1] = num & 1
		num >>= 1
	wires.reverse()
	#print("".join(map(str,wires)))
	return wires


def wires_to_int(wires: list[int], bits: int):
	#print("".join(map(str,wires)))

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
