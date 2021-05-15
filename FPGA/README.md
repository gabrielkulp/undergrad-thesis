# FPGA Co-Processor

This portion of the codebase deals with defining the FPGA configuration. It includes the hardware description (Verilog) and the makefile, which converts this description into an FPGA configuration.

## Building

To build this portion of the project, you'll first need to install the open-source FPGA toolchain for the iCE40 UP5K chip (Yosys, nextpnr, IceStorm, Icarus Verilog, SymbiFlow, and more). There are instructions on the [project homepage](https://wiki.icebreaker-fpga.com/wiki/Getting_started).

Next, you can just run `make prog` to synthesize the FPGA configuration and then push it to the device. You can run `stream.py` to evaluate a nonsense garbled circuit.

## Running

This portion of the project isn't meant to stand on its own. After building and flashing the FPGA, run the FPGA version of the Bob script in `MPCPython` and the FPGA will be put to good use!

## iCEBreaker?

The [iCEBreaker](https://docs.icebreaker-fpga.org/hardware/icebreaker/) FPGA development board is an open-hardware platform designed to work well with the open-source toolchain. I wrote this portion of the project to run on an iCEBreaker, and you would probably need to rewrite (at least) the SPI module to run it elsewhere.
