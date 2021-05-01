`default_nettype none

// Get the segments to illuminate to display a single hex digit.
// N.B., This is positive logic.  Display needs negative.
module digit_to_segments(
	input wire clk,
	input [3:0] digit,
	output reg[6:0] segments
);
	wire [16*7-1:0] segment_map;
	assign segment_map = {
		7'b1110001, // F
		7'b1111001, // E
		7'b1011110, // d
		7'b0111001, // C
		7'b1111100, // b
		7'b1110111, // A
		7'b1101111, // 9
		7'b1111111, // 8
		7'b0000111, // 7
		7'b1111101, // 6
		7'b1101101, // 5
		7'b1100110, // 4
		7'b1001111, // 3
		7'b1011011, // 2
		7'b0000110, // 1
		7'b0111111  // 0
	};
	always @ (posedge clk)
		segments <= segment_map[digit*7 +: 7];
/*
	always @(posedge clk)
		
		case (digit)
			4'h0: segments <= 7'b0111111;
			4'h1: segments <= 7'b0000110;
			4'h2: segments <= 7'b1011011;
			4'h3: segments <= 7'b1001111;
			4'h4: segments <= 7'b1100110;
			4'h5: segments <= 7'b1101101;
			4'h6: segments <= 7'b1111101;
			4'h7: segments <= 7'b0000111;
			4'h8: segments <= 7'b1111111;
			4'h9: segments <= 7'b1101111;
			4'hA: segments <= 7'b1110111;
			4'hB: segments <= 7'b1111100;
			4'hC: segments <= 7'b0111001;
			4'hD: segments <= 7'b1011110;
			4'hE: segments <= 7'b1111001;
			4'hF: segments <= 7'b1110001;
		endcase
		*/

endmodule

module seven_seg(
			input  clk,
			input  [7:0] inp,
			output [7:0] pmod
			);

	// Wiring external pins.
	reg [6:0] seg_pins;
	reg       digit_sel;
	assign pmod[6:0] = seg_pins;
	assign pmod[7]   = digit_sel;

	reg [10:0] counter;
	wire [3:0] nibble_l = inp[3:0];
	wire [3:0] nibble_h = inp[7:4];
	wire [2:0] display_state = counter[10 -: 3];

	reg [6:0]  low_segments;
	reg [6:0]  high_segments;

	digit_to_segments lo2segs(clk, nibble_l, low_segments);
	digit_to_segments hi2segs(clk, nibble_h, high_segments);

	always @(posedge clk) begin
		counter <= counter + 1;

		// Switch seg_pins off during digit_sel transitions
		// to prevent flicker.  Each digit has 25% duty cycle.
		case (display_state)
			0, 1: seg_pins  <= ~low_segments;
			2:    seg_pins  <= ~0;
			3:    digit_sel <=  0;
			4, 5: seg_pins  <= ~high_segments;
			6:    seg_pins  <= ~0;
			7:    digit_sel <=  1;
		endcase
	end

endmodule // top
