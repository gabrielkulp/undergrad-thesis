from .key_schedule import get_keys
from .state import State

def get_key_schedule(key: bytearray):
	return get_keys(key)

def encrypt(key_schedule: tuple[tuple[bytes]], message: bytearray):
	# initialize
	state = State(message)
	state.add_round_key(key_schedule[0])

	# main rounds loop
	for i in range(9):
		state.sub_bytes()
		state.shift_rows()
		state.mix_columns()
		state.add_round_key(key_schedule[i+1])
	
	# final round
	state.sub_bytes()
	state.shift_rows()
	state.add_round_key(key_schedule[10])

	return state.to_bytes()


def decrypt(key_schedule: tuple[tuple[bytes]], ctxt: bytearray):
	# initialize
	state = State(ctxt)
	
	# first round
	state.add_round_key(key_schedule[10])
	state.inv_shift_rows()
	state.inv_sub_bytes()

	for i in range(9):
		state.add_round_key(key_schedule[9-i])
		state.inv_mix_columns()
		state.inv_shift_rows()
		state.inv_sub_bytes()
	
	# finalize
	state.add_round_key(key_schedule[0])

	return state.to_bytes()

