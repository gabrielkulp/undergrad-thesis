#!/usr/bin/env python3
from pyftdi.spi import SpiController
from pyftdi.usbtools import UsbToolsError
import time, random

# spellchecker: ignore ftdi pyftdi udev nums

class FPGA_connection():
	def __init__(self, addr="ftdi://ftdi:2232h/1", spi_frequency=30e6, spi_cs=None):
		# SPI link
		self.spi_frequency = spi_frequency
		self.spi = SpiController(cs_count=3)
		self.spi.configure(addr)

		if spi_cs is not None:
			self.slave = self.spi.get_port(cs=spi_cs, freq=self.spi_frequency, mode=0)
		else:
			self.slave = self._spi_probe()

	def _spi_probe(self):
		for cs in [0, 2]:
			port = self.spi.get_port(cs=cs, freq=self.spi_frequency, mode=0)
			r = port.exchange(b'\x00', duplex=True)[0]
			if r != 0xff:
				return port
			#return port
		raise RuntimeError("Automatic SPI CS probe failed")

	def recv_byte(self) -> int:
		rv = self.slave.exchange(bytearray(2), duplex=True)
		return rv[0] | rv[1]
	
	def send_byte(self, data: int) -> None:
		self.slave.exchange(bytearray([0, data]))
	
	def duplex_bytes(self, cmd: int, data: list) -> list:
		return self.slave.exchange(bytearray([cmd]) + bytearray(data), duplex=True)

	def send_bytes(self, cmd: int, data: list) -> None:
		self.slave.exchange(bytearray([cmd]) + bytearray(data), duplex=False)
	
	def recv_bytes(self, cmd: int, length: int) -> list:
		padding = 6
		data = [x for x in range(length+3+padding)]
		return self.slave.exchange(bytearray([cmd]) + bytearray(data), duplex=True)[4+padding:]

pretty = lambda l: " ".join(["{:02x}".format(x) for x in l])

def get_connection():
	try:
		fpga = FPGA_connection()
		print("FPGA found and connected")
		return fpga
	except UsbToolsError:
		print("FPGA not found")
		return None
	except RuntimeError:
		print("FPGA connected but not listening")
		return None
	except ValueError:
		print("FPGA connected but misconfigured by udev. Wait a moment and try again.")
		return None


def throughput():
	fpga = get_connection()
	if not fpga:
		return 1

	test_count = 1000
	test_size  = 5000
	nums = [random.randint(0,255) for _ in range(test_size)]
	print(f"starting timed test ({test_count} iterations)")

	start = time.time()
	for _ in range(test_count):
		fpga.send_bytes(1, nums)
	stop = time.time()

	#expected = sum(nums)%256

	#print("expecting:", hex(expected), "received result:", hex(fpga.recv_byte()))
	speed = (test_size*test_count)/(stop-start)
	print(f"averaged {int(speed)} bytes per second ({round(speed/50000, 2)}x speedup over I2C)")

	#print("should get the same response again...", hex(fpga.recv_byte()))


def console():
	fpga = get_connection()
	if not fpga:
		return 1
	
	print("format: cmd, data")
	ad = lambda x: fpga.send_bytes(cmd_addr, x)
	wr = lambda x: fpga.send_bytes(cmd_write, x)
	rd = lambda: pretty(fpga.recv_bytes(cmd_read, 16))

	while True:
		try:
			inp = input("fpga > ")
		except EOFError:
			return ad, wr, rd # get rid of "unused var" warning
		try:
			cmd = inp.split(' ')[0]
			rest = ' '.join(inp.split(' ')[1:])
			ret = eval(f"{cmd}({rest})")
			if (ret):
				print(ret)
		except Exception as e:
			print("error:" + str(e))

	#while True:
	#	try:
	#		inp = input("fpga > ")
	#	except EOFError:
	#		return
	#	try:
	#		(cmd, dat) = eval('('+inp+')')
	#		ret = fpga.duplex_bytes(cmd, dat)
	#		print(pretty(ret))
	#	except Exception as e:
	#		print("error:" + str(e))


