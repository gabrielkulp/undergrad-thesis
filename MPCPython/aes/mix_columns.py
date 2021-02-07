
# https://en.wikipedia.org/wiki/Rijndael_MixColumns

def _mul(a: int, b: int): # Galois Field (256) Multiplication of two Bytes
	p = 0

	for _ in range(8):
		if ((b & 1) != 0):
			p ^= a

		hi_bit_set = ((a & 0x80) != 0)
		a <<= 1
		a &= 0xFF
		if hi_bit_set:
			a ^= 0x1B # x^8 + x^4 + x^3 + x + 1

		b >>= 1
	return p


def _mix_single(a):
	# 'a' is the main State matrix column, 'b' is the result column.
	# entries without the _mul call are multiplied by 1.
	b = [0] * 4

	b[0] = _mul(2, a[0]) ^ _mul(3, a[1]) ^         a[2]  ^         a[3]
	b[1] =         a[0]  ^ _mul(2, a[1]) ^ _mul(3, a[2]) ^         a[3]
	b[2] =         a[0]  ^         a[1]  ^ _mul(2, a[2]) ^ _mul(3, a[3])
	b[3] = _mul(3, a[0]) ^         a[1]  ^         a[2]  ^ _mul(2, a[3])

	return b


def _unmix_single(a):
	# 'a' is the main State matrix column, 'b' is the result column.
	b = [0] * 4

	b[0] = _mul(14, a[0]) ^ _mul(11, a[1]) ^ _mul(13, a[2]) ^ _mul(9,  a[3])
	b[1] = _mul(9,  a[0]) ^ _mul(14, a[1]) ^ _mul(11, a[2]) ^ _mul(13, a[3])
	b[2] = _mul(13, a[0]) ^ _mul(9,  a[1]) ^ _mul(14, a[2]) ^ _mul(11, a[3])
	b[3] = _mul(11, a[0]) ^ _mul(13, a[1]) ^ _mul(9,  a[2]) ^ _mul(14, a[3])

	return b


def mix(state):
	return [_mix_single(col) for col in state]

def unmix(state):
	return [_unmix_single(col) for col in state]
