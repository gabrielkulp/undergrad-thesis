def carmichael(p, q):
	return lcm(p-1, q-1)

def lcm(a, b):
	return a * b // gcd(a, b)

def trailing_zeros(n):
	z = 0
	while n & 1 == 0:
		z += 1
		n >>= 1
	return z

# Euclidean algorithm
# https://en.wikipedia.org/wiki/Binary_GCD_algorithm
def gcd(u, v):
	if u == 0:
		return v
	if v == 0:
		return u
	
	i = trailing_zeros(u)
	j = trailing_zeros(v)
	k = min(i, j)
	# factor out every 2
	u >>= i
	v >>= j

	while True:
		# keep u <= v
		if u > v:
			u, v = v, u
		
		v -= u
		if v == 0:
			return u << k
		
		v >>= trailing_zeros(v)


# https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Modular_inverse
def mul_inv(e: int, l: int):
	"""modular multiplicative inverse: find d such that d*e=1 (mod l)"""
	
	# first find extended gcd of a, b such
	# that such that a*x + b*y = gcd(a, b)
	# except we only need x, so ignore y!
	a, b = e, l
	x0, x1 = 0, 1
	while a != 0:
		(q, a), b = divmod(b, a), a
		x0, x1 = x1, x0 - q * x1
	
	if b != 1: # if gcd(e, l) != 1, then e and l are not coprime
		return None
	
	return x0 % l
