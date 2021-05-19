#!/usr/bin/env python3
import time, random
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir+"/MPCPython")
from circuit import GateType
from fpga import get_fpga, Cmd

# spellchecker: ignore nums

pretty = lambda l: " ".join(["{:02x}".format(x) for x in l])

def throughput():
	fpga = get_fpga()
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
	fpga = get_fpga()
	if not fpga:
		return 1
	
	print("format: cmd, data")
	ad = lambda x: fpga.send_bytes(Cmd.addr, x)
	wr = lambda x: fpga.send_bytes(Cmd.write, x)
	rd = lambda: pretty(fpga.recv_bytes(Cmd.read, 16))

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
	fpga = get_fpga()
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


def gate_test():
	fpga = get_fpga()
	if not fpga:
		return 1

	# start by sending some inputs
	fpga.send_bytes(Cmd.addr,  [0,0])
	fpga.send_bytes(Cmd.write, [(8+x**2)%255 for x in range(16)])

	fpga.send_bytes(Cmd.addr,  [1,0])
	fpga.send_bytes(Cmd.write, [((x+9)*(8*x-4))%255 for x in range(16)])

	fpga.send_bytes(Cmd.addr,  [2,0])
	fpga.send_bytes(Cmd.write, [1]+([5]*15))

	fpga.send_bytes(Cmd.addr,  [3,0])
	fpga.send_bytes(Cmd.write, [1]+([3]*15))

	fpga.send_bytes(5, [0]*16) # should be ignored

#	for x in range(9):
#		fpga.send_bytes(cmd_addr, [x,0,0])
#		print(f"{x}:", pretty(fpga.recv_bytes(cmd_read, 16)))

	# then send gates

	#          type         id        gate id
#	gate_def = [GateType.BUF] + [1,0,0] + [3,0,0]
#	fpga.send_bytes(cmd_gates, gate_def)

	#          type         id 1      id 2      gate id
#	gate_def = [GateType.XOR] + [2,0,0] + [3,0,0] + [4,0,0]
#	fpga.send_bytes(cmd_gates, gate_def)

	ctxt  = list(bytearray.fromhex("66217c17175db79ea159514bbeef6072"))
	ctxts = ctxt + [x//2 for x in ctxt] + [(x*2)%256 for x in ctxt]
	fpga.send_bytes(Cmd.gates, [GateType.AND] + [0,0] + [1,0] + ctxts + [4,0])
	fpga.send_bytes(Cmd.gates, [GateType.AND] + [2,0] + [3,0] + ctxts + [5,0])

	fpga.send_bytes(Cmd.gates, [GateType.AND] + [0,0] + [1,0] + ctxts + [6,0])
	fpga.send_bytes(Cmd.gates, [GateType.AND] + [2,0] + [3,0] + ctxts + [7,0])

	fpga.send_bytes(Cmd.gates, [GateType.AND] + [2,0] + [3,0] + ([0]*48) + [8,0])

	# finally, check the result
	for x in range(9):
		fpga.send_bytes(Cmd.addr, [x,0])
		print(f"{x}:  ", pretty(fpga.recv_bytes(Cmd.read, 16)))


def main():
	gate_test()


if __name__ == '__main__':
	main()


#fpga = get_fpga()

#def read_many(n):
#	for x in range(n):
#		fpga.send_bytes(cmd_addr, [x,0,0])
#		print(f"{x}:", pretty(fpga.recv_bytes(cmd_read, 16)))
