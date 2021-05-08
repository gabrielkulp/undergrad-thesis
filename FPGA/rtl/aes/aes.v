`default_nettype none
module aes (
	input  wire clk,
	input  wire rst,
	input  wire [127:0] state_init,
	input  wire start,
	output reg  done,
	output wire [127:0] state_final
);
	// main AES state and its flattened output
	reg [31:0] aes_state [3:0];

	assign state_final[0  +:32] = aes_state[0];
	assign state_final[32 +:32] = aes_state[1];
	assign state_final[64 +:32] = aes_state[2];
	assign state_final[96 +:32] = aes_state[3];

	// key schedule and state counters
	reg  [ 1:0] column;
	reg  [ 3:0] round;
	wire [31:0] key_a;
	wire [31:0] key_b;
	key_schedule keys_a (clk, column,      round, key_a);
	key_schedule keys_b (clk, column+1'b1, round, key_b);

	// T-tables for first 2 bytes of each column
	reg [7:0] t_addr_a [3:0];
	wire [31:0] t_a [3:0];
	tables table_a (clk,
		t_addr_a[0], t_a[0],
		t_addr_a[1], t_a[1],
		t_addr_a[2], t_a[2],
		t_addr_a[3], t_a[3]
	);

	// T-tables for second 2 bytes of each column
	reg [7:0] t_addr_b [3:0];
	wire [31:0] t_b [3:0];
	tables table_b (clk,
		t_addr_b[0], t_b[0],
		t_addr_b[1], t_b[1],
		t_addr_b[2], t_b[2],
		t_addr_b[3], t_b[3]
	);

	// main FSM
	reg [2:0] curr_state;
	reg [2:0] next_state;
	localparam BUBBLE = -1;
	localparam IDLE  = 0;
	localparam INIT  = 1;
	localparam ROUND = 2;
	localparam FINAL = 3;

	integer i;
	always @ (posedge clk) begin
		if (rst) begin
			curr_state <= IDLE;
			done       <= 0;
		end else begin

			case (curr_state)
				IDLE: begin
					if (start) begin
						aes_state[0] <= state_init[0*32 +:32];
						aes_state[1] <= state_init[1*32 +:32];
						aes_state[2] <= state_init[2*32 +:32];
						aes_state[3] <= state_init[3*32 +:32];

						curr_state <= BUBBLE;
						next_state <= INIT;
						column <= 0;
						round  <= 0;
						done   <= 0;
					end
				end

				BUBBLE: begin
					curr_state <= next_state;
					column <= column + 2;

					// load addressed for columns 2 and 3
					t_addr_a[0] <= aes_state[2][ 0+:8];
					t_addr_a[1] <= aes_state[3][ 8+:8];
					t_addr_a[2] <= aes_state[0][16+:8];
					t_addr_a[3] <= aes_state[1][24+:8];

					t_addr_b[0] <= aes_state[3][ 0+:8];
					t_addr_b[1] <= aes_state[0][ 8+:8];
					t_addr_b[2] <= aes_state[1][16+:8];
					t_addr_b[3] <= aes_state[2][24+:8];
				end

				// start by XOR-ing the state with the key
				INIT: begin
					if (column == 2) begin // first cycle
						column <= 0;
						aes_state[0][31:0] <= aes_state[0] ^ key_a;
						aes_state[1][31:0] <= aes_state[1] ^ key_b;
					end else begin // second cycle
						round <= 1;
						aes_state[2][31:0] <= aes_state[2] ^ key_a;
						aes_state[3][31:0] <= aes_state[3] ^ key_b;

						curr_state <= BUBBLE;
						next_state <= ROUND;

						// load addresses for columns 0 and 1
						t_addr_a[0] <= aes_state[0][0*8 +:8];
						t_addr_a[1] <= aes_state[1][1*8 +:8];
						t_addr_a[2] <= aes_state[2][2*8 +:8] ^ key_a[2*8 +:8];
						t_addr_a[3] <= aes_state[3][3*8 +:8] ^ key_b[3*8 +:8];

						t_addr_b[0] <= aes_state[1][0*8 +:8];
						t_addr_b[1] <= aes_state[2][1*8 +:8] ^ key_a[1*8 +:8];
						t_addr_b[2] <= aes_state[3][2*8 +:8] ^ key_b[2*8 +:8];
						t_addr_b[3] <= aes_state[0][3*8 +:8];
					end
				end

				// 9 rounds with 128-bit key and block
				ROUND: begin
					if (column == 2) begin // first cycle
						aes_state[0] <= t_a[0] ^ t_a[1] ^ t_a[2] ^ t_a[3] ^ key_a;
						aes_state[1] <= t_b[0] ^ t_b[1] ^ t_b[2] ^ t_b[3] ^ key_b;
						column <= 0;
					end else begin // second cycle
						aes_state[2] <= t_a[0] ^ t_a[1] ^ t_a[2] ^ t_a[3] ^ key_a;
						aes_state[3] <= t_b[0] ^ t_b[1] ^ t_b[2] ^ t_b[3] ^ key_b;

						// load addresses for columns 0 and 1
						t_addr_a[0] <= aes_state[0][ 0+:8];
						t_addr_a[1] <= aes_state[1][ 8+:8];
						t_addr_a[2] <= t_a[0][16+:8] ^ t_a[1][16+:8] ^ t_a[2][16+:8] ^ t_a[3][16+:8] ^ key_a[16+:8];
						t_addr_a[3] <= t_b[0][24+:8] ^ t_b[1][24+:8] ^ t_b[2][24+:8] ^ t_b[3][24+:8] ^ key_b[24+:8];

						t_addr_b[0] <= aes_state[1][ 0+:8];
						t_addr_b[1] <= t_a[0][ 8+:8] ^ t_a[1][ 8+:8] ^ t_a[2][ 8+:8] ^ t_a[3][ 8+:8] ^ key_a[ 8+:8];
						t_addr_b[2] <= t_b[0][16+:8] ^ t_b[1][16+:8] ^ t_b[2][16+:8] ^ t_b[3][16+:8] ^ key_b[16+:8];
						t_addr_b[3] <= aes_state[0][24+:8];

						round <= round + 1;
						curr_state <= BUBBLE;
						next_state <= (round == 9) ? FINAL : ROUND;
					end
				end

				// No MixColumns for the last round, so it's a bit different
				FINAL: begin
					if (column == 2) begin // first cycle
						// mask off the table entries to make S-boxes.
						// Timing violations on these next two lines!!
						aes_state[0] <= {t_a[3][0+:8], t_a[2][24+:8], t_a[1][16+:8], t_a[0][8+:8]} ^ key_a;
						aes_state[1] <= {t_b[3][0+:8], t_b[2][24+:8], t_b[1][16+:8], t_b[0][8+:8]} ^ key_b;
						column <= 0;

					end else begin // second cycle
						aes_state[2] <= {t_a[3][0+:8], t_a[2][24+:8], t_a[1][16+:8], t_a[0][8+:8]} ^ key_a;
						aes_state[3] <= {t_b[3][0+:8], t_b[2][24+:8], t_b[1][16+:8], t_b[0][8+:8]} ^ key_b;

						done <= 1;
						curr_state <= IDLE;
					end
				end
			endcase
		end
	end

endmodule
