import argparse
import os
import basic_mutator
import re


def compare_fasta(name_file_a, name_file_b, vcf_file_name):

    name = ''

    with open(name_file_a, 'r') as file_a:
        with open(name_file_b, 'r') as file_b:

            for line_a in file_a:
                if line_a[0] == '>':
                    line_b = file_b.readline()
                    find_name = re.search("^>([^\s]+)\s", line_a)
                    name = find_name.group(1)
                    with open(vcf_file_name, 'w') as vcf_file:
                        vcf_file.write("##fileformat=VCFv4.0\n")
                        vcf_file.write("##fileDate=20180329\n")
                        vcf_file.write("##reference=lambdaphage\n")
                        vcf_file.write("##phasing=partial\n")
                        vcf_file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

                else:  # genome
                    line_b = file_b.readline()
                    i = 0
                    while i < len(line_a):
                        if line_a[i] != line_b[i]:

                            with open(vcf_file_name, 'a') as vcf_file:
                                vcf_file.write("{0}\t{1}\t.\t{2}\t.\tPASS\t.{3}\n".format(name, i+1, line_a[i], line_b[i]))
                        i += 1


if __name__ == "__main__":
    source_file = "lambdaphage.fna"
    seeds = ["ALISON", "JOE"]
    allelic_pct = 0.05
    sequence, header, name = basic_mutator.read_file(source_file)
    allelic_snps = int(len(sequence) * allelic_pct)
    snps = {}
    for percent in range(1, 5, 1):
        snps[percent] = int(len(sequence) * (percent / 100.0))
    for percent in range(5, 100, 5):
        snps[percent] = int(len(sequence) * (percent / 100.0))

    species_a = seeds[0]
    species_b = seeds[1]
    for percent, no_snps in snps.iteritems():
        seed = species_a
        os.system("basic_mutator.py {0} {1} {2} > {3}".format(source_file, no_snps, seed, "lambda_snp{0:02d}_seed{1}.fa".format(percent, seed)))
        os.system("basic_mutator.py {0} {1} {2} > {3}".format("lambda_snp{0:02d}_seed{1}.fa".format(percent, seed), allelic_snps, seed, "lambda_a_snp{0:02d}_seed{1}.fa".format(percent, seed)))

    for percent, no_snps in snps.iteritems():
        seed = species_b # Use a different seed so that this set of species are different from the one above
        os.system("basic_mutator.py {0} {1} {2} > {3}".format(source_file, no_snps, seed, "lambda_snp{0:02d}_seed{1}.fa".format(percent, seed)))
        os.system("basic_mutator.py {0} {1} {2} > {3}".format("lambda_snp{0:02d}_seed{1}.fa".format(percent, seed), allelic_snps, seed, "lambda_b_snp{0:02d}_seed{1}.fa".format(percent, seed)))

        # Combine all four files into one
        os.system("type lambda_snp{0:02d}_seed{1}.fa lambda_snp{0:02d}_seed{2}.fa lambda_a_snp{0:02d}_seed{1}.fa lambda_b_snp{0:02d}_seed{2}.fa > lambda_diploid_snp{0:02d}.fa".format(percent, species_a, species_b))
        compare_fasta("lambda_snp{0:02d}_seed{1}.fa".format(percent, species_a), "lambda_snp{0:02d}_seed{1}.fa".format(percent, species_b), "lambda_diploid_snp{0:02d}.vcf".format(percent))  # Writes a vcf file

