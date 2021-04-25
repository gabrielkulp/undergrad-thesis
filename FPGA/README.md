# FPGA Co-Processor

This portion of the codebase deals with programming the FPGA. It includes the hardware description (Verilog) and the makefile, which converts this description into an FPGA configuration.

## Building

To build this portion of the project, you'll first need to install the open-source FPGA toolchain (Yosys, nextpnr, IceStorm, Icarus Verilog, SymbiFlow, and more). There are instructions on the [project homepage](https://wiki.icebreaker-fpga.com/wiki/Getting_started).

Next, you can just run `make prog` to synthesize the FPGA configuration and then push it to the device. You can run `stream.py` to demo encrypting a message with AES.

## iCEBreaker?

The [iCEBreaker](https://docs.icebreaker-fpga.org/hardware/icebreaker/) FPGA development board is an open-hardware platform designed to work well with the open-source toolchain.
