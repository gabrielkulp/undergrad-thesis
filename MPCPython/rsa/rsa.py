import os
from . import primes
from . import modular
from collections import namedtuple

PubKey = namedtuple("PubKey", ["exponent", "modulo"])
PrivKey = namedtuple("PrivKey", ["dp", "dq", "qinv", "p", "q"])

# https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
def generate_keys(key_size: int):
	d = None
	while not d:
		p = primes.next_prime(int.from_bytes(os.urandom(key_size//2), "big"))
		#5428904424695386810646763212901356596007820907006144194078433708892066269711969248166042693451555762318506190315543517163894749075515062478121335278652111
		q = primes.next_prime(int.from_bytes(os.urandom(key_size//2), "big"))
		#4801699083232579906531962705933852009977755777438618497007326525577727931162691741395369739164309124595010358443749152079387986785672311673279065866363027

		n = p * q
		l = modular.carmichael(p, q)
		e = 65537

		# We need to pick e such that gcd(e, l) = 1. We'll see if
		# that's the case during this step. If it doesn't work,
		# loop back and pick a new p and q.
		d = modular.mul_inv(e, l)

	pub_key = PubKey(exponent=e, modulo=n)
	# priv_key = Key(exponent=d, modulo=n)

	# next record extra data for Chinese Remainder Theorem decryption
	dp = d % (p-1)
	dq = d % (q-1)
	qinv = modular.mul_inv(q, p)
	priv_key = PrivKey(dp, dq, qinv, p, q)
	
	return pub_key, priv_key


# Normal modular exponentiation
def encrypt(m:int, k: PubKey):
	return pow(m, k.exponent, k.modulo)


# Chinese Remainder Theorem
def decrypt(c:int, k: PrivKey):
	m1 = pow(c, k.dp, k.p)
	m2 = pow(c, k.dq, k.q)
	h = (k.qinv * (m1-m2)) % k.p
	return m2 + h * k.q


