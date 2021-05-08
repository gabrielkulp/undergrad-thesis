`default_nettype none
// uses 8 BRAMs
module tables (
	input  wire clk,

	input  wire [7:0]  addr_t0,
	output wire [31:0] data_t0,

	input  wire [7:0]  addr_t1,
	output wire [31:0] data_t1,

	input  wire [7:0]  addr_t2,
	output wire [31:0] data_t2,

	input  wire [7:0]  addr_t3,
	output wire [31:0] data_t3
);
	/*
		These tables help perform a round transformation
		by combining SubBytes, ShiftRows, and MixColumns
		into a single lookup. Each pair of tables allow
		an 8-bit address to return a 32-bit column of
		the state matrix ready for XOR. This requires
		one fetch cycle for each column of each round
		and uses eight BRAM blocks.
	*/

	/* ---------------------------------------------- */
	/* === T-tables auto-generated by gen_bram.py === */
	/* ---------------------------------------------- */

	SB_RAM40_4K #(
		.INIT_0(256'h76ecab4dd7b5fee72b5667ce01023060c5916fde6bd6f2ff7bf677ee7cf863c6),
		.INIT_1(256'hc09b72e4a4539c23af45a25fd4b3ad41f0fb478e59b2faef7dfac989821fca8f),
		.INIT_2(256'h152a3162d8ab71e2f1f9e5d1a5513468cc83f7f53f7e366c264c933dfde1b775),
		.INIT_3(256'h75eab27f274eebcde2df801b1224070e9a2f050a96371830c39d2346c7950408),
		.INIT_4(256'h84132f5ee3dd2952b37dd6b73b7652a4a05b5ab46edc1b361a342c58831d0912),
		.INIT_5(256'hcf8558b04c984a943972be67cb8d6ad45bb6b179fce32040edc10000d1b953a6),
		.INIT_6(256'ha84b9f253c7850a07ffe0204f9e9458a851133664d9a4386fbedaa4fefc5d0bb),
		.INIT_7(256'hd2bff3fdffe510202142daafb677bc63f5f138709d21923f8f054080a35d51a2),
		.INIT_8(256'h73e619325dba64c83d7a7efca755c493172e448897355fbeecc313260c18cd81),
		.INIT_9(256'hdbad0b165ebcdea71428b86beec7468c880b903b2a542244dca34f9e811960c0),
		.INIT_A(256'h79f2e4d39531913962c4ac43d3bdc29f5cb82448060c49920a143a743264e0db),
		.INIT_B(256'h0810ae477af465caeacff4f356ac6cd8a9494e9cd5b18d016dda376ec88be7d5),
		.INIT_C(256'h8a0f8b0dbd614b961f3e74e8dda1e8cbc697b473a6571c382e5c254a78f0ba6f),
		.INIT_D(256'h9e271d3ac1998617b96957ae356a61c20e1cf6f70306489066ccb5713e7c70e0),
		.INIT_E(256'hdfa5285055aace87e9c987151e3c9b2d94338e07d9a969d21122982bf8ebe1d9),
		.INIT_F(256'h162cbb6d54a8b07b0f1e2d5a9929418268d04284e6d7bf650d1a8909a1598c03)
	) table_0_lo (
		.RADDR({3'b0, addr_t0}),
		.RDATA({data_t0[15:0]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);

	SB_RAM40_4K #(
		.INIT_0(256'h9a76e6ab62d719fe7d2ba9670301503054c5b16fbd6b0df28d7b9977847ca563),
		.INIT_1(256'h5bc09672f7a4bf9ceaaffda267d4ecad0bf0c947eb5915fa877d40c99d8245ca),
		.INIT_2(256'h3f15533173d8937108f134e5f4a55c344fcc02f7413f5a366a26ae931cfdc2b7),
		.INIT_3(256'h9f75cdb2692726eb3de29b8036120907b59a0f05a19628185ec3652352c70c04),
		.INIT_4(256'h9784712f3ee37b29ceb361d64d3bf652fba0ee5ab26e2d1b2e1a742c9e831b09),
		.INIT_5(256'h4acfe858d44cde4a4b39d9be46cbbe6aed5bc8b11ffc60202ced000068d1f553),
		.INIT_6(256'he3a8ba9f443cf050817f060210f9cf4594855533d74dc54316fbe5aa2aef6bd0),
		.INIT_7(256'h6dd20ef31aff3010632175dac1b6dfbc04f54838bc9dad928a8fc040fea3f351),
		.INIT_8(256'h95732b19e75dac64473d827ef2a757c43917cc44a297e15f2fec3513140c4ccd),
		.INIT_9(256'h76db1d0be25e79de3c14d3b829eeca468388ab907e2a66227fdcd14f9881a060),
		.INIT_A(256'h8b7937e4a495a891a662efac6ed35dc2e45c6c240a06db491e0a4e3a56323be0),
		.INIT_B(256'h1808e9ae8e7aaf6525ea07f4fa56b46ce0a9d24e64d58c8db76d593743c832e7),
		.INIT_C(256'h858a868bdcbddd4b211f9c747cdd23e851c6c7b4f1a6241c722e6f258878d5ba),
		.INIT_D(256'hb99e271d58c19186d0b9f9575f35a361120e01f60503d848aa66c4b5423e9070),
		.INIT_E(256'h7adf7828ff5549ce20e99287221eb69ba794898e70d9bb693311b39813f838e1),
		.INIT_F(256'h3a16d6bbfc54cbb0110f772db099c341b868c64231e6dabf170d8089f8a18f8c)
	) table_0_hi (
		.RADDR({3'b0, addr_t0}),
		.RDATA({data_t0[31:16]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);

	SB_RAM40_4K #(
		.INIT_0(256'hec9a4de6b562e719567dcea9020360509154deb1d6bdff0df68dee99f884c6a5),
		.INIT_1(256'h9b5be49653f723bf45ea5ffdb36741ecfb0b8ec9b2ebef15fa8789401f9d8f45),
		.INIT_2(256'h2a3f6253ab73e293f908d13451f4685c834ff5027e416c5a4c6a3daee11c75c2),
		.INIT_3(256'hea9f7fcd4e69cd26df3d1b9b24360e092fb50a0f37a130289d5e46659552080c),
		.INIT_4(256'h13975e71dd3e527b7dceb761764da4f65bfbb4eedcb2362d342e58741d9e121b),
		.INIT_5(256'h854ab0e898d494de724b67d98d46d4beb6ed79c8e31f4060c12c0000b968a6f5),
		.INIT_6(256'h4be325ba7844a0f0fe810406e9108acf119466559ad786c5ed164fe5c52abb6b),
		.INIT_7(256'hbf6dfd0ee51a20304263af7577c163dff104704821bc3fad058a80c05dfea2f3),
		.INIT_8(256'he695322bbae7c8ac7a47fc8255f293572e3988cc35a2bee1c32f26351814814c),
		.INIT_9(256'had76161dbce2a779283c6bd3c7298cca0b833bab547e4466a37f9ed11998c0a0),
		.INIT_A(256'hf28bd33731a439a8c4a643efbd6e9f5db8e4486c0c0a92db141e744e6456db3b),
		.INIT_B(256'h101847e9f48ecaafcf25f307acfad8b449e09cd2b164018cdab76e598b43d532),
		.INIT_C(256'h0f850d8661dc96dd3e21e89ca17ccb23975173c757f138245c724a6ff0886fd5),
		.INIT_D(256'h27b93a279958179169d0aef96a5fc2a31c12f701060590d8ccaa71c47c42e090),
		.INIT_E(256'ha57a5078aaff8749c92015923c222db633a70789a970d2bb22332bb3eb13d938),
		.INIT_F(256'h2c3a6dd6a8fc7bcb1e115a7729b082c3d0b884c6d73165da1a17098059f8038f)
	) table_1_lo (
		.RADDR({3'b0, addr_t1}),
		.RDATA({data_t1[15:0]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);

	SB_RAM40_4K #(
		.INIT_0(256'h7676ababd7d7fefe2b2b676701013030c5c56f6f6b6bf2f27b7b77777c7c6363),
		.INIT_1(256'hc0c07272a4a49c9cafafa2a2d4d4adadf0f047475959fafa7d7dc9c98282caca),
		.INIT_2(256'h15153131d8d87171f1f1e5e5a5a53434ccccf7f73f3f363626269393fdfdb7b7),
		.INIT_3(256'h7575b2b22727ebebe2e28080121207079a9a050596961818c3c32323c7c70404),
		.INIT_4(256'h84842f2fe3e32929b3b3d6d63b3b5252a0a05a5a6e6e1b1b1a1a2c2c83830909),
		.INIT_5(256'hcfcf58584c4c4a4a3939bebecbcb6a6a5b5bb1b1fcfc2020eded0000d1d15353),
		.INIT_6(256'ha8a89f9f3c3c50507f7f0202f9f94545858533334d4d4343fbfbaaaaefefd0d0),
		.INIT_7(256'hd2d2f3f3ffff10102121dadab6b6bcbcf5f538389d9d92928f8f4040a3a35151),
		.INIT_8(256'h737319195d5d64643d3d7e7ea7a7c4c41717444497975f5fecec13130c0ccdcd),
		.INIT_9(256'hdbdb0b0b5e5edede1414b8b8eeee4646888890902a2a2222dcdc4f4f81816060),
		.INIT_A(256'h7979e4e4959591916262acacd3d3c2c25c5c2424060649490a0a3a3a3232e0e0),
		.INIT_B(256'h0808aeae7a7a6565eaeaf4f456566c6ca9a94e4ed5d58d8d6d6d3737c8c8e7e7),
		.INIT_C(256'h8a8a8b8bbdbd4b4b1f1f7474dddde8e8c6c6b4b4a6a61c1c2e2e25257878baba),
		.INIT_D(256'h9e9e1d1dc1c18686b9b95757353561610e0ef6f6030348486666b5b53e3e7070),
		.INIT_E(256'hdfdf28285555cecee9e987871e1e9b9b94948e8ed9d9696911119898f8f8e1e1),
		.INIT_F(256'h1616bbbb5454b0b00f0f2d2d9999414168684242e6e6bfbf0d0d8989a1a18c8c)
	) table_1_hi (
		.RADDR({3'b0, addr_t1}),
		.RDATA({data_t1[31:16]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);

	SB_RAM40_4K #(
		.INIT_0(256'h9a76e6ab62d719fe7d2ba9670301503054c5b16fbd6b0df28d7b9977847ca563),
		.INIT_1(256'h5bc09672f7a4bf9ceaaffda267d4ecad0bf0c947eb5915fa877d40c99d8245ca),
		.INIT_2(256'h3f15533173d8937108f134e5f4a55c344fcc02f7413f5a366a26ae931cfdc2b7),
		.INIT_3(256'h9f75cdb2692726eb3de29b8036120907b59a0f05a19628185ec3652352c70c04),
		.INIT_4(256'h9784712f3ee37b29ceb361d64d3bf652fba0ee5ab26e2d1b2e1a742c9e831b09),
		.INIT_5(256'h4acfe858d44cde4a4b39d9be46cbbe6aed5bc8b11ffc60202ced000068d1f553),
		.INIT_6(256'he3a8ba9f443cf050817f060210f9cf4594855533d74dc54316fbe5aa2aef6bd0),
		.INIT_7(256'h6dd20ef31aff3010632175dac1b6dfbc04f54838bc9dad928a8fc040fea3f351),
		.INIT_8(256'h95732b19e75dac64473d827ef2a757c43917cc44a297e15f2fec3513140c4ccd),
		.INIT_9(256'h76db1d0be25e79de3c14d3b829eeca468388ab907e2a66227fdcd14f9881a060),
		.INIT_A(256'h8b7937e4a495a891a662efac6ed35dc2e45c6c240a06db491e0a4e3a56323be0),
		.INIT_B(256'h1808e9ae8e7aaf6525ea07f4fa56b46ce0a9d24e64d58c8db76d593743c832e7),
		.INIT_C(256'h858a868bdcbddd4b211f9c747cdd23e851c6c7b4f1a6241c722e6f258878d5ba),
		.INIT_D(256'hb99e271d58c19186d0b9f9575f35a361120e01f60503d848aa66c4b5423e9070),
		.INIT_E(256'h7adf7828ff5549ce20e99287221eb69ba794898e70d9bb693311b39813f838e1),
		.INIT_F(256'h3a16d6bbfc54cbb0110f772db099c341b868c64231e6dabf170d8089f8a18f8c)
	) table_2_lo (
		.RADDR({3'b0, addr_t2}),
		.RDATA({data_t2[15:0]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);

	SB_RAM40_4K #(
		.INIT_0(256'h76ecab4dd7b5fee72b5667ce01023060c5916fde6bd6f2ff7bf677ee7cf863c6),
		.INIT_1(256'hc09b72e4a4539c23af45a25fd4b3ad41f0fb478e59b2faef7dfac989821fca8f),
		.INIT_2(256'h152a3162d8ab71e2f1f9e5d1a5513468cc83f7f53f7e366c264c933dfde1b775),
		.INIT_3(256'h75eab27f274eebcde2df801b1224070e9a2f050a96371830c39d2346c7950408),
		.INIT_4(256'h84132f5ee3dd2952b37dd6b73b7652a4a05b5ab46edc1b361a342c58831d0912),
		.INIT_5(256'hcf8558b04c984a943972be67cb8d6ad45bb6b179fce32040edc10000d1b953a6),
		.INIT_6(256'ha84b9f253c7850a07ffe0204f9e9458a851133664d9a4386fbedaa4fefc5d0bb),
		.INIT_7(256'hd2bff3fdffe510202142daafb677bc63f5f138709d21923f8f054080a35d51a2),
		.INIT_8(256'h73e619325dba64c83d7a7efca755c493172e448897355fbeecc313260c18cd81),
		.INIT_9(256'hdbad0b165ebcdea71428b86beec7468c880b903b2a542244dca34f9e811960c0),
		.INIT_A(256'h79f2e4d39531913962c4ac43d3bdc29f5cb82448060c49920a143a743264e0db),
		.INIT_B(256'h0810ae477af465caeacff4f356ac6cd8a9494e9cd5b18d016dda376ec88be7d5),
		.INIT_C(256'h8a0f8b0dbd614b961f3e74e8dda1e8cbc697b473a6571c382e5c254a78f0ba6f),
		.INIT_D(256'h9e271d3ac1998617b96957ae356a61c20e1cf6f70306489066ccb5713e7c70e0),
		.INIT_E(256'hdfa5285055aace87e9c987151e3c9b2d94338e07d9a969d21122982bf8ebe1d9),
		.INIT_F(256'h162cbb6d54a8b07b0f1e2d5a9929418268d04284e6d7bf650d1a8909a1598c03)
	) table_2_hi (
		.RADDR({3'b0, addr_t2}),
		.RDATA({data_t2[31:16]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);

	SB_RAM40_4K #(
		.INIT_0(256'h7676ababd7d7fefe2b2b676701013030c5c56f6f6b6bf2f27b7b77777c7c6363),
		.INIT_1(256'hc0c07272a4a49c9cafafa2a2d4d4adadf0f047475959fafa7d7dc9c98282caca),
		.INIT_2(256'h15153131d8d87171f1f1e5e5a5a53434ccccf7f73f3f363626269393fdfdb7b7),
		.INIT_3(256'h7575b2b22727ebebe2e28080121207079a9a050596961818c3c32323c7c70404),
		.INIT_4(256'h84842f2fe3e32929b3b3d6d63b3b5252a0a05a5a6e6e1b1b1a1a2c2c83830909),
		.INIT_5(256'hcfcf58584c4c4a4a3939bebecbcb6a6a5b5bb1b1fcfc2020eded0000d1d15353),
		.INIT_6(256'ha8a89f9f3c3c50507f7f0202f9f94545858533334d4d4343fbfbaaaaefefd0d0),
		.INIT_7(256'hd2d2f3f3ffff10102121dadab6b6bcbcf5f538389d9d92928f8f4040a3a35151),
		.INIT_8(256'h737319195d5d64643d3d7e7ea7a7c4c41717444497975f5fecec13130c0ccdcd),
		.INIT_9(256'hdbdb0b0b5e5edede1414b8b8eeee4646888890902a2a2222dcdc4f4f81816060),
		.INIT_A(256'h7979e4e4959591916262acacd3d3c2c25c5c2424060649490a0a3a3a3232e0e0),
		.INIT_B(256'h0808aeae7a7a6565eaeaf4f456566c6ca9a94e4ed5d58d8d6d6d3737c8c8e7e7),
		.INIT_C(256'h8a8a8b8bbdbd4b4b1f1f7474dddde8e8c6c6b4b4a6a61c1c2e2e25257878baba),
		.INIT_D(256'h9e9e1d1dc1c18686b9b95757353561610e0ef6f6030348486666b5b53e3e7070),
		.INIT_E(256'hdfdf28285555cecee9e987871e1e9b9b94948e8ed9d9696911119898f8f8e1e1),
		.INIT_F(256'h1616bbbb5454b0b00f0f2d2d9999414168684242e6e6bfbf0d0d8989a1a18c8c)
	) table_3_lo (
		.RADDR({3'b0, addr_t3}),
		.RDATA({data_t3[15:0]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);

	SB_RAM40_4K #(
		.INIT_0(256'hec9a4de6b562e719567dcea9020360509154deb1d6bdff0df68dee99f884c6a5),
		.INIT_1(256'h9b5be49653f723bf45ea5ffdb36741ecfb0b8ec9b2ebef15fa8789401f9d8f45),
		.INIT_2(256'h2a3f6253ab73e293f908d13451f4685c834ff5027e416c5a4c6a3daee11c75c2),
		.INIT_3(256'hea9f7fcd4e69cd26df3d1b9b24360e092fb50a0f37a130289d5e46659552080c),
		.INIT_4(256'h13975e71dd3e527b7dceb761764da4f65bfbb4eedcb2362d342e58741d9e121b),
		.INIT_5(256'h854ab0e898d494de724b67d98d46d4beb6ed79c8e31f4060c12c0000b968a6f5),
		.INIT_6(256'h4be325ba7844a0f0fe810406e9108acf119466559ad786c5ed164fe5c52abb6b),
		.INIT_7(256'hbf6dfd0ee51a20304263af7577c163dff104704821bc3fad058a80c05dfea2f3),
		.INIT_8(256'he695322bbae7c8ac7a47fc8255f293572e3988cc35a2bee1c32f26351814814c),
		.INIT_9(256'had76161dbce2a779283c6bd3c7298cca0b833bab547e4466a37f9ed11998c0a0),
		.INIT_A(256'hf28bd33731a439a8c4a643efbd6e9f5db8e4486c0c0a92db141e744e6456db3b),
		.INIT_B(256'h101847e9f48ecaafcf25f307acfad8b449e09cd2b164018cdab76e598b43d532),
		.INIT_C(256'h0f850d8661dc96dd3e21e89ca17ccb23975173c757f138245c724a6ff0886fd5),
		.INIT_D(256'h27b93a279958179169d0aef96a5fc2a31c12f701060590d8ccaa71c47c42e090),
		.INIT_E(256'ha57a5078aaff8749c92015923c222db633a70789a970d2bb22332bb3eb13d938),
		.INIT_F(256'h2c3a6dd6a8fc7bcb1e115a7729b082c3d0b884c6d73165da1a17098059f8038f)
	) table_3_hi (
		.RADDR({3'b0, addr_t3}),
		.RDATA({data_t3[31:16]}),
		.RCLK (clk),
		.RE   (1'b1),
		.RCLKE(1'b1),
		.WADDR(11'b0),
		.WCLK (1'b0),
		.WCLKE(1'b0),
		.WE   (1'b0),
		.WDATA(16'b0),
		.MASK (16'b0)
	);
endmodule
