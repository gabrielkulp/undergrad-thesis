# this script takes a nice data format and prints
# it in a way that's easy to paste into the Verilog
# spellchecker: disable

rev_bytes = lambda s: "".join([s[2*i:(2*i)+2] for i in range(len(s)-1, -1, -1)])

key_schedule = [
	"000102030405060708090a0b0c0d0e0f",
	"d6aa74fdd2af72fadaa678f1d6ab76fe",
	"b692cf0b643dbdf1be9bc5006830b3fe",
	"b6ff744ed2c2c9bf6c590cbf0469bf41",
	"47f7f7bc95353e03f96c32bcfd058dfd",
	"3caaa3e8a99f9deb50f3af57adf622aa",
	"5e390f7df7a69296a7553dc10aa31f6b",
	"14f9701ae35fe28c440adf4d4ea9c026",
	"47438735a41c65b9e016baf4aebf7ad2",
	"549932d1f08557681093ed9cbe2c974e",
	"13111d7fe3944a17f307a78b4d2b30c5"
	]

rev = lambda l: [l[i] for i in range(len(l)-1,-1,-1)]
lo_cols = []
lo_code = []
hi_cols = []
hi_code = []
for key in key_schedule:
	hi_cols.append("".join([rev_bytes(key[8*i:(8*i)+8])[:4] for i in range(3,-1,-1)]))
	lo_cols.append("".join([rev_bytes(key[8*i:(8*i)+8])[4:] for i in range(3,-1,-1)]))

lo_code.append("    .INIT_0(256'h" + "".join(rev(lo_cols[0:4])) + ")")
lo_code.append("    .INIT_1(256'h" + "".join(rev(lo_cols[4:8])) + ")")
lo_code.append("    .INIT_2(256'h" + "".join(["00"]*8)+ "".join(rev(lo_cols[8:])) + ")")

hi_code.append("    .INIT_0(256'h" + "".join(rev(hi_cols[0:4])) + ")")
hi_code.append("    .INIT_1(256'h" + "".join(rev(hi_cols[4:8])) + ")")
hi_code.append("    .INIT_2(256'h" + "".join(["00"]*8)+ "".join(rev(hi_cols[8:])) + ")")

for (name, pins, code) in [("lo", "15:0", lo_code), ("hi", "31:16", hi_code)]:
	print("SB_RAM40_4K #(")
	print(",\n".join(code))
	print(f") keys_{name} (")
	print(f"    .RADDR({{5'b0, round, column}}),")
	print(f"    .RDATA({{key[{pins}]}}),")
	print('''    .RCLK (clk),
    .RE   (1'b1),
    .RCLKE(1'b1),
    .WADDR(11'b0),
    .WCLK (1'b0),
    .WCLKE(1'b0),
    .WE   (1'b0),
    .WDATA(16'b0),
    .MASK (16'b0)
);\n''')


