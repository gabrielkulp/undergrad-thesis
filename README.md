# Mobile Cryptographic Coprocessor for Privacy-Preserving Two-Party Computation

![Logo](paper/extras/logo.png)

## Questions I think you might have

### What is this?
This is my undergraduate thesis project at Oregon State University for the Honors College. It's also my capstone project for the College of Engineering, school of Electrical Engineering and Computer Science. My advisor is [Dr. Mike Rosulek](https://web.engr.oregonstate.edu/~rosulekm/), an associate professor who focuses on cryptographic protocols for secure computation.

The goal of this project is to perform a secure two-party computation on a commodity smartphone (the [Pine64 PinePhone](https://wiki.pine64.org/index.php/PinePhone)) with the help of an FPGA coprocessor (the [iCE40 UP5K](https://github.com/icebreaker-fpga/icebreaker)), and for all code and configuration to be my own (within reason). This means I wrote my own cryptographic libraries and hardware. It's a bad idea to use self-made crypto (without extensive and ongoing review) in a security-sensitive situation, so this project only serves as a proof-of-concept.

### How do I run it?
Run `alice.py` and the `bob.py` in separate terminals (in that order, on different computers if you like) to evaluate the specified garbled circuit. You'll need a plaintext circuit definition file in the [Bristol Fashion](https://homes.esat.kuleuven.be/~nsmart/MPC/) format. The current implementation supports four gates: AND, XOR, INV, and EQW (referred to as BUF in some places).


### Architecture
Read the paper for all the fine details!
