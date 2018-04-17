def compare_fasta(name_file_a, name_file_b, vcf_file_name):

    name = ''

    with open(name_file_a, 'r') as file_a:
        with open(name_file_b, 'r') as file_b:

            for line_a in file_a:
                if line_a[0] == '>':
                    line_b = file_b.readline()
                    find_name = re.search("^>([^\s]+)\s", line_a)
                    name = find_name.group(1)
                    with open(vcf_file_name, 'w') as vcf_file:
                        vcf_file.write("##fileformat=VCFv4.0\n")
                        vcf_file.write("##fileDate=20180329\n")
                        vcf_file.write("##reference=lambdaphage\n")
                        vcf_file.write("##phasing=partial\n")
                        vcf_file.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

                else:  # genome
                    line_b = file_b.readline()
                    i = 0
                    while i < len(line_a):
                        if line_a[i] != line_b[i]:

                            with open(vcf_file_name, 'a') as vcf_file:
                                vcf_file.write("{0}\t{1}\t.\t{2}\t.\tPASS\t.{3}\n".format(name, i+1, line_a[i], line_b[i]))
                        i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("contig")
    parser.add_argument("ref")
    praser.add_argument("vcf")
    args = parser.parse_args()
    print(args)
    compare_fasta(args.ref, args.contig, args.vcf)