import sys


# Check whether the line contains the ID of any inverted repeat ID (return bool)
def is_contig_header(line, inv_list):
    for each in inv_list:
        if each in line: return True
    return False


# Check whether the length of inverted repeat is above cutoff
def check_length(start, end, min_len):
    diff = abs(end-start)
    if diff < min_len: return False
    return True


# Iterate through fasta files to filter contigs that (1) have inverted repeats
# and (2) whose inverted repeats are at least the input size
def parse(inv_fasta, filtered_contig_fasta, min_len):
    # For each match in inv_fasta
    inv_list = []
    with open(inv_fasta) as fin:
        for line in fin:
            if line.startswith(">"):
                line = line.strip(">")
                line_id = (line.rpartition("_")[0]).rpartition("_")[0]
                start = float(line.split("_")[6]) # Start pos of inverted read

                while not line.startswith(">"): # Skip non-headers
                    line = fin.readline().strip()

                line = line.strip(">")
                end = float(line.split("_")[7]) # End pos of inverted read

                if line_id not in inv_list and check_length(start, end, min_len):
                    inv_list.append(line_id)

    # Find the corresponding match in filtered_contig_fasta
    with open(filtered_contig_fasta) as fin:
        for line in fin:
            if line.startswith(">"):
                if is_contig_header(line, inv_list):
                    print(line.strip()) # Save the header with Node information
                    line = fin.readline().strip()
                    while not line.startswith(">"): # Save nucleotide info
                        if line != "": print(line)
                        line = fin.readline().strip()


def main():
    inv_fasta = sys.argv[1] # If not in current dir, must include path
    filtered_contig_fasta = sys.argv[2]
    minimum_len = float(sys.argv[3])
    parse(inv_fasta, filtered_contig_fasta, minimum_len)


if __name__=="__main__":
    main()