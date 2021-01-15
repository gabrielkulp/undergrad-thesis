import random

def next_prime(n):
	# only check odd numbers
	if n % 2 == 0:
		n += 1
	else:
		n += 2 # get next prime, not this one

	while True:
		if is_prime(n):
			return n
		else:
			n = n + 2 # next odd


# Miller-Rabin Test
# Adapted from:
# https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
# https://gist.github.com/Ayrx/5884790
def is_prime(n):

	# simple tests first
	if n == 2 or n == 3:
		return True
	if n == 1 or n % 2 == 0:
		return False

	d = n - 1
	r = 0

	# pick d, r such that n = 2**r * d + 1
	while d % 2 == 0:
		r += 1
		d >>= 1

	for _ in range(40): # apparently 40 is a good choice?
		a = random.randint(2, n-2)
		x = pow(a, d, n)
		
		if x == 1 or x == n - 1:
			continue
		
		for _ in range(r-1):
			x = pow(x, 2, n)
			if x == n - 1:
				break
		else:
			return False

	return True
