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

def mix_single(a):
	# entries without the _mul call are multiplied by 1.
	return (
		_mul(2, a[0]) ^ _mul(3, a[1]) ^         a[2]  ^         a[3],
		        a[0]  ^ _mul(2, a[1]) ^ _mul(3, a[2]) ^         a[3],
		        a[0]  ^         a[1]  ^ _mul(2, a[2]) ^ _mul(3, a[3]),
		_mul(3, a[0]) ^         a[1]  ^         a[2]  ^ _mul(2, a[3]),
	)

def unmix_single(a):
	return (
		_mul(14, a[0]) ^ _mul(11, a[1]) ^ _mul(13, a[2]) ^ _mul(9,  a[3]),
		_mul(9,  a[0]) ^ _mul(14, a[1]) ^ _mul(11, a[2]) ^ _mul(13, a[3]),
		_mul(13, a[0]) ^ _mul(9,  a[1]) ^ _mul(14, a[2]) ^ _mul(11, a[3]),
		_mul(11, a[0]) ^ _mul(13, a[1]) ^ _mul(9,  a[2]) ^ _mul(14, a[3])
	)
