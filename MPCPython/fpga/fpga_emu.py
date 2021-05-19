from circuit import GateType
import aes
from .fpga import Cmd

_aes_keys  = aes.get_key_schedule(bytearray.fromhex("000102030405060708090a0b0c0d0e0f"))
_to_bytes = lambda x: bytearray(x.to_bytes(17, "little")[:-1])
hash_pair = lambda x, y: aes.encrypt(_aes_keys, _to_bytes((x^y)*2))
c_idx     = lambda w1,w2: ((w1 & 1) << 1) | (w2 & 1)

class FPGA():
	def __init__(self):
		self.emu = True
		self.addr = 0
		self.array = [None] * 504

	def _run_cmd(self, cmd: int, data: list) -> list:
		if cmd == Cmd.addr:
			self.addr = int.from_bytes(data, "little")
		elif cmd == Cmd.write:
			self.array[self.addr] = data
		elif cmd == Cmd.read:
			return self.array[self.addr]

		elif cmd == Cmd.gates:
			gate = data[0]
			if gate == GateType.AND:
				if len(data) != 55:
					print("length mismatch")
					return None
				input_1  = int.from_bytes(data[ 1: 3],         "little")
				input_2  = int.from_bytes(data[ 3: 5],         "little")
				out_addr = int.from_bytes(data[53:55],         "little")
				label_1  = int.from_bytes(self.array[input_1], "little")
				label_2  = int.from_bytes(self.array[input_2], "little")
				idx      = c_idx(label_1, label_2)

				table    = [None]*4
				table[0] = bytes(16)
				table[1] = data[ 5:21]
				table[2] = data[21:37]
				table[3] = data[37:53]

				hashed    = hash_pair(label_1, label_2)
				if len(hashed) != len(table[idx]):
					print("AND length mismatch")
					return None
				out_label = [a^b for (a,b) in zip(hashed, table[idx])]
				self.array[out_addr] = bytes(out_label)

			elif gate == GateType.XOR:
				if len(data) != 7:
					print("length mismatch")
					return None
				input_1   = int.from_bytes(data[1:3], "little")
				input_2   = int.from_bytes(data[3:5], "little")
				out_addr  = int.from_bytes(data[5:7], "little")
				if len(self.array[input_1]) != len(self.array[input_2]):
					print("XOR length mismatch")
					return None
				out_label = [a^b for (a,b) in zip(self.array[input_1],self.array[input_2])]
				self.array[out_addr] = bytes(out_label)

			elif gate == GateType.BUF:
				if len(data) != 5:
					print("length mismatch")
					return None
				input_1   = int.from_bytes(data[1:3], "little")
				out_addr  = int.from_bytes(data[3:5], "little")
				out_label = self.array[input_1]
				self.array[out_addr] = out_label
		return None

	def send_bytes(self, cmd: int, data: list) -> None:
		self._run_cmd(cmd, data)
	
	def recv_bytes(self, cmd: int, length: int) -> list:
		return self._run_cmd(cmd, [0]*length)


def get_fpga():
	fpga = FPGA()
	print("Emulating FPGA")
	return fpga
