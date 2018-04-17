'''
Given a .sam file extract the mapping of sequence to haplotype.
'''

import argparse
import re

haplotype = {}


def read_contigs(contig_file_name):
    with open(contig_file_name, 'r') as contig_file:
        for line in contig_file:
            found = re.search("(^seq[^\s]+)\s[^\s]+\s([^\s]+)", line)
            if found:
                haplotype[found.group(1)] = found.group(2)
    return haplotype


def write_haplotypes(output_file_name):
    global haplotype
    with open(output_file_name, 'w') as out_file:
        for sequence, haplotype in haplotype.iteritems():
            out_file.write("{0}\t{1}\n".format(sequence, haplotype))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("contigs")
    parser.add_argument("mapping")
    args = parser.parse_args()
    print(args)
    read_contigs(args.contigs)
    write_haplotypes(args.mapping)