table_0 = [
	"c66363a5", "f87c7c84", "ee777799", "f67b7b8d",
	"fff2f20d", "d66b6bbd", "de6f6fb1", "91c5c554",
	"60303050", "02010103", "ce6767a9", "562b2b7d",
	"e7fefe19", "b5d7d762", "4dababe6", "ec76769a",
	"8fcaca45", "1f82829d", "89c9c940", "fa7d7d87",
	"effafa15", "b25959eb", "8e4747c9", "fbf0f00b",
	"41adadec", "b3d4d467", "5fa2a2fd", "45afafea",
	"239c9cbf", "53a4a4f7", "e4727296", "9bc0c05b",
	"75b7b7c2", "e1fdfd1c", "3d9393ae", "4c26266a",
	"6c36365a", "7e3f3f41", "f5f7f702", "83cccc4f",
	"6834345c", "51a5a5f4", "d1e5e534", "f9f1f108",
	"e2717193", "abd8d873", "62313153", "2a15153f",
	"0804040c", "95c7c752", "46232365", "9dc3c35e",
	"30181828", "379696a1", "0a05050f", "2f9a9ab5",
	"0e070709", "24121236", "1b80809b", "dfe2e23d",
	"cdebeb26", "4e272769", "7fb2b2cd", "ea75759f",
	"1209091b", "1d83839e", "582c2c74", "341a1a2e",
	"361b1b2d", "dc6e6eb2", "b45a5aee", "5ba0a0fb",
	"a45252f6", "763b3b4d", "b7d6d661", "7db3b3ce",
	"5229297b", "dde3e33e", "5e2f2f71", "13848497",
	"a65353f5", "b9d1d168", "00000000", "c1eded2c",
	"40202060", "e3fcfc1f", "79b1b1c8", "b65b5bed",
	"d46a6abe", "8dcbcb46", "67bebed9", "7239394b",
	"944a4ade", "984c4cd4", "b05858e8", "85cfcf4a",
	"bbd0d06b", "c5efef2a", "4faaaae5", "edfbfb16",
	"864343c5", "9a4d4dd7", "66333355", "11858594",
	"8a4545cf", "e9f9f910", "04020206", "fe7f7f81",
	"a05050f0", "783c3c44", "259f9fba", "4ba8a8e3",
	"a25151f3", "5da3a3fe", "804040c0", "058f8f8a",
	"3f9292ad", "219d9dbc", "70383848", "f1f5f504",
	"63bcbcdf", "77b6b6c1", "afdada75", "42212163",
	"20101030", "e5ffff1a", "fdf3f30e", "bfd2d26d",
	"81cdcd4c", "180c0c14", "26131335", "c3ecec2f",
	"be5f5fe1", "359797a2", "884444cc", "2e171739",
	"93c4c457", "55a7a7f2", "fc7e7e82", "7a3d3d47",
	"c86464ac", "ba5d5de7", "3219192b", "e6737395",
	"c06060a0", "19818198", "9e4f4fd1", "a3dcdc7f",
	"44222266", "542a2a7e", "3b9090ab", "0b888883",
	"8c4646ca", "c7eeee29", "6bb8b8d3", "2814143c",
	"a7dede79", "bc5e5ee2", "160b0b1d", "addbdb76",
	"dbe0e03b", "64323256", "743a3a4e", "140a0a1e",
	"924949db", "0c06060a", "4824246c", "b85c5ce4",
	"9fc2c25d", "bdd3d36e", "43acacef", "c46262a6",
	"399191a8", "319595a4", "d3e4e437", "f279798b",
	"d5e7e732", "8bc8c843", "6e373759", "da6d6db7",
	"018d8d8c", "b1d5d564", "9c4e4ed2", "49a9a9e0",
	"d86c6cb4", "ac5656fa", "f3f4f407", "cfeaea25",
	"ca6565af", "f47a7a8e", "47aeaee9", "10080818",
	"6fbabad5", "f0787888", "4a25256f", "5c2e2e72",
	"381c1c24", "57a6a6f1", "73b4b4c7", "97c6c651",
	"cbe8e823", "a1dddd7c", "e874749c", "3e1f1f21",
	"964b4bdd", "61bdbddc", "0d8b8b86", "0f8a8a85",
	"e0707090", "7c3e3e42", "71b5b5c4", "cc6666aa",
	"904848d8", "06030305", "f7f6f601", "1c0e0e12",
	"c26161a3", "6a35355f", "ae5757f9", "69b9b9d0",
	"17868691", "99c1c158", "3a1d1d27", "279e9eb9",
	"d9e1e138", "ebf8f813", "2b9898b3", "22111133",
	"d26969bb", "a9d9d970", "078e8e89", "339494a7",
	"2d9b9bb6", "3c1e1e22", "15878792", "c9e9e920",
	"87cece49", "aa5555ff", "50282878", "a5dfdf7a",
	"038c8c8f", "59a1a1f8", "09898980", "1a0d0d17",
	"65bfbfda", "d7e6e631", "844242c6", "d06868b8",
	"824141c3", "299999b0", "5a2d2d77", "1e0f0f11",
	"7bb0b0cb", "a85454fc", "6dbbbbd6", "2c16163a"
]

