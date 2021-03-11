import aes
from .types import Circuit, GateType

_aes_keys  = aes.get_key_schedule(bytearray.fromhex("00000000000000000000000000000000"))
_to_bytes = lambda x: bytearray(x.to_bytes(16, "little"))
hash_pair = lambda x, y: int.from_bytes(aes.encrypt(_aes_keys, _to_bytes(x^y)), "little")

c_idx     = lambda w1,w2: ((w1 & 1) << 1) | (w2 & 1)


# non-cryptographic for testing
def plain_evaluate(circuit: Circuit, inputs: list[int]):
	if len(circuit.input_counts) != len(inputs):
		raise ValueError("Input count doesn't match circuit")

	labels = list()

	# first we convert the inputs into wire labels
	for i,c in zip(inputs, circuit.input_counts):
		input_wires = int_to_wires(i, c)
		labels += input_wires

	labels += [None] * circuit.gate_count

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


	result = wires_to_int(labels[-sum(circuit.output_counts):], sum(circuit.output_counts))

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
