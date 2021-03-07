from . import key_schedule
from . import state
from . import forward
from . import inverse

def get_key_schedule(key: bytearray):
	return key_schedule.get_keys(key)

def encrypt(keys: tuple[tuple[int]], message: bytearray):
	# initialize
	mat = state.from_bytes(message)
	mat = key_schedule.add_round_key(keys[0], mat)

	# main rounds loop
	for i in range(1,10):
		mat = forward.sub_shift_mix(mat)
		mat = key_schedule.add_round_key(keys[i], mat)
	
	# final round
	mat = forward.sub_shift(mat)
	mat = key_schedule.add_round_key(keys[10], mat)

	return state.to_bytes(mat)


def decrypt(keys: tuple[tuple[int]], ctxt: bytearray):
	# initialize
	mat = state.from_bytes(ctxt)
	
	# first round
	mat = key_schedule.add_round_key(keys[10], mat)
	mat = inverse.shift_sub(mat)

	for i in range(9,0,-1):
		mat = key_schedule.add_round_key(keys[i], mat)
		mat = inverse.mix_shift_sub(mat)
	
	# finalize
	mat = key_schedule.add_round_key(keys[0], mat)

	return state.to_bytes(mat)
