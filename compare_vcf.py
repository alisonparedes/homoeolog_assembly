import argparse
import re

ground_truth = {}

def vcf_reader(vcf_file_name):
    with open(vcf_file_name, 'r') as vcf_file:
        for line in vcf_file:
            if line[0] == '#':
                pass
            else:
                found = re.search("^[^\s]+\t([0-9]+)\t[^\s]\t([AGCT]+)\t([AGCT]+)", line)
                yield int(found.group(1)), found.group(2), found.group(3)

def main(ground_truth_vcf, observed_vcf):
    truth_reader = vcf_reader(ground_truth_vcf)
    global ground_truth
    while True:
        try:
            position, _, to_acid = next(truth_reader)
            ground_truth[(position, to_acid)] = 1
        except(StopIteration):
            break
    observed_reader = vcf_reader(observed_vcf)
    all_count = 0
    found_count = 0
    while True:
        try:
            position, _, to_acid = next(observed_reader)
            all_count += 1
            found_count += ground_truth.get((position, to_acid), 0)
        except(StopIteration):
            break
    print("{0}\t{1}\t{2}\t{3}\t{4}\n".format(ground_truth_vcf,
                                             observed_vcf,
                                             found_count,
                                             all_count,
                                             round(found_count/float(all_count), 4)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ground_truth")
    parser.add_argument("observed")
    args = parser.parse_args()
    #print(args)
    main(args.ground_truth, args.observed)