import socket
import rsa
import os

exponent_size = 3 # exponent is hard-coded to 65537 in rsa.py
pubkey_size = 16 # bytes

# As per the typical convention:
# use little-endian for on-device encoding, and
# use big-endian for anything sent through the socket

def send(sock: socket.socket, message0, message1): # Alice
	pubkey, privkey = rsa.generate_keys(pubkey_size)

	print("N  ", pubkey.modulo)

	# send public key
	sock.sendall(pubkey.exponent.to_bytes(exponent_size, "big"))
	sock.sendall(pubkey.modulo.to_bytes(pubkey_size, "big"))

	# generate and send 2 random messages
	x0 = os.urandom(pubkey_size)
	x1 = os.urandom(pubkey_size)
	sock.sendall(x0)
	sock.sendall(x1)
	print("x0 ", int.from_bytes(x0, "big"))
	print("x1 ", int.from_bytes(x1, "big"))

	# receive encrypted choice
	v = int.from_bytes(sock.recv(pubkey_size), "big")
	print("v  ", v)

	# decrypt choice with the messages
	k0 = rsa.decrypt((v - int.from_bytes(x0, "big")), privkey) % pubkey.modulo
	k1 = rsa.decrypt((v - int.from_bytes(x1, "big")), privkey) % pubkey.modulo
	print("k0 ", k0)
	print("k1 ", k1)

	# send both messages
	m0 = int.from_bytes(message0, "little")
	m1 = int.from_bytes(message1, "little")
	sock.sendall((m0+k0).to_bytes(pubkey_size, "big"))
	sock.sendall((m1+k1).to_bytes(pubkey_size, "big"))



def receive(sock: socket.socket, choice): # Bob
	# get public key
	exponent = int.from_bytes(sock.recv(exponent_size), "big")
	modulo   = int.from_bytes(sock.recv(pubkey_size), "big")
	pubkey = rsa.PubKey(exponent, modulo)

	# get 2 random messages
	x0 = sock.recv(pubkey_size)
	x1 = sock.recv(pubkey_size)

	# choose
	xb = int.from_bytes(x1 if choice else x0, "big")
	print("xb ", xb)

	# encrypt choice with random
	k = int.from_bytes(os.urandom(pubkey_size), "little")
	v = (xb + rsa.encrypt(k, pubkey)) % pubkey.modulo
	sock.sendall(v.to_bytes(pubkey_size, "big"))
	print("v  ", v)
	print("k  ", k)

	# receive both messages
	m0 = int.from_bytes(sock.recv(pubkey_size), "big")
	m1 = int.from_bytes(sock.recv(pubkey_size), "big")

	print("m0\'", m0)
	print("m1\'", m1)

	# decrypt the chosen value
	mb = (m1 if choice else m0) - k
	print("m  ", mb)

	# detect when there's a problem
	if mb < 0:
		print("ERROR!")
		return False

	# it's an int, so turn it back into bytes
	return mb.to_bytes((mb.bit_length()+7)//8, "little")
