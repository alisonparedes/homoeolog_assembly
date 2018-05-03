import argparse


def read_tsv(file_name):
    tsv_file = tsv_reader(file_name)
    purity = {}
    while True:
        try:
            haplotype, contig, contig_purity, delta_homoeolog = next(tsv_file)
            global contigs
            if contig_purity > purity.get(contig, (None, 0))[1]:
                purity[contig] = (haplotype, contig_purity, delta_homoeolog)
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
                delta_homoeolog = data[18]
                yield haplotype, contig, float(matched_total_percent), int(delta_homoeolog)


def score(purity):
    impurity = 0.0
    sum_homoeolog = 0
    for contig, (haplotype, contig_purity, delta_homoeolog) in purity.items():
        print("{0}\t{1}\t{2}\t{3}".format(haplotype, contig, contig_purity, delta_homoeolog))
        if contig_purity < 1:
            impurity += 1
        sum_homoeolog += delta_homoeolog
    return impurity / len(purity), sum_homoeolog


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tsv")
    args = parser.parse_args()

    print("haplotype\tcontig\tpurity_pct\tdelta_homoeolog")
    purity = read_tsv(args.tsv)
    impurity, homoeolog = score(purity)
    print("IMPURITY: {0} DELTA: {1}".format(impurity, homoeolog))