table_1 = [
	"a5c66363", "84f87c7c", "99ee7777", "8df67b7b",
	"0dfff2f2", "bdd66b6b", "b1de6f6f", "5491c5c5",
	"50603030", "03020101", "a9ce6767", "7d562b2b",
	"19e7fefe", "62b5d7d7", "e64dabab", "9aec7676",
	"458fcaca", "9d1f8282", "4089c9c9", "87fa7d7d",
	"15effafa", "ebb25959", "c98e4747", "0bfbf0f0",
	"ec41adad", "67b3d4d4", "fd5fa2a2", "ea45afaf",
	"bf239c9c", "f753a4a4", "96e47272", "5b9bc0c0",
	"c275b7b7", "1ce1fdfd", "ae3d9393", "6a4c2626",
	"5a6c3636", "417e3f3f", "02f5f7f7", "4f83cccc",
	"5c683434", "f451a5a5", "34d1e5e5", "08f9f1f1",
	"93e27171", "73abd8d8", "53623131", "3f2a1515",
	"0c080404", "5295c7c7", "65462323", "5e9dc3c3",
	"28301818", "a1379696", "0f0a0505", "b52f9a9a",
	"090e0707", "36241212", "9b1b8080", "3ddfe2e2",
	"26cdebeb", "694e2727", "cd7fb2b2", "9fea7575",
	"1b120909", "9e1d8383", "74582c2c", "2e341a1a",
	"2d361b1b", "b2dc6e6e", "eeb45a5a", "fb5ba0a0",
	"f6a45252", "4d763b3b", "61b7d6d6", "ce7db3b3",
	"7b522929", "3edde3e3", "715e2f2f", "97138484",
	"f5a65353", "68b9d1d1", "00000000", "2cc1eded",
	"60402020", "1fe3fcfc", "c879b1b1", "edb65b5b",
	"bed46a6a", "468dcbcb", "d967bebe", "4b723939",
	"de944a4a", "d4984c4c", "e8b05858", "4a85cfcf",
	"6bbbd0d0", "2ac5efef", "e54faaaa", "16edfbfb",
	"c5864343", "d79a4d4d", "55663333", "94118585",
	"cf8a4545", "10e9f9f9", "06040202", "81fe7f7f",
	"f0a05050", "44783c3c", "ba259f9f", "e34ba8a8",
	"f3a25151", "fe5da3a3", "c0804040", "8a058f8f",
	"ad3f9292", "bc219d9d", "48703838", "04f1f5f5",
	"df63bcbc", "c177b6b6", "75afdada", "63422121",
	"30201010", "1ae5ffff", "0efdf3f3", "6dbfd2d2",
	"4c81cdcd", "14180c0c", "35261313", "2fc3ecec",
	"e1be5f5f", "a2359797", "cc884444", "392e1717",
	"5793c4c4", "f255a7a7", "82fc7e7e", "477a3d3d",
	"acc86464", "e7ba5d5d", "2b321919", "95e67373",
	"a0c06060", "98198181", "d19e4f4f", "7fa3dcdc",
	"66442222", "7e542a2a", "ab3b9090", "830b8888",
	"ca8c4646", "29c7eeee", "d36bb8b8", "3c281414",
	"79a7dede", "e2bc5e5e", "1d160b0b", "76addbdb",
	"3bdbe0e0", "56643232", "4e743a3a", "1e140a0a",
	"db924949", "0a0c0606", "6c482424", "e4b85c5c",
	"5d9fc2c2", "6ebdd3d3", "ef43acac", "a6c46262",
	"a8399191", "a4319595", "37d3e4e4", "8bf27979",
	"32d5e7e7", "438bc8c8", "596e3737", "b7da6d6d",
	"8c018d8d", "64b1d5d5", "d29c4e4e", "e049a9a9",
	"b4d86c6c", "faac5656", "07f3f4f4", "25cfeaea",
	"afca6565", "8ef47a7a", "e947aeae", "18100808",
	"d56fbaba", "88f07878", "6f4a2525", "725c2e2e",
	"24381c1c", "f157a6a6", "c773b4b4", "5197c6c6",
	"23cbe8e8", "7ca1dddd", "9ce87474", "213e1f1f",
	"dd964b4b", "dc61bdbd", "860d8b8b", "850f8a8a",
	"90e07070", "427c3e3e", "c471b5b5", "aacc6666",
	"d8904848", "05060303", "01f7f6f6", "121c0e0e",
	"a3c26161", "5f6a3535", "f9ae5757", "d069b9b9",
	"91178686", "5899c1c1", "273a1d1d", "b9279e9e",
	"38d9e1e1", "13ebf8f8", "b32b9898", "33221111",
	"bbd26969", "70a9d9d9", "89078e8e", "a7339494",
	"b62d9b9b", "223c1e1e", "92158787", "20c9e9e9",
	"4987cece", "ffaa5555", "78502828", "7aa5dfdf",
	"8f038c8c", "f859a1a1", "80098989", "171a0d0d",
	"da65bfbf", "31d7e6e6", "c6844242", "b8d06868",
	"c3824141", "b0299999", "775a2d2d", "111e0f0f",
	"cb7bb0b0", "fca85454", "d66dbbbb", "3a2c1616"
]

