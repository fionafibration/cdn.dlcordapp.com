# -*- coding: utf-8 -*-

import sys
import os
import argparse
import shutil


# Globals #

cwd = os.getcwd()
script_dir = os.path.dirname(os.path.realpath(__file__))


def main(argv):

    # Arguments #

    parser = argparse.ArgumentParser(description='Scaffold a Flask Skeleton.')
    parser.add_argument('appname', help='The application name')
    parser.add_argument('-s', '--skeleton', help='The skeleton folder to use.')
    args = parser.parse_args()

    # Variables #

    appname = args.appname
    fullpath = os.path.join(cwd, appname)
    skeleton_dir = args.skeleton

    # Tasks #

    # Copy files and folders
    shutil.copytree(os.path.join(script_dir, skeleton_dir), fullpath)


if __name__ == '__main__':
    main(sys.argv)

