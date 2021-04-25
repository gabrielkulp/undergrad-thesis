#!/usr/bin/env python3
from pyftdi.spi import SpiController
from pyftdi.usbtools import UsbToolsError
import time, random

# spellchecker: ignore ftdi pyftdi

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

	def send_bytes(self, addr: int, data: list) -> None:
		return self.slave.exchange(bytearray([addr]) + bytearray(data), duplex=True)


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
	
	while True:
		try:
			inp = input("fpga > ")
		except EOFError:
			return
		try:
			ret = fpga.send_bytes(1,eval(inp))
			print(" ".join(["{:02x}".format(x) for x in ret]))
		except Exception as e:
			print("error:" + str(e))



def main():
	fpga = get_connection()
	if not fpga:
		return 1

	#gate_type = 0
	#id_1 = [0x12, 0x34, 0x56]
	#id_2 = [0x78, 0x9a, 0xbc]
	ctxts = [0x66, 0x21, 0x7c, 0x17, 0x17, 0x5d, 0xb7, 0x9e, 0xa1, 0x59, 0x51, 0x4b, 0xbe, 0xef, 0x60, 0x72]

	#gate_def = [gate_type] + id_1 + id_2 + ctxts + [x+1 for x in ctxts] + [(2*x)%256 for x in ctxts]

	fpga.send_bytes(0, bytearray([0]*16))
	time.sleep(0.1)
	print("received:", " ".join(["{:02x}".format(b) for b in fpga.send_bytes(1,[x for x in range(20)])[5:]]))
	print("expected:", "c6 a1 3b 37 87 8f 5b 82 6f 4f 81 62 a1 c8 d8 79")

	fpga.send_bytes(0, bytearray(ctxts))
	time.sleep(0.1)
	print("received:", " ".join(["{:02x}".format(b) for b in fpga.send_bytes(1,[x for x in range(20)])[5:]]))
	print("expected:", "b9 32 b1 5b a3 7b 86 44 08 30 cc 5f 21 6a 3b f5")


if __name__ == '__main__':
	main()
