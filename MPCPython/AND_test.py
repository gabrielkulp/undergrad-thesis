#!/usr/bin/env python3
# generate test vectors for debugging AND gates

import aes

pretty = lambda l: " ".join(["{:02x}".format(x) for x in l])
aes_keys = aes.get_key_schedule(bytearray.fromhex("000102030405060708090a0b0c0d0e0f"))

#label_1_arr = bytearray([(8+x**2)%255 for x in range(16)])
label_1_arr = bytearray([1]+([5]*15))
#label_2_arr = bytearray([((x+9)*(8*x-4))%255 for x in range(16)])
label_2_arr = bytearray([1]+([3]*15))
label_1_int = int.from_bytes(label_1_arr, "little")
label_2_int = int.from_bytes(label_2_arr, "little")

print("Label 1:   ", pretty(label_1_arr))
print("Label 2:   ", pretty(label_2_arr))

# the *2 makes the final number too big, so we cut off the top byte
combined   = ((label_1_int*2) ^ (label_2_int*2)).to_bytes(17, "little")[:-1]
aes_input  = bytearray(combined)
aes_output = aes.encrypt(aes_keys, aes_input)
print("\nAES input: ", pretty(aes_input))
print("AES output:", pretty(aes_output))

# generate ciphertext array
ctxt  = bytearray.fromhex("66217c17175db79ea159514bbeef6072")
ctxts = [[0]*16, ctxt, bytearray([x//2 for x in ctxt]), bytearray([(x*2)%256 for x in ctxt])]
ctxt_n = ((label_1_arr[0] & 1) << 1) | (label_2_arr[0] & 1)

print("\nCTXTs:")
for n in range(4):
	print(f"         {n}:", pretty(ctxts[n]), "<<<" if ctxt_n==n else "")

print("\nNew label choices:")
for n in range(4):
	new_label = [a^b for (a,b) in zip(aes_output, ctxts[n])]
	print(f"         {n}:", pretty(new_label), "<<<" if ctxt_n==n else "")