def aes_test():
	fpga = get_connection()
	if not fpga:
		return 1

	fpga.send_bytes(1, bytearray([0]*16))
	time.sleep(0.2)
	print("\nreceived:", pretty(fpga.recv_bytes(2,16)))
	print("expected: c6 a1 3b 37 87 8f 5b 82 6f 4f 81 62 a1 c8 d8 79\n")

	fpga.send_bytes(1, bytearray.fromhex("66217c17175db79ea159514bbeef6072"))
	time.sleep(0.2)
	print("received:", pretty(fpga.recv_bytes(2,16)))
	print("expected: b9 32 b1 5b a3 7b 86 44 08 30 cc 5f 21 6a 3b f5")


cmd_addr  = 1 # set address for read or write
cmd_write = 2 # data to write at address (inputs)
cmd_gates = 3 # data to send through gate evaluation
cmd_read  = 4 # return data at address

gate_and = 0
gate_xor = 1
gate_buf = 2

def gate_test():
	fpga = get_connection()
	if not fpga:
		return 1

	# start by sending some inputs
	fpga.send_bytes(cmd_addr,  [0,0,0])
	fpga.send_bytes(cmd_write, [(8+x**2)%255 for x in range(16)])

	fpga.send_bytes(cmd_addr,  [1,0,0])
	fpga.send_bytes(cmd_write, [((x+9)*(8*x-4))%255 for x in range(16)])

	fpga.send_bytes(cmd_addr,  [2,0,0])
	fpga.send_bytes(cmd_write, [1]+([5]*15))

	fpga.send_bytes(cmd_addr,  [3,0,0])
	fpga.send_bytes(cmd_write, [1]+([3]*15))

	fpga.send_bytes(5, [0]*16) # should be ignored

#	for x in range(9):
#		fpga.send_bytes(cmd_addr, [x,0,0])
#		print(f"{x}:", pretty(fpga.recv_bytes(cmd_read, 16)))

	# then send gates

	#          type         id        gate id
#	gate_def = [gate_buf] + [1,0,0] + [3,0,0]
#	fpga.send_bytes(cmd_gates, gate_def)

	#          type         id 1      id 2      gate id
#	gate_def = [gate_xor] + [2,0,0] + [3,0,0] + [4,0,0]
#	fpga.send_bytes(cmd_gates, gate_def)

	ctxt  = list(bytearray.fromhex("66217c17175db79ea159514bbeef6072"))
	ctxts = ctxt + [x//2 for x in ctxt] + [(x*2)%256 for x in ctxt]
	fpga.send_bytes(cmd_gates, [gate_and] + [0,0,0] + [1,0,0] + ctxts + [4,0,0])
	fpga.send_bytes(cmd_gates, [gate_and] + [2,0,0] + [3,0,0] + ctxts + [5,0,0])

	fpga.send_bytes(cmd_gates, [gate_and] + [0,0,0] + [1,0,0] + ctxts + [6,0,0])
	fpga.send_bytes(cmd_gates, [gate_and] + [2,0,0] + [3,0,0] + ctxts + [7,0,0])

	fpga.send_bytes(cmd_gates, [gate_and] + [2,0,0] + [3,0,0] + ([0]*48) + [8,0,0])

	# finally, check the result
	for x in range(9):
		fpga.send_bytes(cmd_addr, [x,0,0])
		print(f"{x}:  ", pretty(fpga.recv_bytes(cmd_read, 16)))


def main():
	gate_test()


if __name__ == '__main__':
	main()


#fpga = get_connection()

#def read_many(n):
#	for x in range(n):
#		fpga.send_bytes(cmd_addr, [x,0,0])
#		print(f"{x}:", pretty(fpga.recv_bytes(cmd_read, 16)))
