"""
This very basic mutator takes a file containing a single, complete, ground truth genome (see example test_01) and a
parameter k which is the number of mutations you want to apply to it. Then it creates a new sequence with exactly k
mutations.
Example command line: python basic_mutator.py test_01.fna 1 ALISON
"""

import random


def read_file(file_name):
    sequence = ''
    header = ''
    with open(file_name, 'r') as my_file:
        for line in my_file:
            if line[0] == '>':
                header = line.rstrip()
            else:
                sequence += line
    return sequence, header


mutation_model = {
'A':'TCG',
'T':'CGA',
'C':'GAT',
'G':'ATC'
}


def sample_positions(sequence, k, seed):
    random.seed(seed)
    new_sequence = list(sequence)
    last_position = len(sequence) - 1
    k_random_positions = random.sample(range(last_position), k)
    return k_random_positions


def mutate(sequence, k_random_positions):
    new_sequence = list(sequence)
    for position in k_random_positions:
        orig_nucleotide = sequence[position]
        new_nucleotide = random.choice(mutation_model[orig_nucleotide])
        new_sequence[position] = new_nucleotide
    return ''.join(new_sequence)


def snp_density(sequence, snp_positions):
    total_bp = len(sequence)
    snp_count = len(snp_positions)
    return snp_count / total_bp


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("k")
    parser.add_argument("seed")
    args = parser.parse_args()

    orig_sequence, header = read_file(args.file_name)
    random_positions = sample_positions(orig_sequence, int(args.k), args.seed)
    new_sequence = mutate(orig_sequence, random_positions)

    print("{0} | snp density: {1}".format(header, snp_density(orig_sequence, random_positions)))
    print("{0}".format(new_sequence))

