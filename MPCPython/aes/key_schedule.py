from . import sub_bytes

# Round constants
rc = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
rc_words = [bytearray([r, 0, 0, 0]) for r in rc]

# Key is 128 bits, which is 4 words.
# Instances of 4 are references to this.

def _rot_word(word):
	return word[-3:] + word[:1]
	#return word[-1:] + word[0:3]

def _xor3(a, b, c):
	for i in range(4):
		a[i] ^= b[i] ^ c[i]
	return a

def xor2(a, b):
	for i in range(4):
		a[i] ^= b[i]
	return a

def get_keys(orig_key):
	words = [0] * 44 # 4-byte key chunks
	keys  = [0] * 11 # full 32-byte keys

	for i in range(44):
		if i < 4:
			words[i] = orig_key[(i*4):(i*4+4)]
			continue

		if i % 4 == 0:
			tmp = sub_bytes.sub_word(_rot_word(words[i-1][:]))
			words[i] = _xor3(words[i-4][:], tmp, rc_words[i//4][:])
			continue
		
		# else
		words[i] = xor2(words[i-4][:], words[i-1])
	
	# next combine chunks of 4 bytes into chunks of 16
	for i in range(11):
		keys[i] = words[4*i:4*i+4]# + words[4*i+1] + words[4*i+2] + words[4*i+3]

	return keys

def add_round_key(key: bytearray, state):
	for i in range(4):
		state[i] = xor2(key[i], state[i])
	return state

# test vectors: https://samiam.org/key-schedule.html
