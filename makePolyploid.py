"""
This very basic mutator takes a file containing a single, complete, ground truth genome (see example test_01) and a
parameter k which is the number of mutations you want to apply to it. Then it creates a new sequence with exactly k
mutations.
Example command line: python basic_mutator.py test_01.fna 1 ALISON
"""

'''
This is an extension of Alison's mutator program with an attempt to 
add ploidy levels. Given a ploidy level it creates mutated sequences
and generates ploidy based fasta files
''' 

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


#TODO if fast file doesn't end with line.strip() the last
#line is "lost"
def write_ploidy_files(file_name, ploidy_level, k, seed, ploidy_files):
	processing_sequence = False
	tmp_sequence = ''
	with open(file_name, 'r') as my_file:
		for line in my_file:
			if line[0] == '>':
				header = line
				processing_sequence = True
			elif line.strip() == '' and processing_sequence:
					for i in range(0, ploidy_level - 1):
						ploidy_file = ploidy_files[i] 
						# make new header with poly info all one line
						new_header = header[:len(header)-1]
						new_header += ":ploidy_level " + str(i + 2)
						ploidy_file.write(new_header + '\n')
						# use the mutatation mechanism to alter the new sequence
						random_positions = sample_positions(tmp_sequence, k, seed)
						new_sequence = mutate(tmp_sequence, random_positions)
						ploidy_file.write(new_sequence + '\n')
						# display SNP distribution of the sequence
						display_snp_distr(new_header, new_sequence, random_positions)	
					tmp_sequence = ''		
					processing_sequence = False
			elif line.strip() != '':
					tmp_sequence += line
				    
			


mutation_model = {
'A':'TCG',
'T':'CGA',
'C':'GAT',
'G':'ATC'
}


# more likely for A G, C T


def sample_positions(sequence, k, seed):
    random.seed(seed)
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
    
    
def display_snp_distr(header, sequence, random_positions, interval=100):
    snp_distribution = snp_density_distribution(sequence, random_positions, interval)
    print("{0} | snp density distribution: {1}".format(header, snp_distribution))
    print("{0}".format(sequence))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("k")
    parser.add_argument("seed")
    parser.add_argument("ploidy_level")
    args = parser.parse_args()
    file_name = args.file_name
    k = int(args.k)
    
    ploidy_level = int(args.ploidy_level)
    ploidy_files = []
    for i in range(0, ploidy_level - 1):
		f = open(("ploidy_file" + str(i + 2) + ".fna"), 'w')
		ploidy_files.append(f) 
    
    if ploidy_level < 2:
		print("Ploidy_level must be > 1")
    else:
		write_ploidy_files(file_name, ploidy_level, k, args.seed, ploidy_files)
	
	#TODO: interpret the result (somehow)