table_2 = [
	"63a5c663", "7c84f87c", "7799ee77", "7b8df67b",
	"f20dfff2", "6bbdd66b", "6fb1de6f", "c55491c5",
	"30506030", "01030201", "67a9ce67", "2b7d562b",
	"fe19e7fe", "d762b5d7", "abe64dab", "769aec76",
	"ca458fca", "829d1f82", "c94089c9", "7d87fa7d",
	"fa15effa", "59ebb259", "47c98e47", "f00bfbf0",
	"adec41ad", "d467b3d4", "a2fd5fa2", "afea45af",
	"9cbf239c", "a4f753a4", "7296e472", "c05b9bc0",
	"b7c275b7", "fd1ce1fd", "93ae3d93", "266a4c26",
	"365a6c36", "3f417e3f", "f702f5f7", "cc4f83cc",
	"345c6834", "a5f451a5", "e534d1e5", "f108f9f1",
	"7193e271", "d873abd8", "31536231", "153f2a15",
	"040c0804", "c75295c7", "23654623", "c35e9dc3",
	"18283018", "96a13796", "050f0a05", "9ab52f9a",
	"07090e07", "12362412", "809b1b80", "e23ddfe2",
	"eb26cdeb", "27694e27", "b2cd7fb2", "759fea75",
	"091b1209", "839e1d83", "2c74582c", "1a2e341a",
	"1b2d361b", "6eb2dc6e", "5aeeb45a", "a0fb5ba0",
	"52f6a452", "3b4d763b", "d661b7d6", "b3ce7db3",
	"297b5229", "e33edde3", "2f715e2f", "84971384",
	"53f5a653", "d168b9d1", "00000000", "ed2cc1ed",
	"20604020", "fc1fe3fc", "b1c879b1", "5bedb65b",
	"6abed46a", "cb468dcb", "bed967be", "394b7239",
	"4ade944a", "4cd4984c", "58e8b058", "cf4a85cf",
	"d06bbbd0", "ef2ac5ef", "aae54faa", "fb16edfb",
	"43c58643", "4dd79a4d", "33556633", "85941185",
	"45cf8a45", "f910e9f9", "02060402", "7f81fe7f",
	"50f0a050", "3c44783c", "9fba259f", "a8e34ba8",
	"51f3a251", "a3fe5da3", "40c08040", "8f8a058f",
	"92ad3f92", "9dbc219d", "38487038", "f504f1f5",
	"bcdf63bc", "b6c177b6", "da75afda", "21634221",
	"10302010", "ff1ae5ff", "f30efdf3", "d26dbfd2",
	"cd4c81cd", "0c14180c", "13352613", "ec2fc3ec",
	"5fe1be5f", "97a23597", "44cc8844", "17392e17",
	"c45793c4", "a7f255a7", "7e82fc7e", "3d477a3d",
	"64acc864", "5de7ba5d", "192b3219", "7395e673",
	"60a0c060", "81981981", "4fd19e4f", "dc7fa3dc",
	"22664422", "2a7e542a", "90ab3b90", "88830b88",
	"46ca8c46", "ee29c7ee", "b8d36bb8", "143c2814",
	"de79a7de", "5ee2bc5e", "0b1d160b", "db76addb",
	"e03bdbe0", "32566432", "3a4e743a", "0a1e140a",
	"49db9249", "060a0c06", "246c4824", "5ce4b85c",
	"c25d9fc2", "d36ebdd3", "acef43ac", "62a6c462",
	"91a83991", "95a43195", "e437d3e4", "798bf279",
	"e732d5e7", "c8438bc8", "37596e37", "6db7da6d",
	"8d8c018d", "d564b1d5", "4ed29c4e", "a9e049a9",
	"6cb4d86c", "56faac56", "f407f3f4", "ea25cfea",
	"65afca65", "7a8ef47a", "aee947ae", "08181008",
	"bad56fba", "7888f078", "256f4a25", "2e725c2e",
	"1c24381c", "a6f157a6", "b4c773b4", "c65197c6",
	"e823cbe8", "dd7ca1dd", "749ce874", "1f213e1f",
	"4bdd964b", "bddc61bd", "8b860d8b", "8a850f8a",
	"7090e070", "3e427c3e", "b5c471b5", "66aacc66",
	"48d89048", "03050603", "f601f7f6", "0e121c0e",
	"61a3c261", "355f6a35", "57f9ae57", "b9d069b9",
	"86911786", "c15899c1", "1d273a1d", "9eb9279e",
	"e138d9e1", "f813ebf8", "98b32b98", "11332211",
	"69bbd269", "d970a9d9", "8e89078e", "94a73394",
	"9bb62d9b", "1e223c1e", "87921587", "e920c9e9",
	"ce4987ce", "55ffaa55", "28785028", "df7aa5df",
	"8c8f038c", "a1f859a1", "89800989", "0d171a0d",
	"bfda65bf", "e631d7e6", "42c68442", "68b8d068",
	"41c38241", "99b02999", "2d775a2d", "0f111e0f",
	"b0cb7bb0", "54fca854", "bbd66dbb", "163a2c16"
]

