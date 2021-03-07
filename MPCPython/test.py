#!/usr/bin/env python3
from collections import namedtuple

import aes
def test_aes(verbose):
	TestVector = namedtuple("TestVector", ["key", "plaintext", "ciphertext"])

	tests = [
		TestVector(
			key        = bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"),
			plaintext  = bytearray.fromhex("6bc1bee22e409f96e93d7e117393172a"),
			ciphertext = bytearray.fromhex("3ad77bb40d7a3660a89ecaf32466ef97")
		),
		TestVector(
			key        = bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"),
			plaintext  = bytearray.fromhex("ae2d8a571e03ac9c9eb76fac45af8e51"),
			ciphertext = bytearray.fromhex("f5d3d58503b9699de785895a96fdbaaf")
		),
		TestVector(
			key        = bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"),
			plaintext  = bytearray.fromhex("30c81c46a35ce411e5fbc1191a0a52ef"),
			ciphertext = bytearray.fromhex("43b1cd7f598ece23881b00e3ed030688")
		),
		TestVector(
			key        = bytearray.fromhex("2b7e151628aed2a6abf7158809cf4f3c"),
			plaintext  = bytearray.fromhex("f69f2445df4f9b17ad2b417be66c3710"),
			ciphertext = bytearray.fromhex("7b0c785e27e8ad3f8223207104725dd4")
		),
		TestVector(
			key        = bytearray.fromhex("00000000000000000000000000000000"),
			plaintext  = bytearray.fromhex("cb9fceec81286ca3e989bd979b0cb284"),
			ciphertext = bytearray.fromhex("92beedab1895a94faa69b632e5cc47ce")
		),
		TestVector(
			key        = bytearray.fromhex("10a58869d74be5a374cf867cfb473859"),
			plaintext  = bytearray.fromhex("00000000000000000000000000000000"),
			ciphertext = bytearray.fromhex("6d251e6944b051e04eaa6fb4dbf78465")
		),
		TestVector(
			key        = bytearray.fromhex("caea65cdbb75e9169ecd22ebe6e54675"),
			plaintext  = bytearray.fromhex("00000000000000000000000000000000"),
			ciphertext = bytearray.fromhex("6e29201190152df4ee058139def610bb")
		),
		TestVector(
			key        = bytearray.fromhex("a2e2fa9baf7d20822ca9f0542f764a41"),
			plaintext  = bytearray.fromhex("00000000000000000000000000000000"),
			ciphertext = bytearray.fromhex("c3b44b95d9d2f25670eee9a0de099fa3")
		),
		TestVector(
			key        = bytearray.fromhex("b6364ac4e1de1e285eaf144a2415f7a0"),
			plaintext  = bytearray.fromhex("00000000000000000000000000000000"),
			ciphertext = bytearray.fromhex("5d9b05578fc944b3cf1ccf0e746cd581")
		),
		TestVector(
			key        = bytearray.fromhex("64cf9c7abc50b888af65f49d521944b2"),
			plaintext  = bytearray.fromhex("00000000000000000000000000000000"),
			ciphertext = bytearray.fromhex("f7efc89d5dba578104016ce5ad659c05")
		)
	]

	for test in tests:
		if verbose:
			print("key:    ", test.key.hex())
			print("inputs: ", test.plaintext.hex(), "-e->", test.ciphertext.hex())
		keys = aes.get_key_schedule(test.key)
		enc = aes.encrypt(keys, test.plaintext)
		dec = aes.decrypt(keys, test.ciphertext)
		round_trip = aes.decrypt(keys, aes.encrypt(keys, test.plaintext))
		if verbose:
			print("outputs:", dec.hex(), "-e->", enc.hex())
			print("round-trip?", (test.plaintext == round_trip))
			print("")
		if enc != test.ciphertext:
			return False
		if dec != test.plaintext:
			return False
		if test.plaintext != round_trip:
			return False
	return True


import rsa
from rsa import primes
def test_rsa(verbose):
	pub, priv = rsa.generate_keys(128)
	m = b"hello world"
	c = rsa.encrypt(int.from_bytes(m, "big"), pub)
	m2 = rsa.decrypt(c, priv)
	return (m2.to_bytes(len(m), "big") == m)


import circuit
def test_circuit():
	inputs = [(256,2), (928374,4345), (-234,43), (-987243,-345), (-9872,-333345)]
	
	c = circuit.read_from_file("udivide64.txt")
	print("read")
	gc = circuit.garble(c)
	print("garbled")
	for i in inputs:
		clear = circuit.evaluate(c,i)
		garbled = circuit.gc_evaluate(gc,i)
		print("clear:  ", clear)
		print("garbled:", garbled)
		print("")
		if clear != garbled:
			return False
	return True


def test_all(verbose):
	print("AES:", test_aes(verbose))
	print("RSA:", test_rsa(verbose))

test_all(False)
test_circuit()
