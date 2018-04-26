import argparse


def read_tsv(file_name):
    tsv_file = tsv_reader(file_name)
    purity = {}
    while True:
        try:
            haplotype, contig, contig_purity = next(tsv_file)
            global contigs
            if contig_purity > purity.get(contig, 0):
                purity[contig] = contig_purity
        except(StopIteration):
            break
    return purity


def tsv_reader(file_name):
    with open(file_name) as tsv_file:
        for line in tsv_file:
            haplotype, contig, matched, total, matched_total_percent = line.split("\t")
            yield haplotype, contig, float(matched_total_percent)


def score(purity):
    impurity = 0.0
    for contig, contig_purity in purity.iteritems():
        print("{0}\t{1}".format(contig, contig_purity))
        if contig_purity < 1:
            impurity += 1
    return impurity / len(purity)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv")
    args = parser.parse_args()

    purity = read_tsv(args.tsv)
    print("IMPURITY: {0}".format(score(purity)))

