import sys


def is_contig_header(line, inv_list):
    if line.startswith(">"):
        for each in inv_list:
            if each in line: return True
    return False


def parse(inv_fasta, filtered_contig_fasta):
    # For each match in inv_fasta
    inv_list = []
    with open(inv_fasta) as fin:
        for line in fin:
            if line.startswith(">"):
                line = (line.rpartition("_")[0]).rpartition("_")[0]
                if line not in inv_list:
                    inv_list.append(line)

    # Find the corresponding match in filtered_contig_fasta
    with open(filtered_contig_fasta) as fin:
        for line in fin:
            if is_contig_header(line, inv_list):
                print(line.strip()) # Print the header with Node information
                line = fin.readline().strip()
                while not line.startswith(">"): # Print nucleotide info
                    if line != "": print(line)
                    line = fin.readline().strip()


def main():
    inv_fasta = sys.argv[1] # If not in current dir, must include path
    filtered_contig_fasta = sys.argv[2]
    parse(inv_fasta, filtered_contig_fasta)


if __name__=="__main__":
    main()