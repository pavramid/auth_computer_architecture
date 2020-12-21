import os, sys, glob
import pickle, pprint
from tqdm import tqdm

pp = pprint.PrettyPrinter(indent=4, width=600)

pickle_file = "./../ergasia2/final_tests.pickle"

tests_dir = "./../ergasia2/spec_results/"
    
def mcpat_run(infile, print_level = 5):
    #./mcpat -infile ProcessorDescriptionFiles/Xeon.xml -print_level 1
    base = "./../../../McPAT_fromdocker/my_mcpat/mcpat"
    cmd = f"{base}/mcpat -infile converted/{infile}.xml -print_level {print_level} > {infile}.txt"
    os.system(cmd)

def main():

    #final_tests = pickle.load(open( pickle_file, "rb" ))
    #pp.pprint(final_tests)

    # Get test names
    os.chdir(tests_dir)
    filesDepth2 = glob.glob('*/*')
    test_dirs = list(filter(lambda f: os.path.isdir(f), filesDepth2))
    os.chdir("./../../ergasia3")
    print(len(test_dirs))

    for test in tqdm(test_dirs):
        #print(test)
        mcpat_run(test.split("/")[1])

    #os.system()
    #./../mcpat/ProcessorDescriptionFiles/inorder_arm.xml
if __name__ == "__main__":
    main()
