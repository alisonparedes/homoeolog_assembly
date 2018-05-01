import argparse
import re
import numpy as np



def vcf_reader(vcf_file_name):
    with open(vcf_file_name, 'r') as vcf_file:
        for line in vcf_file:
            if line[0] == '#':
                pass
            else:
                found = re.search("^[^\s]+\t([0-9]+)\t[^\s]\t([AGCT]+)\t([AGCT]+)", line)
                yield int(found.group(1)), found.group(2), found.group(3), line


def read_truth(ground_truth_vcf):
    truth_reader = vcf_reader(ground_truth_vcf)
    ground_truth = {}
    while True:
        try:
            position, _, to_acid, _ = next(truth_reader)
            ground_truth[(position, to_acid)] = 1
        except(StopIteration):
            break
    return ground_truth

def vclist_reader(observed):
    for line in observed:
        found = re.search("^[^\s]+\t([0-9]+)\t[^\s]\t([AGCT]+)\t([AGCT]+)", line)
        yield int(found.group(1)), found.group(2), found.group(3), line


def compare_observed(observed_vcf, ground_truth):
    if isinstance(observed_vcf, str):
        observed_reader = vcf_reader(observed_vcf)
    else:
        observed_reader = vclist_reader(observed_vcf)
    all_count = 0
    found_count = 0
    lengths = list()
    segment_length = 0
    not_found = []
    while True:
        try:
            position, _, to_acid, line = next(observed_reader)
            all_count += 1
            found = ground_truth.get((position, to_acid), 0)
            found_count += found
            if found > 0:
                segment_length += 1
            else:
                if segment_length > 0:
                    lengths.append(segment_length)
                segment_length = 0
                not_found.append(line)
        except(StopIteration):
            if segment_length > 0:
                lengths.append(segment_length)
            break
    if len(lengths) == 0:
        lengths.append(0)
    if all_count == 0:
        percent = 0
    else:
        percent = found_count/float(all_count)
    return found_count, all_count, lengths, not_found, percent


def main(ground_truth_vcf, observed_vcf, homoeolog_vcf, homolog_vcf):
    ground_truth = read_truth(ground_truth_vcf)
    found_count, all_count, lengths, not_found, percent = compare_observed(observed_vcf, ground_truth)
    summary_str = ""
    summary_str = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(ground_truth_vcf,
                                           observed_vcf,
                                           found_count,
                                           all_count,
                                           round(percent, 4),
                                                     min(lengths),
                                                     max(lengths),
                                                     int(round(np.median(lengths), 1)),
                                                     int(round(np.mean(lengths), 1)))
    with(open("polymorph_lengths.tsv", 'a')) as len_file:
        for length in lengths:
            if length > 0:
                len_file.write("{0}\thaplotype\n".format(length))


    if args.homolog:
        homolog = read_truth(homolog_vcf)
        found_count, all_count, lengths, not_in_homolog, percent = compare_observed(not_found, homolog)
        summary_str += "\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(homolog_vcf,
                                                                   found_count,
                                                                   all_count,
                                                                   round(percent, 4),
                                                                   min(lengths),
                                                                   max(lengths),
                                                                   round(np.median(lengths), 1),
                                                                   round(np.mean(lengths), 1))
        with(open("polymorph_lengths.tsv", 'a')) as len_file:
            for length in lengths:
                if length > 0:
                    len_file.write("{0}\thomolog\n".format(length))

    if args.homoeolog:
        homoeolog = read_truth(homoeolog_vcf)
        found_count, all_count, lengths, not_in_homoeolog, percent = compare_observed(not_in_homolog, homoeolog)
        summary_str += "\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(homoeolog_vcf,
                                                                         found_count,
                                                                         all_count,
                                                                         round(percent, 4),
                                                                         min(lengths),
                                                                         max(lengths),
                                                                         round(np.median(lengths), 1),
                                                                         round(np.mean(lengths), 1))
        with(open("polymorph_lengths.tsv", 'a')) as len_file:
            for length in lengths:
                if length > 0:
                    len_file.write("{0}\thomoeolog\n".format(length))

    print(summary_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ground_truth")
    parser.add_argument("observed")
    parser.add_argument("--homoeolog", dest="homoeolog")
    parser.add_argument("--homolog", dest="homolog")
    args = parser.parse_args()
    #print(args)
    main(args.ground_truth, args.observed, args.homoeolog, args.homolog)