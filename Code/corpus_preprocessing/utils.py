import os
import sys
from pathlib import Path

def create_dir(checked_path):
    # checks if output dir exists, if not creates one
    if not os.path.exists(checked_path):
        os.mkdir(checked_path)
        print("Successfully created the %s" % checked_path)



def check_dir(checked_path):
    if os.path.exists(checked_path):
        print("Path %s already exists. Please remove the path first to avoid duplicating file input. Exiting." % checked_path)
        sys.exit()

    elif not os.path.exists(checked_path):
        os.mkdir(checked_path)
        print("Successfully created directory %s" % checked_path)
    else:
        print("sth went wrong")

def only_check_dir(checked_path):
    if os.path.exists(checked_path):
        print("Path %s already exists. Please remove the path first to avoid duplicating file input. Exiting." % checked_path)
        sys.exit()

def check_subdirectory_exists(df, directory, suffix_string):
    fn_list = df["filename"].tolist()
    # check if subdirs exist. exit if so to avoid dublicate writing into txt files.
    check_subdir = list(set([x.split('_spch')[0] for x in fn_list]))
    check_subdir_path = [Path(directory).joinpath(x + suffix_string) for x in check_subdir]
    for p in check_subdir_path:
        check_dir(p)