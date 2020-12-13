import os, sys, glob
import configparser
import pprint, json, pickle, time, datetime

import matplotlib
import matplotlib.pyplot as plt
#import  as ax
import numpy as np
import math

CONFIG_FILE = "conf_script.ini"

limits_all = []
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


    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    #langs = ['C', 'C++', 'Java', 'Python', 'PHP']
    #students = [23,17,35,29,12]
    #ax.bar(langs,students)
    ax.bar(bars, heights, color=['coral', 'indianred', 'forestgreen', 'chocolate', 'skyblue'])
    #plt.show()
    
    low , high, min_max_range = min(heights), max(heights), max(heights) - min(heights)
    

    # Create bars
    bottom = 0.0#low - 0.5
    #plt.bar(y_pos, heights, color=['coral', 'indianred', 'forestgreen', 'chocolate', 'skyblue'])

    #ax.autoscale(enable=True, axis='both', tight=True)
    #plt.ylim([math.floor(low-0.5*(high-low)), math.ceil(high+0.5*(high-low))])
    print("DEBUG:", filename, heights, bars, bottom)
    print(plt.get_fignums())
    #plt.ylim(low - min(0.5*min_max_range, 1.0), high + 0.5 * min_max_range)
    #plt.ylim(0.0, 8.0)
    # Create names on the x-axis
    ax.set_xticks(y_pos, bars)
    #ax = matplotlib.axes.Axes()
    #plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    #plt.figure(1, [4, 8])
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    plt.savefig(filename)
    # Show graphic
    #plt.show()

if __name__ == "__main__":

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(CONFIG_FILE)
    print(config.sections())


    pp = pprint.PrettyPrinter(indent=4, width=600)
    final_tests = pickle.load(open( "final_tests.pickle", "rb" ))

    print("Gathering stats")

    os.chdir("spec_results/")
    filesDepth2 = glob.glob('*/*')
    dirsDepth2 = list(filter(lambda f: os.path.isdir(f), filesDepth2))
    pp.pprint(dirsDepth2)
    print(len(dirsDepth2))
    os.chdir("../")


    config['Benchmarks'] == None
    for directory in dirsDepth2:
        config['Benchmarks'][directory] = None
    #print(config['Benchmarks'][directory])

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
        print("Stats file written!")

    if False:
        os.system("./read_results.sh conf_script.ini")


    with open (list(config['Output'])[0], 'r') as stats_file:
        stats = stats_file.readlines()

    cpi_stats = []
    for line in stats:
        if line.startswith( ('specbzip', 'specsjeng', 'spechmmer', 'specmcf', 'speclibm' ) ):
            cpi_stats.append(line.strip().rsplit('\t', 1)[0])

    pp.pprint(cpi_stats)

    cpi_stats_dict =  dict(map(lambda s : s.split('\t'), cpi_stats))


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


ppp = pprint.PrettyPrinter(indent=4, width=50)
ppp.pprint(limits_all)

