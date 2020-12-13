import os, sys
import itertools
import pprint, json, pickle, time, datetime


pp = pprint.PrettyPrinter(indent=4, width=600)

benchmarks = {
    "specbzip": """-c spec_cpu2006/401.bzip2/src/specbzip -o "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000""",
    "specmcf": """-c spec_cpu2006/429.mcf/src/specmcf -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000""",
    "spechmmer": """-c spec_cpu2006/456.hmmer/src/spechmmer -o "--fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000""",
    "specsjeng": """-c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000""",
    "speclibm": """-c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000"""
}

def generate_cmd(bench, directory_ending = '', l1d_size=64, l1i_size=32, l2_size=2048, l1i_assoc=2, l1d_assoc=2, l2_assoc=8, cacheline_size=64):

    cpu_configs = lambda: f"""--cpu-type=MinorCPU --caches --l2cache --l1d_size={l1d_size}kB --l1i_size={l1i_size}kB --l2_size={l2_size}kB --l1i_assoc={l1i_assoc} --l1d_assoc={l1d_assoc} --l2_assoc={l2_assoc} --cacheline_size={cacheline_size} --cpu-clock=1GHz"""
    cmd_template = lambda bench, cpu_configs, bench_configs: f"""./build/ARM/gem5.opt -d spec_results/{bench}/{directory_ending} configs/example/se.py {cpu_configs} {bench_configs}"""

    cmd = cmd_template(bench, cpu_configs(), benchmarks[bench])
    return cmd

def generate_cmds(bench, test_type, data, directory_endings = []):
    print("List of cmds: ")
    pp.pprint(data)
    if test_type == "l1i":
        return [generate_cmd(bench, f"{bench}_l1i_{directory_endings[i].lower().replace(' ', '_').replace(',', '')}", l1i_size=pair[0], l1i_assoc=pair[1]) for i, pair in enumerate(data)]
    elif test_type == "l1d":
        return [generate_cmd(bench, f"{bench}_l1d_{directory_endings[i].lower().replace(' ', '_').replace(',', '')}", l1d_size=pair[0], l1d_assoc=pair[1]) for i, pair in enumerate(data)]
    elif test_type == "l2":
        return [generate_cmd(bench, f"{bench}_l2_{directory_endings[i].lower().replace(' ', '_').replace(',', '')}", l2_size=pair[0], l2_assoc=pair[1]) for i, pair in enumerate(data)]
    elif test_type == "cache_line":
        return [generate_cmd(bench, f"{bench}_cache_line_{directory_endings[i].lower().replace(' ', '_')}", cacheline_size=size) for i, size in enumerate(data)]
    else:
        print("UNKOWN test type!")

    

L1i_sizes = [64, 128]
L1d_sizes = [128, 256]
l1i_assocs = [2, 4]
l1d_assocs = [2, 4]

L2_sizes = [4096, 2048, 1024, 512]
l2_assocs = [4, 2]

cacheline_sizes = [64, 128, 256]

#prototype benchmarks
grand_total_tests = 0
final_tests = {}
for bench in benchmarks:
    total = 0
    print(f"\nTests for bench {bench}:")

    final_tests[bench] = {}
    final_tests[bench]["l1i"] = {}
    final_tests[bench]["l1d"] = {}
    final_tests[bench]["l2"] = {}
    final_tests[bench]["cache_line"] = {}
    final_tests[bench]["l1i"]["cmds"] = []
    final_tests[bench]["l1d"]["cmds"] = []
    final_tests[bench]["l2"]["cmds"] = []
    final_tests[bench]["cache_line"]["cmds"] = []


    L1i_tests = list(itertools.product(L1i_sizes, l1i_assocs))
    final_tests[bench]["l1i"]["labels"] = tuple("{}kB, {}-way".format(*label) for label in L1i_tests)
    final_tests[bench]["l1i"]["cmds"].extend(generate_cmds(bench, "l1i", L1i_tests, final_tests[bench]["l1i"]["labels"]))
    print("L1i:", len(L1i_tests), L1i_tests)
    
    L1d_tests = list(itertools.product(L1d_sizes, l1d_assocs))
    final_tests[bench]["l1d"]["labels"] = tuple("{}kB, {}-way".format(*label) for label in L1d_tests)
    final_tests[bench]["l1d"]["cmds"].extend(generate_cmds(bench, "l1d", L1d_tests, final_tests[bench]["l1d"]["labels"]))
    print("L1d:", len(L1d_tests), L1d_tests)

    L2_tests = list(itertools.product(L2_sizes, l2_assocs))
    final_tests[bench]["l2"]["labels"] = tuple("{}kB, {}-way".format(*label) for label in L2_tests)
    final_tests[bench]["l2"]["cmds"].extend(generate_cmds(bench, "l2", L2_tests, final_tests[bench]["l2"]["labels"]))
    print("L2:", len(L2_tests), L2_tests)

    Cache_line_tests = cacheline_sizes
    final_tests[bench]["cache_line"]["labels"] = tuple(f"{label} Bytes" for label in Cache_line_tests)
    final_tests[bench]["cache_line"]["cmds"].extend(generate_cmds(bench, "cache_line", Cache_line_tests, final_tests[bench]["cache_line"]["labels"]))
    print("Cache_line_tests:", len(Cache_line_tests), Cache_line_tests)

    total = len(L1d_tests) + len(L1i_tests) + len(L2_tests) + len(Cache_line_tests)
    print(f"In total: {total} tests for {bench}")
    grand_total_tests += total

    

    #final_tests.extend(generate_cmds(bench, ))

    #break

print(f"Grand Total: {grand_total_tests}!")

print(json.dumps(final_tests, indent=4))

pickle.dump( final_tests, open( "final_tests.pickle", "wb" ) )

#pp.pprint(final_tests)
#sys.exit(0)


os.chdir(os.path.realpath("../gem5_fromdocker/my_gem5/"))
print(os.getcwd())


#print(cmds)
counter = 0
for bench in final_tests:
    for test in final_tests[bench]:
        print(bench, test, final_tests[bench][test]["labels"])

start_time = time.time()

for bench in final_tests:
    for test in final_tests[bench]:
        print("\n\n", bench, test, final_tests[bench][test]["labels"])
        for i, command in enumerate(final_tests[bench][test]["cmds"]):
            print(f"EXECUTING NEW TEST: \n{command}")
            print(bench, test, final_tests[bench][test]["labels"], final_tests[bench][test]["labels"][i])
            counter += 1
            if True:
                os.system(command)
            print(f"Simulation number: {counter}, Completion: {100*(counter/grand_total_tests):.2f}%, Total time till now: {datetime.timedelta(seconds=round(time.time() - start_time, 2))} H:M:S.")



print(counter)


print(f"Simulations finished in:{datetime.timedelta(seconds=round(time.time() - start_time, 2))}")


