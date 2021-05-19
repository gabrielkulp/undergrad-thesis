from circuit import Circuit
from pyftdi.spi import SpiController
from pyftdi.usbtools import UsbToolsError
from pyftdi.ftdi import FtdiError
# spellchecker: ignore ftdi pyftdi udev
def enum(**named_values):
	return type("Enum", (), named_values)

Cmd = enum(addr=1, write=2, gates=3, read=4)
# Cmd.addr:  set address for next read or write
# Cmd.write: data to write at address (inputs)
# Cmd.gates: data to send through gate evaluation
# Cmd.read:  return data at address

class FPGA():
	def __init__(self, addr="ftdi://ftdi:2232h/1", spi_frequency=30e6, spi_cs=None):
		self.emu = False
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
	
	def send_bytes(self, cmd: int, data: list) -> None:
		self.slave.exchange(bytearray([cmd]) + bytearray(data), duplex=False)
	
	def recv_bytes(self, cmd: int, length: int) -> list:
		padding = 6
		data = [x for x in range(length+3+padding)]
		return self.slave.exchange(bytearray([cmd]) + bytearray(data), duplex=True)[4+padding:]

# constructor wrapper to handle errors in one spot
def get_fpga():
	try:
		fpga = FPGA()
		print("FPGA found and connected")
		return fpga
	except UsbToolsError:
		print("FPGA not found")
		return None
	except FtdiError:
		print("FPGA busy")
		return None
	except RuntimeError:
		print("FPGA connected but not listening")
		return None
	except ValueError:
		print("FPGA connected but misconfigured by udev. Wait a moment and try again.")
		return None
