import argparse
import re

def score_reader(score_tsv):
    with(open(score_tsv, 'r')) as score_file:
        for line in score_file:
            if line[0] not in  ('h','I'):
                haplotype, contig, score, delta = line.split("\t")
                yield haplotype, contig


def read_scores(score_tsv):
    reader = score_reader(score_tsv)
    best_haplotype = {}
    while True:
        try:
            haplotype, contig = next(reader)
            best_haplotype[contig] = haplotype
        except StopIteration:
            break
    return best_haplotype


def filter_lengths(lengths_tsv, best_haplotype):
    with(open(lengths_tsv, 'r')) as lengths_file:
        for line in lengths_file:
            found = re.search("^([^\s]+)\t([^\s]+)\t", line)
            if found and best_haplotype[found.group(2)] == found.group(1):
                print(line.strip(), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("score_file")
    parser.add_argument("lengths_file")
    args = parser.parse_args()
    best_haplotype = read_scores(args.score_file)
    filter_lengths(args.lengths_file, best_haplotype)
    exit(0)
