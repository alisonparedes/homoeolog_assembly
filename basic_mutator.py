"""
This very basic mutator takes a file containing a single, complete, ground truth genome (see example test_01) and a
parameter k which is the number of mutations you want to apply to it. Then it creates a new sequence with exactly k
mutations.
Example command line: python basic_mutator.py test_01.fna 1 ALISON
"""

import random
import heapq
import copy

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


def sample_positions(sequence, k_snps, seed):
    random.seed(seed)
    last_position = len(sequence) - 1
    k_random_positions = random.sample(range(last_position), k_snps)
    return k_random_positions


def mutate(sequence, k_random_positions):
    new_sequence = list(sequence)
    for position in k_random_positions:
        orig_nucleotide = sequence[position]
        new_nucleotide = random.choice(mutation_model[orig_nucleotide])
        new_sequence[position] = new_nucleotide
    return ''.join(new_sequence)


def snp_density_distribution(sequence, snp_positions, interval):
    min_heap = copy.copy(snp_positions)
    heapq.heapify(min_heap)
    end_position = interval - 1
    count = 0
    distribution = {}
    while end_position < len(sequence) + interval:
        if len(min_heap) > 0 and min_heap[0] <= end_position:
            heapq.heappop(min_heap)
            count += 1
        else:
            end_position += interval
            distribution[count] = distribution.get(count, 0) + 1
            count = 0
    return distribution


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("k_snps")
    parser.add_argument("seed")
    args = parser.parse_args()
    k_snps = int(args.k_snps)

    orig_sequence, header = read_file(args.file_name)
    random_positions = sample_positions(orig_sequence, k_snps, args.seed)
    new_sequence = mutate(orig_sequence, random_positions)
    snp_distribution = snp_density_distribution(new_sequence, random_positions, interval=100)
    print("{0} | snp density distribution: {1}".format(header, snp_distribution))
    print("{0}".format(new_sequence))

