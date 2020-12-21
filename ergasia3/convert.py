import os, sys, glob
import pickle, pprint


pp = pprint.PrettyPrinter(indent=4, width=600)

pickle_file = "./../ergasia2/final_tests.pickle"

tests_dir = "./../ergasia2/spec_results/"

def convert_files( bench, test_name):
    filename = test_name + ".xml"
    print(os.getcwd())
    mcpat_base = "./../../../McPAT_fromdocker/my_mcpat"
    test_dir_base = "../../../for_git/auth_computer_architecture/ergasia2/spec_results/"
    stats = test_dir_base + f"{bench}/{test_name}/stats.txt"
    json =  test_dir_base + f"{bench}/{test_name}/config.json"
    script = mcpat_base + "/Scripts/GEM5ToMcPAT.py"
    xml_template = mcpat_base + "/mcpat/ProcessorDescriptionFiles/inorder_arm.xml"
    cmd = f"python {script} -o converted/{filename} {stats} {json} {xml_template}"
    #os.chdir(tests_dir)
    print(os.getcwd())
    os.system(cmd)


def main():

    #final_tests = pickle.load(open( pickle_file, "rb" ))
    #pp.pprint(final_tests)

    # Get test names
    os.chdir(tests_dir)
    filesDepth2 = glob.glob('*/*')
    test_dirs = list(filter(lambda f: os.path.isdir(f), filesDepth2))
    print(len(test_dirs))

    print(os.getcwd())
    os.chdir("../../ergasia3")

    for test in test_dirs:
        convert_files(*test.split("/"))


if __name__ == "__main__":
    main()
