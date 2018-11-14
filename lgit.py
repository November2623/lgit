#!/usr/bin/env python3
import argparse
import os
import hashlib
import sys


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='+', help='init/add/commit/snapshots/index/config/status')
    args = parser.parse_args()
    return args.command


def main():
    args = get_argument()
    command = args[0]
    print(command)
    if command == 'init':
        create_dir()


def create_dir():
    path = os.getcwd() + '/.lgit'
    os.mkdir(path)
    os.mkdir(path + '/commits')
    os.mkdir(path + '/objects')
    os.mkdir(path + '/snapshot')
    os.mknod(path + '/index')
    os.mknod(path + '/config')
    return path
# def lgit_add(file_name):





if __name__ == '__main__':
    main()