table_3 = [
	"6363a5c6", "7c7c84f8", "777799ee", "7b7b8df6",
	"f2f20dff", "6b6bbdd6", "6f6fb1de", "c5c55491",
	"30305060", "01010302", "6767a9ce", "2b2b7d56",
	"fefe19e7", "d7d762b5", "ababe64d", "76769aec",
	"caca458f", "82829d1f", "c9c94089", "7d7d87fa",
	"fafa15ef", "5959ebb2", "4747c98e", "f0f00bfb",
	"adadec41", "d4d467b3", "a2a2fd5f", "afafea45",
	"9c9cbf23", "a4a4f753", "727296e4", "c0c05b9b",
	"b7b7c275", "fdfd1ce1", "9393ae3d", "26266a4c",
	"36365a6c", "3f3f417e", "f7f702f5", "cccc4f83",
	"34345c68", "a5a5f451", "e5e534d1", "f1f108f9",
	"717193e2", "d8d873ab", "31315362", "15153f2a",
	"04040c08", "c7c75295", "23236546", "c3c35e9d",
	"18182830", "9696a137", "05050f0a", "9a9ab52f",
	"0707090e", "12123624", "80809b1b", "e2e23ddf",
	"ebeb26cd", "2727694e", "b2b2cd7f", "75759fea",
	"09091b12", "83839e1d", "2c2c7458", "1a1a2e34",
	"1b1b2d36", "6e6eb2dc", "5a5aeeb4", "a0a0fb5b",
	"5252f6a4", "3b3b4d76", "d6d661b7", "b3b3ce7d",
	"29297b52", "e3e33edd", "2f2f715e", "84849713",
	"5353f5a6", "d1d168b9", "00000000", "eded2cc1",
	"20206040", "fcfc1fe3", "b1b1c879", "5b5bedb6",
	"6a6abed4", "cbcb468d", "bebed967", "39394b72",
	"4a4ade94", "4c4cd498", "5858e8b0", "cfcf4a85",
	"d0d06bbb", "efef2ac5", "aaaae54f", "fbfb16ed",
	"4343c586", "4d4dd79a", "33335566", "85859411",
	"4545cf8a", "f9f910e9", "02020604", "7f7f81fe",
	"5050f0a0", "3c3c4478", "9f9fba25", "a8a8e34b",
	"5151f3a2", "a3a3fe5d", "4040c080", "8f8f8a05",
	"9292ad3f", "9d9dbc21", "38384870", "f5f504f1",
	"bcbcdf63", "b6b6c177", "dada75af", "21216342",
	"10103020", "ffff1ae5", "f3f30efd", "d2d26dbf",
	"cdcd4c81", "0c0c1418", "13133526", "ecec2fc3",
	"5f5fe1be", "9797a235", "4444cc88", "1717392e",
	"c4c45793", "a7a7f255", "7e7e82fc", "3d3d477a",
	"6464acc8", "5d5de7ba", "19192b32", "737395e6",
	"6060a0c0", "81819819", "4f4fd19e", "dcdc7fa3",
	"22226644", "2a2a7e54", "9090ab3b", "8888830b",
	"4646ca8c", "eeee29c7", "b8b8d36b", "14143c28",
	"dede79a7", "5e5ee2bc", "0b0b1d16", "dbdb76ad",
	"e0e03bdb", "32325664", "3a3a4e74", "0a0a1e14",
	"4949db92", "06060a0c", "24246c48", "5c5ce4b8",
	"c2c25d9f", "d3d36ebd", "acacef43", "6262a6c4",
	"9191a839", "9595a431", "e4e437d3", "79798bf2",
	"e7e732d5", "c8c8438b", "3737596e", "6d6db7da",
	"8d8d8c01", "d5d564b1", "4e4ed29c", "a9a9e049",
	"6c6cb4d8", "5656faac", "f4f407f3", "eaea25cf",
	"6565afca", "7a7a8ef4", "aeaee947", "08081810",
	"babad56f", "787888f0", "25256f4a", "2e2e725c",
	"1c1c2438", "a6a6f157", "b4b4c773", "c6c65197",
	"e8e823cb", "dddd7ca1", "74749ce8", "1f1f213e",
	"4b4bdd96", "bdbddc61", "8b8b860d", "8a8a850f",
	"707090e0", "3e3e427c", "b5b5c471", "6666aacc",
	"4848d890", "03030506", "f6f601f7", "0e0e121c",
	"6161a3c2", "35355f6a", "5757f9ae", "b9b9d069",
	"86869117", "c1c15899", "1d1d273a", "9e9eb927",
	"e1e138d9", "f8f813eb", "9898b32b", "11113322",
	"6969bbd2", "d9d970a9", "8e8e8907", "9494a733",
	"9b9bb62d", "1e1e223c", "87879215", "e9e920c9",
	"cece4987", "5555ffaa", "28287850", "dfdf7aa5",
	"8c8c8f03", "a1a1f859", "89898009", "0d0d171a",
	"bfbfda65", "e6e631d7", "4242c684", "6868b8d0",
	"4141c382", "9999b029", "2d2d775a", "0f0f111e",
	"b0b0cb7b", "5454fca8", "bbbbd66d", "16163a2c"
]

