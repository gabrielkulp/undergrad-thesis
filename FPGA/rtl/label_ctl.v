`default_nettype none

module label_ctl (
	input wire clk,
	input wire rst,

	output reg done,

	// fetching
	input wire [23:0] wire_id_read,
	input wire id_1_strobe,
	input wire id_2_strobe,
	input wire [  1:0] gate_type,
	output reg [127:0] label_out, // BUF/INV, XOR, or AND-plaintext
	output reg [  1:0] ctxt_point, // point and permute pointer

	// storing
	input wire [23:0] wire_id_write,
	input wire store_strobe,
	input wire [127:0] label_in
);
	wire array_done;
	wire [127:0] array_out;
	reg  array_strobe;

	wire [127:0] wire_id;
	assign wire_id = wr_en ? wire_id_write : wire_id_read;

	always @ (posedge clk)
		array_strobe <= (id_1_strobe | id_2_strobe | store_strobe);

	reg wr_en;
	label_array label_array_i (
		.clk(clk),
		.rst(rst),
		.wire_id(wire_id[12:0]),
		.id_strobe(array_strobe),
		.wr_en(wr_en),
		.label_in(label_in),
		.label_out(array_out),
		.done(array_done)
	);

	// FSM
	reg [1:0] state;
	localparam IDLE    = 0;
	localparam FETCH_1 = 1;
	localparam FETCH_2 = 2;
	localparam STORE   = 3;

	// gate types
	localparam AND_GATE = 0;
	localparam XOR_GATE = 1;
	localparam BUF_GATE = 2;

	always @ (posedge clk) begin
		if (rst) begin
			state <= IDLE;
			done  <= 0;
		end else begin
			case (state)
				IDLE: begin
					done <= 0;
					if (id_1_strobe) begin
						state <= FETCH_1;
						wr_en <= 0;
					end else if (id_2_strobe) begin
						state <= FETCH_2;
						wr_en <= 0;
					end else if (store_strobe) begin
						state <= STORE;
						wr_en <= 1;
					end
				end
				FETCH_1: begin
					if (array_done) begin
						state <= IDLE;
						label_out <= array_out;
						done <= 1;
					end
				end
				FETCH_2: begin
					if (array_done) begin
						/*
						assuming FETCH_1 happened before this,
						label_out holds the first input wire label and
						array_out holds the second input wire label
						*/
						state <= IDLE;
						ctxt_point <= {label_out[0], array_out[0]};
						done <= 1;

						if (gate_type == AND_GATE)
							label_out <= {array_out[126:0] ^ label_out[126:0], 1'b0};
						else 
							label_out <= label_out ^ array_out;
					end
				end
				STORE: begin
					if (array_done) begin
						label_out <= label_in;
						state <= IDLE;
						done  <= 1;
					end
				end
			endcase
		end
	end
endmodule
