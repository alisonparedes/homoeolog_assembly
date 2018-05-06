import os
import sys
import argparse


def read_contigs():
    for line in sys.stdin:
        yield line.rstrip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-A")
    parser.add_argument("-a")
    parser.add_argument("-B")
    parser.add_argument("-b")
    args = parser.parse_args()
    contigs = read_contigs()
    print(args, file=sys.stderr, flush=True)
    i = 0
    while True:
        try:
            contig = next(contigs)
            command = ""
            command += "cat {0}".format(contig)
            command += " | python3 /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py"
            command += " {1} -o polymorphism_lengths_haplotype_04_{0}.tsv".format(i, args.A)
            command += " --relationship homologous "
            command += " |  python3 /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py"
            command += " {1} -o polymorphism_lengths_haplotype_02_{0}.tsv".format(i, args.a)
            command += " --relationship homologous "
            command += "|  python3 /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py"
            command += " {1} -o polymorphism_lengths_haplotype_01_{0}.tsv".format(i, args.B)
            command += " --relationship homoeologous "
            command += "|  python3 /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py"
            command += " {1} -o polymorphism_lengths_haplotype_03_{0}.tsv".format(i, args.b)
            command += " --relationship homoeologous "
            print(command, file=sys.stderr, flush=True)
            os.system(command)
            i += 1
        except StopIteration:
            break
    exit(0)