# auth_computer_architecture


cpu minor

cpu-freq 4GHz
num-cores 1
mem-type DDR3_1600_8x8
mem-channels 2
mem-ranks None
mem-size 2GB

"memories": [
            "system.mem_ctrls0.dram",
            "system.mem_ctrls1.dram"
        ],


        "mem_ranges": [
            "0:2147483648"
        ],

2147483648 = 1024^3 * 2
2 billion bytes (Giga bytes)


            "cpus": [
                {
                    "type": "MinorCPU",



TimingSimple: Πολύ απλός cpu. δεν έχει καν pipeline

minorcpu: απλός in-order επεξεργαστής
