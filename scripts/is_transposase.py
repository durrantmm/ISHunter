import sys
from os.path import join, basename
from collections import defaultdict


def overlap_range(gi_range, contig_range):
    if len(set(gi_range).intersection(contig_range)) != 0: return True
    return False


def remove_symbol(string, sym):
    string = string.split(sym)[1]
    return int(string)


def get_range_gi(line):
    min = (line.split("..")[0]).rpartition(" ")[2]
    if "<" in min: min = remove_symbol(min, "<")
    else: min = int(min)

    max = line.split("..")[1]
    if ">" in max: max = remove_symbol(max, ">")
    else: max = int(max)

    if min > max:
        tmp = max
        min = max
        max = tmp
    max += 1

    return range(min, max)


def is_range(line):
    if "CDS " in line:
        if "(" not in line and ")" not in line:
            if ".." in line: return True
    return False


def strip_range(range):
    range = (str(range).strip("(")).strip(")")
    range_split = range.split(", ")
    return range_split[0] + "-" + range_split[1]


# Determines whether the gi is an IS
    # Finds first indication that it is IS
def is_transposase(gi_contig, gi_dir):
    is_entries = []
    for key in gi_contig: # For each gi ID...
        with open(join(gi_dir, key)) as fin:
            for line in fin: # Look through the gi file...
                if is_range(line): # If the file contains the range where the IS is located (in the complete genome)
                    gi_range_int = get_range_gi(line)

                    # Find overlap
                    for contig_name, contig_node_range, contig_gi_range in gi_contig[key]: # For each contig associated with this gi ID...
                        contig_gi_range_int = range(contig_gi_range[0], contig_gi_range[1])

                        while "/product" not in line and line != "\n":
                            line = fin.readline()

                        # If it is an IS...
                        if "transposase" in line or "transposon" in line:
                            if overlap_range(gi_range_int, contig_gi_range_int):
                                line = (line.split("=")[1]).split("\"")[1]
                                contig_gi_range = strip_range(contig_gi_range)
                                contig_node_range = strip_range(contig_node_range)

                                # The two overlapping ranges
                                entry = contig_name + "\t" + str(contig_node_range) + "\t" + str(contig_gi_range) + "\t" + line.strip()
                                is_entries.append(entry)
    return is_entries


def build_gi_contig(f):
    gi_contig = defaultdict(list)
    for line in open(f):
        gi_id = line.split("|")[1]
        node_id = line.split("_")[1]

        ranges_list = line.split(",")
        ranges_list_len = len(ranges_list)

        min_contig_node = int(ranges_list[ranges_list_len - 4])
        max_contig_node = int(ranges_list[ranges_list_len - 3])
        min_contig_gi = int(ranges_list[ranges_list_len - 2])
        max_contig_gi = int(ranges_list[ranges_list_len - 1])

        if min_contig_node > max_contig_node:
            tmp = max_contig_node
            min_contig_node = max_contig_node
            max_contig_node = tmp
        max_contig_node += 1

        if min_contig_gi > max_contig_gi:
            tmp = max_contig_gi
            min_contig_gi = max_contig_gi
            max_contig_gi = tmp
        max_contig_gi += 1


        entry = str(basename(f).split(".")[0]) + "\t" + "NODE_" + node_id
        gi_id += ".txt"
        if entry not in gi_contig[gi_id]:
            gi_contig[gi_id].append((entry, (min_contig_node, max_contig_node), (min_contig_gi, max_contig_gi)))

    return gi_contig


def main():
    f = sys.argv[1]
    gi_dir = sys.argv[2]
    gi_contig = build_gi_contig(f)
    is_entries = is_transposase(gi_contig, gi_dir)
    for each in is_entries:
        print(each)


if __name__=="__main__":
    main()