import random

def read_file(file_name):
    sequence = ''
    with open(file_name, 'r') as my_file:
        for line in my_file:
            if line[0] == '>':
                print(line)
            else:
                sequence += line
    return sequence

mutation_model = {
'A':'TCG',
'T':'CGA',
'C':'GAT',
'G':'ATC'
}

def mutate(sequence, k):
    new_sequence = list(sequence)
    last_position = len(sequence) - 1
    for position in random.sample(range(last_position), k):
        orig_nucleotide = sequence[position]
        new_nucleotide = random.choice(mutation_model[orig_nucleotide])
        new_sequence[position] = new_nucleotide
    return ''.join(new_sequence)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("k")
    args = parser.parse_args()
    print(args)
    sequence = read_file(args.file_name)
    new_sequence = mutate(sequence, int(args.k))
    print(new_sequence)

