#!/usr/bin/env python3
import hashlib
import argparse
import os
def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='+', help='init/add/commit/snapshots/index/config/status')
    args = parser.parse_args()
    return args.command


def caculate_sha1_file(filename):
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read()
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read()
    return hasher.hexdigest()


def directory_tree_list(path):
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            print(os.path.join(dirname, filename))

path = os.getcwd()
caculate_sha1_file('text.txt')
directory_tree_list(path)
