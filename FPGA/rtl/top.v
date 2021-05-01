/*
 * top.v
 *
 * vim: ts=4 sw=4
 *
 * Copyright (C) 2019  Sylvain Munaut <tnt@246tNt.com>
 * All rights reserved.
 *
 * BSD 3-clause, see LICENSE.bsd
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the <organization> nor the
 *       names of its contributors may be used to endorse or promote products
 *       derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 * ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

`default_nettype none

module top (
	// SPI Slave interface
	input  wire slave_mosi,
	output wire slave_miso,
	input  wire slave_cs_n,
	input  wire slave_clk,

	// user I/O
	output wire [4:0] LEDs,
	//input  wire [3:0] BTNs,

	output wire [7:0] PMOD_1A,
	input  wire [7:0] PMOD_1B,
	input  wire clk_12m
);
	assign LEDs = 0;

	wire clk;
	wire clk_2x;
	wire rst;

	wire [7:0] spi_cmd;
	wire [7:0] spi_data;
	wire strobe_first;
	wire strobe_last;
	wire strobe_data;
	reg [7:0] spi_out;
	wire spi_out_first;
	wire spi_out_next;
	spi_fast spi_I (
		.spi_mosi(slave_mosi),
		.spi_miso(slave_miso),
		.spi_cs_n(slave_cs_n),
		.spi_clk(slave_clk),
		.addr(spi_cmd),
		.data(spi_data),
		.first(strobe_first),
		.last(strobe_last),
		.strobe(strobe_data),
		.out(spi_out),
		.out_first(spi_out_first),
		.out_next(spi_out_next),
		.clk(clk),
		.rst(rst)
	);
	reg [3:0] in_counter;
	reg [4:0] out_counter;
	always @ (posedge clk) begin
		if (strobe_data) begin
			if (spi_cmd == 0) begin
				if (strobe_first) begin
					in_counter <= 1;
					recv_buffer[0+:8] <= spi_data;
				end else begin
					in_counter <= in_counter + 1;
					recv_buffer[in_counter*8 +:8] <= spi_data;
				end
			end
		end
		if (spi_out_next) begin
			out_counter <= out_counter + 1;
			spi_out <= reply_buffer[out_counter*8 +:8];
		end else if (rst | strobe_last) begin
			out_counter <= -2-6;
			spi_out <= reply_buffer[0+:8];
		end
	end

	reg [127:0] recv_buffer;
	reg [127:0] reply_buffer;
	wire done;
	reg aes_start;
	aes aes_I (
		.clk(clk),
		.rst(rst),
		.start(aes_start),
		.done(done),
		.state_init(recv_buffer),
		.state_final(reply_buffer)
	);
	always @ (posedge clk) begin
		if (strobe_last && spi_cmd==0)
			aes_start <= 1;
		else
			aes_start <= 0;
	end
	seven_seg disp_I (
		.clk(clk),
		.inp(reply_buffer[PMOD_1B*8 +:8]),
		.pmod(PMOD_1A)
	);
/*
	wire read;
	wire write;

	hram hyperram (
	input         .i_clk(clk),
	input         .i_rstn(rst),

	input         .i_cfg_access(0),
	input         .i_mem_valid(),
	output        .o_mem_ready(),
	input  [ 3:0] .i_mem_wstrb(),
	input  [31:0] .i_mem_addr(),
	input  [31:0] .i_mem_wdata(),
	output [31:0] .o_mem_rdata(),

	output        .o_csn0(),
	output        .o_csn1(),
	output        .o_clk(),
	output        .o_clkn(),
	inout  [7:0]  .io_dq(PMOD_1B),
	inout         .io_rwds(PMOD_1A),
	output        .o_resetn(),
	);



	wire gate_strobe;
	wire id_1_strobe;
	wire id_2_strobe;
	wire ctxt_strobe;
	wire [1:0] gate_type;
	wire [23:0] id_1;
	wire [23:0] id_2;
	wire [7:0] ctxt_byte;
	spi_decoder spi_d_I (
		.input_data(spi_data),
		.input_command(spi_cmd),
		.input_strobe(strobe_data),

		.gate_type(gate_type),
		.id_1(id_1),
		.id_2(id_2),
		.ctxt_byte(ctxt_byte),
		.gate_strobe(gate_strobe),
		.id_1_strobe(id_1_strobe),
		.id_2_strobe(id_2_strobe),
		.ctxt_strobe(ctxt_strobe),

		.clk(clk),
		.rst(rst)
	);

	wire [127:0] read_data;
	ctxt_mem ctxt_m_I (
		.clk(clk),
		.rst(gate_strobe), // reset before ctxt
		.write_data(ctxt_byte),
		.write_strobe(ctxt_strobe),

		.read_addr(BTNs[2:1]+1),
		.read_data(read_data)
	);

	seven_seg disp_I (
		.clk(clk),
		.inp(counter),
		.pmod(PMOD_1A)
	);
*/

`ifdef NO_PLL
	reg [7:0] rst_cnt = 8'h00;
	wire rst_i;

	always @(posedge clk)
		if (~rst_cnt[7])
			rst_cnt <= rst_cnt + 1;

	wire rst_i = ~rst_cnt[7];

	SB_GB clk_gbuf_I (
		.USER_SIGNAL_TO_GLOBAL_BUFFER(clk_12m),
		.GLOBAL_BUFFER_OUTPUT(clk)
	);

	SB_GB rst_gbuf_I (
		.USER_SIGNAL_TO_GLOBAL_BUFFER(rst_i),
		.GLOBAL_BUFFER_OUTPUT(rst)
	);
`else
	sysmgr sys_mgr_I (
		.clk_in(clk_12m),
		.rst_in(1'b0),
		.clk_out(clk),
		.clk_2x_out(clk_2x),
		.rst_out(rst)
	);
`endif

endmodule // top