tables = [table_0, table_1, table_2, table_3]

for t in range(len(tables)):
	table = tables[t]

	hi_code = []
	lo_code = []
	idx = 0
	for row in [table[16*i:(16*i)+16] for i in range(16)]:
		hi_bytes = [rev_bytes(row[j])[:4] for j in range(15,-1,-1)]
		lo_bytes = [rev_bytes(row[j])[4:] for j in range(15,-1,-1)]
		hi_code.append(f"    .INIT_{idx%16:X}(256'h{''.join(hi_bytes)})")
		lo_code.append(f"    .INIT_{idx%16:X}(256'h{''.join(lo_bytes)})")
		idx += 1
	
	for (name, pins, code) in [("lo", "15:0", lo_code), ("hi", "31:16", hi_code)]:
		print("SB_RAM40_4K #(")
		print(",\n".join(code))
		print(f") table_{t}_{name} (")
		print(f"    .RADDR({{3'b0, addr_t{t}}}),")
		print(f"    .RDATA({{data_t{t}[{pins}]}}),")
		print('''    .RCLK (clk),
    .RE   (1'b1),
    .RCLKE(1'b1),
    .WADDR(11'b0),
    .WCLK (1'b0),
    .WCLKE(1'b0),
    .WE   (1'b0),
    .WDATA(16'b0),
    .MASK (16'b0)
);\n''')
