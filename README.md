# Mobile Cryptographic Co-Processor for Privacy-Preserving Two-Party Computation

## Questions I think you might have

### What is this?
This is my undergraduate thesis project at Oregon State University for the Honors College. It's also my capstone project for the College of Engineering, school of Electrical Engineering and Computer Science. My advisor is [Dr. Mike Rosulek](https://web.engr.oregonstate.edu/~rosulekm/), an associate professor who focuses on cryptographic protocols for secure computation.

The goal of this project is to perform a secure two-party computation on a commodity smartphone (the Pine64 [PinePhone](https://wiki.pine64.org/index.php/PinePhone)) with the help of an FPGA coprocessor, and for all code and configuration to be my own (within reason). This means I will be writing my own cryptographic libraries and hardware. It's a bad idea to use self-made crypto (without extensive and ongoing review) in a security-sensitive situation, so this project only serves as a proof-of-concept.

### How do I run it?
For now, just sit tight. If you really want to execute something, you can run `alice.py` and the `bob.py` in separate terminals (in that order) to perform an oblivious transfer.

## Architecture
I'm first writing code to perform Yao's Garbled Circuits in Python. Once that's working, I'll rewrite in C or Rust. Once that's working, I'll rewrite the main performance-critical loop in Verilog and connect the software and hardware implementations over I<sup>2</sup>C. This isn't a particularly fast connection, but it's what's available via the PinePhone pogo pins.
