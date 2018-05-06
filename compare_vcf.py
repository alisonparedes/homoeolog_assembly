import argparse
import re
import sys


def vcf_reader(vcf_file_name=sys.stdin):
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
    global out_file_name
    global relationship
    global ground_truth_name
    with(open(out_file_name, 'w')) as out_file:
        observed_reader = vcf_reader()
        all_count = 0
        found_count = 0
        segment_length = 0
        while True:
            try:
                position, _, to_acid, line = next(observed_reader)
                out_prefix = "{0}\t{1}\t{2}".format(position, ground_truth_name, relationship)
                all_count += 1
                found = ground_truth.get((position, to_acid), 0)
                found_count += found
                if found > 0:
                    segment_length += 1
                else:  # Not found
                    if segment_length > 0:
                        out_file.write("{0}\t{1}\n".format(out_prefix, segment_length))
                    segment_length = 0
                    print(line.strip(), file=sys.stdout, flush=True)
            except StopIteration:
                if segment_length > 0:
                    out_file.write("{0}\t{1]\n".format(out_prefix, segment_length))
                break
        if all_count == 0:
            percent = 0
        else:
            percent = found_count/float(all_count)
    return found_count, all_count, percent


def main(ground_truth_vcf, observed_vcf):
    ground_truth = read_truth(ground_truth_vcf)
    found_count, all_count, percent = compare_observed(observed_vcf, ground_truth)
    summary_str = "{0}\t{1}\t{2}\t{3}".format(ground_truth_vcf,
                                           #observed_vcf,
                                           found_count,
                                           all_count,
                                           round(percent, 4))

    print(summary_str, file=sys.stderr)

out_file_name = "polymorph_lengths.tsv"
relationship = "haplotype"
#contig = None
ground_truth_name = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ground_truth")
    #parser.add_argument("observed")
    parser.add_argument("-o", dest="out_file")
    parser.add_argument("--relationship", dest="relationship")  # Code classifying relationshop of ground truth to homoeolog model, {
    args = parser.parse_args()
    print(args, file=sys.stderr)
    #contig = args.observed
    out_file_name = args.out_file
    ground_truth_name = args.ground_truth
    relationship = args.relationship
    main(args.ground_truth, args.observed)