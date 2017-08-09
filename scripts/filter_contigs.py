import sys
import numpy

fname = ""


def calc_cov(fname, sdevs_above):
    cov_all = []

    with open(fname) as fin:
        for line in fin:
            if line.startswith(">"):
                line_split = line.split("_")
                cov_all.append(float(line_split[5].strip()))

    avg = numpy.mean(cov_all)
    std = numpy.std(cov_all)

    return avg + sdevs_above*std


def valid_contig(len, cov, param_len_min, param_len_max, param_cov):
    return (len >= param_len_min) and (len <= param_len_max) and (cov >= param_cov)


def parse(fname, param_len_min, param_len_max, param_cov):
    with open(fname) as fin:
        for line in fin:
            if line.startswith(">"):
                line_split = line.split("_")
                len = float(line_split[3].strip())
                cov = float(line_split[5].strip())

                if valid_contig(len, cov, param_len_min, param_len_max, param_cov):
                    print(line.strip()) # Print the header with Node information
                    line = fin.readline().strip()
                    while not line.startswith(">"): # Print nucleotide info
                        if line != "": print(line)
                        line = fin.readline().strip()


def main():
    fname = sys.argv[1] # If not in current dir, must include path
    param_len_min = float(sys.argv[2])
    param_len_max = float(sys.argv[3])
    sdevs_above = float(sys.argv[4])
    param_cov = calc_cov(fname, sdevs_above)


    parse(fname, param_len_min, param_len_max, param_cov)


if __name__ == "__main__":
    main()