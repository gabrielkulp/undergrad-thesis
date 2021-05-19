`default_nettype none

module top (
	// SPI Slave interface
	input  wire slave_mosi,
	output wire slave_miso,
	input  wire slave_cs_n,
	input  wire slave_clk,

	// user I/O
	output wire [4:0] LEDs,
	input  wire [3:0] BTNs,

	//output wire [7:0] PMOD_1A,
	//input  wire [7:0] PMOD_1B,
	input  wire clk_12m
);
	wire clk, clk_2x, rst;

	// debugging output
	reg error;
	assign LEDs = {5{error}};
	always @ (posedge clk)
		if (rst | ~BTNs[0])
			error <= 0;


	// Get data from SPI onto fabric

	wire [7:0] spi_cmd;
	wire [7:0] spi_data;
	wire       spi_first, spi_last, spi_strobe_data;
	reg  [7:0] spi_out;
	wire       spi_out_first, spi_out_next;

	wire   spi_strobe_first, spi_strobe_last;
	assign spi_strobe_first = spi_strobe_data & spi_first;
	assign spi_strobe_last  = spi_strobe_data & spi_last;
	spi_fast spi_I (
		.spi_mosi(slave_mosi),
		.spi_miso(slave_miso),
		.spi_cs_n(slave_cs_n),
		.spi_clk(slave_clk),
		.addr(spi_cmd),
		.data(spi_data),
		.first(spi_first),
		.last(spi_last),
		.strobe(spi_strobe_data),
		.out(spi_out),
		.out_first(spi_out_first),
		.out_next(spi_out_next),
		.clk(clk),
		.rst(rst)
	);



	// Handle direct memory access over SPI
	// for sending inputs and retrieving outputs

	localparam CMD_ADDR  = 1; // set address for reads and writes
	localparam CMD_WRITE = 2; // data to write at address (inputs)
	localparam CMD_GATES = 3; // data to send through gate evaluation
	localparam CMD_READ  = 4; // return data at address

	reg  [ 12:0] recv_addr;
	reg  [127:0] recv_data;
	wire [127:0] send_data;
	reg  [  4:0] in_counter;
	reg  [  4:0] out_counter;
	always @ (posedge clk) begin
		if (spi_strobe_data) begin // receive plaintext
			case (spi_cmd)
				CMD_ADDR: begin
					if (spi_strobe_first) begin
						in_counter <= 1;
						recv_addr[0+:8] <= spi_data;
					end else begin
						in_counter <= in_counter + 1;
						recv_addr[in_counter*8 +:8] <= spi_data;
					end
				end
				CMD_WRITE: begin
					if (spi_strobe_first) begin
						in_counter <= 1;
						recv_data[0+:8] <= spi_data;
					end else begin
						in_counter <= in_counter + 1;
						recv_data[in_counter*8 +:8] <= spi_data;
					end
				end
				// CMD_GATES handled below by spi_decoder
			endcase
		end
		// CMD_READ actually always happens here
		if (spi_out_next) begin // send reply from send_data register
			out_counter <= out_counter + 1;
			spi_out     <= send_data[out_counter*8 +:8];
		end else if (rst || spi_strobe_last) begin
			out_counter <= -2-6; // 6 bytes of extra padding
			spi_out     <= send_data[0+:8];
		end
	end
	assign send_data = label_out;



	// Deserialize SPI stream when receiving gate definitions

	wire gate_strobe, id_1_strobe, id_2_strobe, ctxt_strobe, gate_id_strobe;
	wire [  1:0] gate_type;
	wire [ 12:0] input_id;
	wire [127:0] ctxt;
	wire [  1:0] ctxt_recv_idx;
	wire [ 12:0] gate_id;
	spi_decoder spi_decoder_i (
		.input_data(spi_data),
		.input_strobe(spi_strobe_data & (spi_cmd == CMD_GATES)),

		.gate_type(gate_type),
		.input_id(input_id),
		.ctxt(ctxt),
		.gate_id(gate_id),

		.gate_strobe(gate_strobe),
		.id_1_strobe(id_1_strobe),
		.id_2_strobe(id_2_strobe),
		.ctxt_strobe(ctxt_strobe),
		.ctxt_idx(ctxt_recv_idx),
		.gate_id_strobe(gate_id_strobe),

		.clk(clk),
		.rst(rst)
	);



	// Main logic: pass gate definitions to label array
	// to fetch, compute new labels, and store results
	wire [12:0] wire_id_read;
	wire [12:0] wire_id_write;
	assign wire_id_read  = (spi_cmd == CMD_GATES) ? input_id : recv_addr;
	assign wire_id_write = (spi_cmd == CMD_GATES) ? gate_id  : recv_addr;

	wire [127:0] label_out;
	reg  [127:0] new_label;

	wire l_ctl_done;
	reg  l_ctl_store;

	localparam AND_GATE = 0;
	localparam XOR_GATE = 1;
	localparam BUF_GATE = 2;

	reg [2:0] state;
	localparam IDLE       = 0;
	localparam WAIT_L_CTL = 1;
	localparam WAIT_AES   = 2;
	localparam WAIT_CTXT  = 3;
	localparam WAIT_ID    = 4;
	always @ (posedge clk) begin
		if (rst) begin
			state <= IDLE;
			l_ctl_store <= 0;
			aes_start <= 0;
		end else begin
			case (state)
				IDLE: begin // wait until last input addr received
					l_ctl_store <= 0;
					if (gate_id_strobe)
						error <= 1;
					if ((gate_type == BUF_GATE) & id_1_strobe) begin
						state <= WAIT_L_CTL;
					end else if (id_2_strobe) begin
						state <= WAIT_L_CTL;
					end
				end
				WAIT_L_CTL: begin // last input addr received, so wait for fetch
					if (gate_id_strobe | ctxt_strobe)
						error <= 1;
					if (l_ctl_done) begin
						new_label <= label_out;
						if (gate_type == AND_GATE) begin
							aes_start <= 1;
							state <= WAIT_AES;
						end else begin
							state <= WAIT_ID;
						end
					end
				end
				WAIT_AES: begin // wait for encryption to finish
					aes_start <= 0;
					if (gate_id_strobe | ctxt_strobe)
						error <= 1;
					if (aes_done) begin
						if (ctxt_point == 0) begin // ctxt_point of 0 means ctxt is 0
//							new_label <= aes_out;
							state <= WAIT_ID;
						end else begin // otherwise wait for ctxt over serial
							state <= WAIT_CTXT;
						end
					end
				end
				WAIT_CTXT: begin // wait for the right ctxt to arrive
					if (gate_id_strobe)
						error <= 1;
					if (ctxt_strobe & (ctxt_recv_idx == ctxt_point)) begin
						new_label <= aes_out ^ ctxt;
						state <= WAIT_ID;
					end
				end
				WAIT_ID: begin // wait for storage location
					if (gate_strobe)
						error <= 1;
					if (gate_id_strobe) begin
						if ((gate_type == AND_GATE) & (ctxt_point == 0))
							new_label <= aes_out;
						l_ctl_store <= 1;
						state <= IDLE;
					end
				end
			endcase
		end
	end

	wire [1:0] ctxt_point;
	label_ctl label_ctl_i (
		.clk(clk),
		.rst(rst),

		.done(l_ctl_done),

		// fetching
		// fetch whenever the address changes
		.wire_id_read(wire_id_read),
		.id_1_strobe(id_1_strobe | ((spi_cmd == CMD_ADDR) & spi_strobe_last)),
		.id_2_strobe(id_2_strobe),
		.gate_type(gate_type),
		.label_out(label_out),
		.ctxt_point(ctxt_point),

		// storing
		.wire_id_write(wire_id_write),
		.store_strobe(l_ctl_store | ((spi_cmd == CMD_WRITE) & spi_strobe_last)),
		.label_in((spi_cmd != CMD_WRITE) ? new_label : recv_data)
	);



	reg  aes_start;
	wire aes_done;
	wire [127:0] aes_out;
	aes enc (
		.clk(clk),
		.rst(rst),

		.state_init(label_out),
		.start(aes_start),

		.done(aes_done),
		.state_final(aes_out)
	);



// Copyright (C) 2019 Sylvain Munaut <tnt@246tNt.com>
// All rights reserved
// Licensed under 3-clause BSD license
// spellchecker: ignore gbuf sysmgr
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

endmodule
