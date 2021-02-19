from collections import namedtuple

Circuit = namedtuple("Circuit", ["input_counts", "output_counts", "gate_count", "wire_count", "gates"])


GarbledCircuit = namedtuple("GarbledCircuit", ["input_labels", "ctxts", "output_map", "circuit"])

_Gate = namedtuple("Gate", ["type", "inputs", "id"])
	# if xor == False then it's an AND gate
	# id is a wire. start counting after inputs


def enum(**named_values):
	return type("Enum", (), named_values)


_GateType = enum(XOR=0, AND=1, INV=2, EQW=3)
