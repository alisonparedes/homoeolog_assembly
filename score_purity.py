import argparse


def read_tsv(file_name):
    tsv_file = tsv_reader(file_name)
    purity = {}
    while True:
        try:
            haplotype, contig, contig_purity, delta_homoeolog, delta_homolog = next(tsv_file)
            global contigs
            if contig_purity > purity.get(contig, 0):
                purity[contig] = (haplotype, contig_purity, delta_homoeolog, delta_homolog)
        except(StopIteration):
            break
    return purity


def tsv_reader(file_name):
    with open(file_name) as tsv_file:
        for line in tsv_file:
            if line[0] == "h":
                pass
            else:
                data = line.split("\t")
                haplotype = data[0]
                contig = data[1]
                matched_total_percent = data[4]
                delta_homolog = data[10]
                delta_homoeolog = data[18]
                yield haplotype, contig, float(matched_total_percent), int(delta_homoeolog), int(delta_homolog)


def score(purity):
    impurity = 0.0
    sum_homoeolog = 0
    sum_homolog = 0
    for contig, (haplotype, contig_purity, delta_homoeolog, delta_homolog) in purity.iteritems():
        print("{0}\t{1}\t{2}\t{3}\t{4}".format(haplotype, contig, contig_purity, delta_homoeolog, delta_homolog))
        if contig_purity < 1:
            impurity += 1
        sum_homoeolog += delta_homoeolog
        sum_homolog += delta_homolog
    delta = ""
    if sum_homoeolog > sum_homolog:
        delta = "homoeolog"
    elif sum_homolog > sum_homoeolog:
        delta = "homolog"
    else:
        delta = "tie"
    return impurity / len(purity), delta, max(sum_homoeolog, sum_homolog)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv")
    args = parser.parse_args()

    print("haplotype\tcontig\tpurity_pct\tdelta_homoeolog\tdelta_homolog")
    purity = read_tsv(args.tsv)
    impurity, explained_by, delta = score(purity)
    print("IMPURITY: {0} DELTA: {1} ({2})".format(impurity, explained_by, delta))

