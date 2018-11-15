#!/usr/bin/env python3
import argparse
import os
import hashlib
import shutil


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='+', help='init/add/commit/snapshots/index/config/status')
    args = parser.parse_args()
    return args.command


def main():
    args = get_argument()
    command = args[0]
    if command == 'init':
        create_dir()
    elif command == 'add':
        argument = args[1:]
        for item in argument:
            lgit_add(item)


def caculate_sha1_file(filename):
    hasher = hashlib.sha1()
    with open(filename, 'rb') as afile:
        buf = afile.read()
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read()
    return hasher.hexdigest()


def directory_tree_list(path):
    list_file = []
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            list_file.append(os.path.join(dirname, filename))
    return list_file


def create_dir():
    path = os.getcwd() + '/.lgit'
    if os.path.exists(path):
        print('Reinitialized existing Git repository in ' + path)
        shutil.rmtree(path)
    else:
        print('Initialized empty Git repository in ' + path)
    os.mkdir(path)
    os.mkdir(path + '/commits')
    os.mkdir(path + '/objects')
    os.mkdir(path + '/snapshot')
    os.path.join(path,'index')
    os.path.join(path,'config')


def create_file_objects(filename):
    path = os.getcwd()
    file_content = open(filename,'r').read()
    path_objects = path +'/.lgit/objects'
    hash_sha1 = caculate_sha1_file(filename)
    print(hash_sha1)
    file_name = hash_sha1[2:]
    dir_name =  hash_sha1[:2]
    if not os.path.exists(path_objects + "/" + dir_name):
        os.mkdir(path_objects + "/" + dir_name)
    file = open(path_objects + "/" + dir_name + "/" + file_name, 'w+')
    file.write(file_content)
    file.close()
    hash_sha2 = caculate_sha1_file(path_objects + "/" + dir_name + "/" + file_name)
    print(hash_sha2)
    index = create_structure_index(filename, hash_sha1, hash_sha2)
    with open(path_objects + "/" + dir_name + "/" + file_name, 'w+') as f_index:
        f_index.write(index)
    f_index.close()


def create_structure_index(filename, hash1, hash2):
    file_index = []
    timestamp = str(get_timestamp(filename))
    file_index.append(timestamp)
    SHA1_file = hash1
    file_index.append(SHA1_file)
    SHA1_file_added = hash2
    file_index.append(SHA1_file_added)
    #SHA1 of the file content after commited
    file_index.append(' ' * 40)
    file_index.append(filename)
    return ' '.join(file_index)

def get_timestamp(filename):
    stat = os.stat(filename)
    return stat.st_mtime

def lgit_add(file_name):
    if os.path.isdir(file_name):
        files = directory_tree_list(file_name)
        for file in files:
            create_file_objects(file)
    elif os.path.isfile(file_name):
        create_file_objects(file_name)








if __name__ == '__main__':
    main()
