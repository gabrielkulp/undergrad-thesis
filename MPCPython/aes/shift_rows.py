# Shift rows to mix the columns so they aren't encrypted independently

# Note that AES stores its data in column-major form, so
# shifting rows means moving bytes between sub-lists.

def shift(state):
	# don't shift first row

	# shift second row left by one
	temp = state[0][1]
	state[0][1] = state[1][1]
	state[1][1] = state[2][1]
	state[2][1] = state[3][1]
	state[3][1] = temp

	# shift third row left by two
	temp = state[0][2]
	state[0][2] = state[2][2]
	state[2][2] = temp

	temp = state[1][2]
	state[1][2] = state[3][2]
	state[3][2] = temp

	# shift fourth row left by 3 (right by 1)
	temp = state[0][3]
	state[0][3] = state[3][3]
	state[3][3] = state[2][3]
	state[2][3] = state[1][3]
	state[1][3] = temp

	return state


def unshift(state):
	# don't shift first row

	# shift second row right by one
	temp = state[0][1]
	state[0][1] = state[3][1]
	state[3][1] = state[2][1]
	state[2][1] = state[1][1]
	state[1][1] = temp

	# shift third row right by two
	temp = state[0][2]
	state[0][2] = state[2][2]
	state[2][2] = temp

	temp = state[1][2]
	state[1][2] = state[3][2]
	state[3][2] = temp

	# shift fourth row right by 3 (left by 1)
	temp = state[0][3]
	state[0][3] = state[1][3]
	state[1][3] = state[2][3]
	state[2][3] = state[3][3]
	state[3][3] = temp

	return state
