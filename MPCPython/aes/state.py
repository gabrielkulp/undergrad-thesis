from . import sub_bytes
from . import shift_rows
from . import mix_columns
from . import key_schedule

class State:
	def __init__(self, data: bytearray): # from_bytes
		self.state = [ [0]*4 for _ in range(4) ]
		for i in range(4):
			for j in range(4):
				idx = (4*i)+j
				if idx < len(data):
					self.state[i][j] = data[idx]

	def to_bytes(self):
		rows = list()
		for r in self.state:
			rows.append(bytearray(r))
		return b"".join(rows)
	
	def sub_bytes(self):
		self.state = sub_bytes.forward(self.state)
	
	def inv_sub_bytes(self):
		self.state = sub_bytes.inverse(self.state)
	
	def shift_rows(self):
		self.state = shift_rows.shift(self.state)

	def inv_shift_rows(self):
		self.state = shift_rows.unshift(self.state)
	
	def mix_columns(self):
		self.state = mix_columns.mix(self.state)

	def inv_mix_columns(self):
		self.state = mix_columns.unmix(self.state)
	
	def add_round_key(self, key: bytearray):
		self.state = key_schedule.add_round_key(key, self.state)
		#for i in range(4):
		#	self.state[i] = xor2(key[i], self.state[i])
