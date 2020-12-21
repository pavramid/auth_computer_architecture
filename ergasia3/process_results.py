import os, sys, glob
import pprint, pickle
import numpy as np
import math
#from tqdm import tqdm

import matplotlib
import matplotlib.pyplot as plt
#import  as ax
import numpy as np
import math


pp = pprint.PrettyPrinter(indent=4, width=600)

tests_dir = "./../ergasia2/spec_results/"
limits_all = []

def process_mcpat_text(filepath):
    print(filepath)
    #filepath = "mcpat_files/specbzip_cache_line_64_bytes.txt"
    with open( filepath, "rb" ) as f:
        file_str = f.readlines()

    counter = 0
    important_lines = []
    for line in file_str:
        if counter >= 8:
            counter = 0

        if line.startswith(b"L2") or line.startswith(b"Core:"):
            counter += 1

        if counter < 8 and counter > 0:
            counter += 1
            important_lines.append(line.strip().decode("utf-8"))

    important_info = {}
    important_info["L2"] = {}
    important_info["Core:"] = {}
    
    for i in range(len(important_lines)):
        key = important_lines[0] if i < 7 else important_lines[7]
        if i != 0 and i != 7:
            important_info[key][important_lines[i].split(' = ')[0]] = float(important_lines[i].split(' = ')[1].split(' ')[0])
    return important_info

def plot_barplot(title, heights, bars, filename, ylabel = 'CPI'):
    #height = [2.624227, 2.624227, 2.624227, 2.624227]
    #bars = ('2-2-2', '2-2-4', '2-4-2', '2-4-4')
    if len(heights) != len(bars):
        print("Problematic Input!")
        sys.exit(0)
    bars = tuple(bars)
    y_pos = np.arange(len(bars))


    #data = {'C':20, 'C++':15, 'Java':30,  
    #        'Python':35} 
    #courses = list(data.keys()) 
    #values = list(data.values()) 
       
    fig = plt.figure(figsize = (10, 5)) 
      
    # creating the bar plot 
    plt.bar(bars, heights, color=['coral', 'indianred', 'brown', 'forestgreen', 'chocolate', 'skyblue', 'gold', 'olive'],  
            width = 0.6)
    print("DEBUG:", filename, heights, bars)
    low , high, min_max_range = min(heights), max(heights), max(heights) - min(heights)
    print(math.ceil(low-0.5*(high-low)), math.floor(low-0.5*(high-low)))
    limits = [round((low-0.5*(high**0.5-low**0.5))-0.01, 2), round((high+0.5*(high**0.5-low**0.5))+0.01, 2)]
    limits_all.append(limits)
    print(limits)
    plt.ylim(limits)
      

    plt.xticks(rotation=15)
    plt.ylabel(ylabel) 
    plt.title(title) 
    plt.savefig(filename) 
    return


def main():
        
    final_tests = pickle.load(open( "./../ergasia2/final_tests.pickle", "rb" ))
    
    os.chdir(tests_dir)
    filesDepth2 = glob.glob('*/*')
    test_dirs = list(filter(lambda f: os.path.isdir(f), filesDepth2))
    os.chdir("./../../ergasia3")

    mcpat_result_dict = {}
    for filepath in filesDepth2:
        #mcpat_result_dict[filepath.split('/')[0]] = process_mcpat_text("mcpat_files/" + filepath.split('/')[1] + ".txt")
        mcpat_result_dict[filepath] = process_mcpat_text("mcpat_files/" + filepath.split('/')[1] + ".txt")

    power_cons = {}
    for bench in mcpat_result_dict:
        power_cons[bench] = 0
        for key in mcpat_result_dict[bench]:
            print(mcpat_result_dict[bench][key])
            power_cons[bench] += mcpat_result_dict[bench][key]['Subthreshold Leakage'] + mcpat_result_dict[bench][key]['Gate Leakage'] + mcpat_result_dict[bench][key]['Runtime Dynamic']
    
    for key in power_cons: 
        print(f"| {key.split('/')[1]} | {power_cons[key]:.3f} |")

        
        

    #Area, l1i
    tests = {}
    for plot_type in ["Peak Dynamic", "Area"]:
        tests[plot_type] = {}
        for cpu_component in ["L2", "Core:"]:
            tests[plot_type][cpu_component] = {}
            for filepath in filesDepth2:
                #print(plot_type, cpu_component, len(list(mcpat_result_dict.values())), list(mcpat_result_dict.values()))
                tests[plot_type][cpu_component][filepath] = mcpat_result_dict[filepath][cpu_component]
                #print(plot_type, cpu_component, filepath, mcpat_result_dict[filepath])

    for plot_type in tests:
        for cpu_component in tests[plot_type]:
            print(tests[plot_type][cpu_component].keys())
            heights = []
            bars = []
            for test_type in tests[plot_type][cpu_component]:
                if "l2" in test_type:
                    heights.append(tests[plot_type][cpu_component][test_type][plot_type])
                    bars.append(test_type.split("_")[2] + test_type.split("_")[3])
            print(heights, bars)
            plot_barplot(plot_type + " / " + cpu_component , heights, bars, f"mcpat_plots/{plot_type}_{cpu_component}.png", plot_type)

    sys.exit(0)
    for category in mcpat_result_dict:
        for value_type in mcpat_result_dict[category]:
            print(category, value_type, mcpat_result_dict[category][value_type])
                
                #for 
    sys.exit(0)
    for bench in final_tests:
        for test in final_tests[bench]:
                #print(bench, test, final_tests[bench][test]["labels"])
                heights = []
                bars = []
                for label in final_tests[bench][test]["labels"]:    
                    name = f"{bench}/{bench}_{test}_{label.lower().replace(' ', '_').replace(',', '')}"
                    #print(name, label, cpi_stats_dict[name])
                    heights.append(float(cpi_stats_dict[name]))
                    bars.append(label)
                title = f"{bench.title()} {test.replace('_', ' ')}"
                print("\n", title)
                print(len(heights), heights)
                print(len(bars), bars)
                plot_barplot(title, heights, bars, filename = f"plots/{bench}/{test}")

    pp.pprint(mcpat_result_dict)


if __name__ == "__main__":
    main()
