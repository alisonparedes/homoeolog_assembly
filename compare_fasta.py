import argparse
import re


def fasta_reader(fasta_file_name):
    with open(fasta_file_name, 'r') as fasta_file:
        next_char = fasta_file.read(1)
        comment = False
        while next_char:
            if next_char in ('>','*','s'):
                comment = True
            elif comment and next_char == '\n':
                comment = False
            elif not comment and next_char != '\n':
                yield next_char
            next_char = fasta_file.read(1)


def compare_fasta(name_file_a, name_file_b, vcf_file_name):
    a_reader = fasta_reader(name_file_a)
    b_reader = fasta_reader(name_file_b)
    with open(vcf_file_name, 'w') as vcf_file:
        vcf_file.write("##fileformat=VCFv4.0\n")
        vcf_file.write("##fileDate=20180329\n")
        vcf_file.write("##reference=lambdaphage\n")
        vcf_file.write("##phasing=partial\n")
        vcf_file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
    i = 0
    while True:
        try:
            nuc_a = next(a_reader)
            nuc_b = next(b_reader)
            i += 1
            if nuc_a != nuc_b and nuc_a != '-' and nuc_b != '-':
                with open(vcf_file_name, 'a') as vcf_file:
                    vcf_file.write("{0}\t{1}\t.\t{2}\t{3}\t.\tPASS\t.\n".format(name_file_b, i, nuc_a, nuc_b))
        except(StopIteration):
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("contig")
    parser.add_argument("ref")
    parser.add_argument("vcf")
    args = parser.parse_args()
    print(args)
    compare_fasta(args.ref, args.contig, args.vcf)