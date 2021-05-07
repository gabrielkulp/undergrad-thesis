`default_nettype none

module label_array (
	input wire clk,
	input wire rst,
	input wire [12:0] wire_id,    // address to read/write
	input wire id_strobe,         // bring high to latch inputs
	input wire wr_en,             // high = write, low = read
	input wire [127:0] label_in,  // write this if wr_en
	output reg [127:0] label_out, // value it read comes out here
	output reg done               // raised high after reading/writing
);
	reg  [13:0] ram_addr;
	reg  [63:0] ram_data_in;
	wire [63:0] ram_data_out;
	reg  ram_wr_en;

	// pipeline FSM
	reg  [1:0] state;
	localparam IDLE        = 0;
	localparam BUBBLE      = 1;
	localparam FIRST_HALF  = 2;
	localparam SECOND_HALF = 3;

	always @ (posedge clk) begin
		if (rst) begin
			state <= IDLE;
		end else begin
			case (state)
				IDLE: begin
					done <= 0;
					if (id_strobe) begin
						ram_wr_en   <= wr_en;
						ram_addr    <= {wire_id[12:0], 1'b0}; // fetch lower 64 bits
						ram_data_in <= label_in[0+:64];
						state       <= BUBBLE;
					end
				end
				// wait for first address to propagate, and assign second address
				BUBBLE: begin
					ram_addr[0] <= 1'b1; // fetch upper 64 bits
					ram_data_in <= label_in[64+:64];
					state       <= FIRST_HALF;
				end
				// data for first address is ready
				FIRST_HALF: begin
					label_out[0+:64] <= ram_data_out;
					state <= SECOND_HALF;
				end
				// data for second address is ready
				SECOND_HALF: begin
					label_out[64+:64] <= ram_data_out;
					done  <= 1;
					state <= IDLE;
				end
			endcase
		end
	end

	// Fetch and store 64 bits at a time by parallelizing SPRAM modules.

	SB_SPRAM256KA ram_0 (
		.ADDRESS(ram_addr),
		.DATAIN(ram_data_in[0+:16]),
		.MASKWREN(4'b1111),
		.WREN(ram_wr_en),
		.CHIPSELECT(1),
		.CLOCK(clk),
		.STANDBY(1'b0),
		.SLEEP(1'b0),
		.POWEROFF(1'b1),
		.DATAOUT(ram_data_out[0+:16])
	);

	SB_SPRAM256KA ram_1 (
		.ADDRESS(ram_addr),
		.DATAIN(ram_data_in[16+:16]),
		.MASKWREN(4'b1111),
		.WREN(ram_wr_en),
		.CHIPSELECT(1),
		.CLOCK(clk),
		.STANDBY(1'b0),
		.SLEEP(1'b0),
		.POWEROFF(1'b1),
		.DATAOUT(ram_data_out[16+:16])
	);

	SB_SPRAM256KA ram_2 (
		.ADDRESS(ram_addr),
		.DATAIN(ram_data_in[32+:16]),
		.MASKWREN(4'b1111),
		.WREN(ram_wr_en),
		.CHIPSELECT(1),
		.CLOCK(clk),
		.STANDBY(1'b0),
		.SLEEP(1'b0),
		.POWEROFF(1'b1),
		.DATAOUT(ram_data_out[32+:16])
	);

	SB_SPRAM256KA ram_3 (
		.ADDRESS(ram_addr),
		.DATAIN(ram_data_in[48+:16]),
		.MASKWREN(4'b1111),
		.WREN(ram_wr_en),
		.CHIPSELECT(1),
		.CLOCK(clk),
		.STANDBY(1'b0),
		.SLEEP(1'b0),
		.POWEROFF(1'b1),
		.DATAOUT(ram_data_out[48+:16])
	);
endmodule
