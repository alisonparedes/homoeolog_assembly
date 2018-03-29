"""
This very basic mutator takes a file containing a single, complete, ground truth genome (see example test_01) and a
parameter k which is the number of mutations you want to apply to it. Then it creates a new sequence with exactly k
mutations.
Example command line: python basic_mutator.py test_01.fna 1 ALISON
"""

import random
import heapq
import copy
import re

def read_file(file_name):
    sequence = ''
    header = ''
    name = ''
    with open(file_name, 'r') as my_file:
        for line in my_file:
            if line[0] == '>':
                header = line.rstrip()
                find_name = re.search("^>([^\s]+)\s", header)
                name = find_name.group(1)
            else:
                sequence += line.rstrip()
    return sequence, header, name


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


def avg_snp_density(sequence, snp_positions, per_bp=1000):
    min_heap = copy.copy(snp_positions)
    heapq.heapify(min_heap)
    end_position = per_bp - 1
    snps = 0
    sum_snp_density = 0.0
    while end_position < len(sequence) + per_bp:
        if len(min_heap) > 0 and min_heap[0] <= end_position:
            heapq.heappop(min_heap)
            snps += 1
        else:
            end_position += per_bp
            sum_snp_density += snps/float(per_bp)
            snps = 0
    return sum_snp_density / (max(len(sequence)/per_bp, 1))



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("k_snps")
    parser.add_argument("seed")
    args = parser.parse_args()
    k_snps = int(args.k_snps)
    per_bp = 1000

    orig_sequence, header, name = read_file(args.file_name)
    random_positions = sample_positions(orig_sequence, k_snps, args.seed)
    new_sequence = mutate(orig_sequence, random_positions)
    snp_distribution = avg_snp_density(new_sequence, random_positions, per_bp)
    print("{0} | average snp density per {1} bp: {2}, total bp: {3}".format(header.replace(name, "{0}.{1}.{2}".format(name, k_snps, args.seed)), per_bp, snp_distribution, len(new_sequence)))
    print("{0}".format(new_sequence))

