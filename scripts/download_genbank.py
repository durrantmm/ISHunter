from Bio import Entrez
import os
from os.path import join
import sys

wd = sys.argv[1]
output_dir = sys.argv[2]


def download_genbank(id_num):
    Entrez.email = "mli6@stanford.edu"
    handle = Entrez.efetch(db="nucleotide", id=id_num, rettype="gb", retmode="text")
    path = join(output_dir, id_num + ".txt")
    with open(path, 'w') as fout:
        for line in handle:
            fout.write(line)


def compile_IS_id(dir, complete):
    id_list = []
    for line in open(join(wd, dir)):
        name = line.split("|")[1]
        if name not in complete and name not in id_list:
            id_list.append(name)
    return id_list


def main():

    complete = []
    for f in os.listdir(output_dir):
        complete.append(f.split(".")[0])
    for filename in os.listdir(wd):
        id_list = compile_IS_id(filename, complete)
        for id in id_list:
            download_genbank(id)
            complete.append(id)



if __name__ == '__main__':
    main()
