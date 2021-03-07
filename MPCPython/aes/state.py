# bytearray -> tuple[tuple[int]]
def from_bytes(data: bytearray):
	return (
		tuple(data[0:4]),
		tuple(data[4:8]),
		tuple(data[8:12]),
		tuple(data[12:16]),
	)

# tuple[tuple[int]] -> bytearray
def to_bytes(state: tuple[tuple[int]]):
	return b"".join((bytearray(c) for c in state))
