// this module reads in gate definitions and parallelizes the config fields
`default_nettype none

module spi_decoder (
	// SPI interface
	input wire [7:0] input_data,
	input wire input_strobe,

	// Deserialized outputs
	output reg [  1:0] gate_type,
	output reg [ 12:0] input_id,
	output reg [127:0] ctxt,
	output reg [ 12:0] gate_id,

	// Context for control unit
	output reg gate_strobe, // gate type is ready
	output reg id_1_strobe,
	output reg id_2_strobe,
	output reg ctxt_strobe,
	output wire [1:0] ctxt_idx, // which ctxt received?
	output reg gate_id_strobe, // output storage location

	// Clock and reset
	input wire clk,
	input wire rst
);

	assign ctxt_idx[1:0] = ctxt_counter[5:4];

	// FSM variables
	reg [2:0] recv_state; // which field to listen for
	localparam RECV_GATE_TYPE = 0;
	localparam RECV_ID_1      = 1;
	localparam RECV_ID_2      = 2;
	localparam RECV_CTXT      = 3;
	localparam RECV_GATE_ID   = 4;

	// gate types
	localparam AND_GATE = 0;
	localparam XOR_GATE = 1;
	localparam BUF_GATE = 2;

	reg [1:0] id_counter; // which byte of an id are we on
	reg [5:0] ctxt_counter;  // which ctxt byte are we on
	always @ (posedge clk) begin
		if (rst) begin
			recv_state <= RECV_GATE_TYPE;
		end else if (input_strobe) begin
			case (recv_state)
				RECV_GATE_TYPE: begin
					gate_type <= input_data[1:0];
					id_counter <= 0;
					gate_strobe <= 1;
					recv_state <= RECV_ID_1;
				end
				RECV_ID_1: begin
					if (id_counter == 0) begin
						id_counter <= 1;
						input_id[7:0] <= input_data;
					end else begin
						input_id[12:8] <= input_data[4:0];
						id_1_strobe <= 1;
						if (gate_type == BUF_GATE) begin
							recv_state <= RECV_GATE_ID;
						end else begin // else AND or XOR
							recv_state <= RECV_ID_2;
						end
						id_counter <= 0;
					end
				end
				RECV_ID_2: begin // XOR and AND gates
					ctxt_counter <= 0;
					if (id_counter == 0) begin
						id_counter <= 1;
						input_id[7:0] <= input_data;
					end else begin
						input_id[12:8] <= input_data[4:0];
						id_2_strobe <= 1;
						if (gate_type == AND_GATE) begin
							recv_state <= RECV_CTXT;
						end else begin // else XOR gate
							recv_state <= RECV_GATE_ID;
						end
						id_counter <= 0;
					end
				end
				RECV_CTXT: begin // ctxt_counter = {ctxt_idx, byte index}
					ctxt_counter <= ctxt_counter + 1;
					ctxt[ctxt_counter[3:0]*8 +:8] <= input_data;

					// if just received the 16th byte of each ctxt
					if (ctxt_counter[3:0] == 4'b1111) begin
						ctxt_strobe <= 1;
						if (ctxt_idx == 2)
							recv_state <= RECV_GATE_ID;
					end
				end
				RECV_GATE_ID: begin
					id_counter <= 1;
					if (id_counter == 0) begin
						gate_id[7:0] <= input_data;
					end else begin
						gate_id[12:8] <= input_data[4:0];
						gate_id_strobe <= 1;
						recv_state <= RECV_GATE_TYPE;
					end
				end
			endcase
		end else begin // not input_strobe
			// reset strobes after a cycle
			gate_strobe <= 0;
			id_1_strobe <= 0;
			id_2_strobe <= 0;
			ctxt_strobe <= 0;
			gate_id_strobe <= 0;
		end
	end

endmodule
