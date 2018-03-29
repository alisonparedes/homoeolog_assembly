import argparse
import os
import basic_mutator

if __name__ == "__main__":
    source_file = "lambdaphage.fna"
    seeds = ["ALISON", "JOE"]
    mutations_pct = 0.05
    sequence, header, name = basic_mutator.read_file(source_file)
    mutations_snps = int(len(sequence) * mutations_pct)
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
        os.system("basic_mutator.py {0} {1} {2} > {3}".format("lambda_snp{0:02d}_seed{1}.fa".format(percent, seed), mutations_snps, seed, "lambda_a_snp{0:02d}_seed{1}.fa".format(percent, seed)))

    for percent, no_snps in snps.iteritems():
        seed = species_b # Use a different seed so that this set of species are different from the one above
        os.system("basic_mutator.py {0} {1} {2} > {3}".format(source_file, no_snps, seed, "lambda_snp{0:02d}_seed{1}.fa".format(percent, seed)))
        os.system("basic_mutator.py {0} {1} {2} > {3}".format("lambda_snp{0:02d}_seed{1}.fa".format(percent, seed), mutations_snps, seed, "lambda_b_snp{0:02d}_seed{1}.fa".format(percent, seed)))
        os.system("type lambda_snp{0:02d}_seed{1}.fa lambda_snp{0:02d}_seed{2}.fa lambda_a_snp{0:02d}_seed{1}.fa lambda_b_snp{0:02d}_seed{2}.fa > lambda_diploid_snp{0:02d}.fa".format(percent, species_a, species_b))


