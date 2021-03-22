from socket import socket
import rsa
import os

exponent_size = 3 # exponent is hard-coded to 65537 in rsa.py
pubkey_size = 16 # bytes

# As per the typical convention:
# use little-endian for on-device encoding, and
# use big-endian for anything sent through the socket

def send(sock: socket, message0, message1): # Alice
	pubkey, privkey = rsa.generate_keys(pubkey_size)

	# send public key
	sock.sendall(pubkey.exponent.to_bytes(exponent_size, "big"))
	sock.sendall(pubkey.modulo.to_bytes(pubkey_size, "big"))

	# generate and send 2 random messages
	x0 = int.from_bytes(os.urandom(pubkey_size), "little") % pubkey.modulo
	x1 = int.from_bytes(os.urandom(pubkey_size), "little") % pubkey.modulo
	sock.sendall(x0.to_bytes(pubkey_size, "big"))
	sock.sendall(x1.to_bytes(pubkey_size, "big"))

	# receive encrypted choice
	v = int.from_bytes(sock.recv(pubkey_size), "big")

	# decrypt choice with the messages
	k0 = rsa.decrypt((v - x0), privkey) % pubkey.modulo
	k1 = rsa.decrypt((v - x1), privkey) % pubkey.modulo

	# send both messages
	m0 = (message0^k0)# % pubkey.modulo
	m1 = (message1^k1)# % pubkey.modulo
	sock.sendall((m0).to_bytes(pubkey_size, "big"))
	sock.sendall((m1).to_bytes(pubkey_size, "big"))



def receive(sock: socket, choice): # Bob
	# get public key
	exponent = int.from_bytes(sock.recv(exponent_size), "big")
	modulo   = int.from_bytes(sock.recv(pubkey_size), "big")
	pubkey = rsa.PubKey(exponent, modulo)

	# get 2 random messages
	x0 = sock.recv(pubkey_size)
	x1 = sock.recv(pubkey_size)

	# choose
	xb = int.from_bytes(x1 if choice else x0, "big")

	# encrypt choice with random
	k = int.from_bytes(os.urandom(pubkey_size), "little") % pubkey.modulo
	v = (xb + rsa.encrypt(k, pubkey)) % pubkey.modulo
	sock.sendall(v.to_bytes(pubkey_size, "big"))

	# receive both messages
	m0 = int.from_bytes(sock.recv(pubkey_size), "big")
	m1 = int.from_bytes(sock.recv(pubkey_size), "big")

	# decrypt the chosen value
	mb = (m1 if choice else m0) ^ k

	# detect when there's a problem
	if mb < 0:
		return False

	# return result as int
	return mb
