from .forward import tab as sub_table
def _sub_word(word):
	return (
		sub_table[word[0]],
		sub_table[word[1]],
		sub_table[word[2]],
		sub_table[word[3]],
	)

# Round constants
rc = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]
rc_words = [bytearray([r, 0, 0, 0]) for r in rc]

# Key is 128 bits, which is 4 words.
# Instances of 4 are references to this.

def _rot_word(word: list()):
	return word[-3:] + word[:1]
	#return word[-1:] + word[0:3]

def _xor3(a, b, c):
	f = lambda x: x[0]^x[1]^x[2]
	return map(f, zip(a,b,c))

def _xor2(a, b):
	f = lambda x: x[0]^x[1]
	return map(f, zip(a,b))

def get_keys(orig_key: bytearray):
	words = [0] * 44 # 4-byte key chunks
	keys  = [0] * 11 # full 32-byte keys

	for i in range(44):
		if i < 4:
			words[i] = orig_key[(i*4):(i*4+4)]
			continue

		if i % 4 == 0:
			tmp = _sub_word(_rot_word(words[i-1][:]))
			words[i] = list(_xor3(words[i-4][:], tmp, rc_words[i//4][:]))
			continue
		
		# else
		words[i] = list(_xor2(words[i-4][:], words[i-1]))
	
	# next combine chunks of 4 bytes into chunks of 16
	for i in range(11):
		keys[i] = tuple([tuple(w) for w in words[4*i:4*i+4]])

	return tuple(keys)

def add_round_key(key: tuple[tuple[int]], state: tuple[tuple[int]]):
	new_state = (
		tuple(_xor2(key[0], state[0])),
		tuple(_xor2(key[1], state[1])),
		tuple(_xor2(key[2], state[2])),
		tuple(_xor2(key[3], state[3]))
	)
	return new_state

# test vectors: https://samiam.org/key-schedule.html
