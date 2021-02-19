#!/usr/bin/env python3
from collections import namedtuple

import aes
def test_aes(verbose):
	TestVector = namedtuple("TestVector", ["key", "plaintext", "ciphertext"])

	tests = [
		TestVector(
			key        = bytearray.fromhex("00000000000000000000000000000000"),
			plaintext  = bytearray.fromhex("f34481ec3cc627bacd5dc3fb08f273e6"),
			ciphertext = bytearray.fromhex("0336763e966d92595a567cc9ce537f5e")
		),
		TestVector(
			key        = bytearray.fromhex("00000000000000000000000000000000"),
			plaintext  = bytearray.fromhex("9798c4640bad75c7c3227db910174e72"),
			ciphertext = bytearray.fromhex("a9a1631bf4996954ebc093957b234589")
		),
		TestVector(
			key        = bytearray.fromhex("00000000000000000000000000000000"),
			plaintext  = bytearray.fromhex("96ab5c2ff612d9dfaae8c31f30c42168"),
			ciphertext = bytearray.fromhex("ff4f8391a6a40ca5b25d23bedd44a597")
		),
		TestVector(
			key        = bytearray.fromhex("00000000000000000000000000000000"),
			plaintext  = bytearray.fromhex("6a118a874519e64e9963798a503f1d35"),
			ciphertext = bytearray.fromhex("dc43be40be0e53712f7e2bf5ca707209")
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
		enc = aes.encrypt(test.key, test.plaintext)
		dec = aes.decrypt(test.key, test.ciphertext)
		round_trip = aes.decrypt(test.key, aes.encrypt(test.key, test.plaintext))
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
	c = circuit.read_from_file("circuit.txt")
	circuit.evaluate(c, [256,2])
	circuit.evaluate(c, [928374,4345])
	circuit.evaluate(c, [-234,43])
	circuit.evaluate(c, [-987243,-345])
	circuit.evaluate(c, [-9872,-333345])




def test_all(verbose):
	print("AES:", test_aes(verbose))
	print("RSA:", test_rsa(verbose))

#test_all(False)
test_circuit()
