from . import key_schedule
from .state import State

def encrypt(key: bytearray, message: bytearray):
	# initialize
	keys  = key_schedule.get_keys(key)
	state = State(message)
	state.add_round_key(keys[0])

	# main rounds loop
	for i in range(9):
		state.sub_bytes()
		state.shift_rows()
		state.mix_columns()
		state.add_round_key(keys[i+1])
	
	# final round
	state.sub_bytes()
	state.shift_rows()
	state.add_round_key(keys[10])

	return state.to_bytes()


def decrypt(key: bytearray, ctext: bytearray):
	keys  = key_schedule.get_keys(key)
	state = State(ctext)
	
	# first round
	state.add_round_key(keys[10])
	state.inv_shift_rows()
	state.inv_sub_bytes()

	for i in range(9):
		state.add_round_key(keys[9-i])
		state.inv_mix_columns()
		state.inv_shift_rows()
		state.inv_sub_bytes()
	
	# finalize
	state.add_round_key(keys[0])

	return state.to_bytes()

