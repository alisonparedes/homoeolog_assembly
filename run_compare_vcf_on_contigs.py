import os
import sys
import argparse


def read_contigs():
    for line in sys.stdin:
        yield line.rstrip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prefix")
    args = parser.parse_args()
    contigs = read_contigs()
    header = "haplotype\tcontig\tfound\tall\tpercent\tminlen\tmaxlen\tmedlen\tavglen\thomoeolog\tdlthefound\tdltheall"
    header += "\tdlthepercent\tdltheminlen\tdlthemaxlen\tdlthemedlen\tdltheavglen\thomolog\tdlthofound\tdlthoall"
    header += "\tdlthopercent\tdlthominlen\tdlthomaxlen\tdlthomedlen\tdlthoavglen"
    print(header)
    while True:
        try:
            contig = next(contigs)
            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "{1}_01.vcf {0}".format(contig, args.prefix)
            command += " --homoeolog {0}_02.vcf".format(args.prefix)
            command += " --homolog {0}_03.vcf".format(args.prefix)
            os.system(command)

            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "{1}_02.vcf {0}".format(contig, args.prefix)
            command += " --homoeolog {0}_01.vcf".format(args.prefix)
            command += " --homolog {0}_04.vcf".format(args.prefix)
            os.system(command)

            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "{1}_03.vcf {0}".format(contig, args.prefix)
            command += " --homoeolog {0}_02.vcf".format(args.prefix)
            command += " --homolog {0}_01.vcf ".format(args.prefix)
            os.system(command)

            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "{1}_04.vcf {0}".format(contig, args.prefix)
            command += " --homoeolog {0}_01.vcf".format(args.prefix)
            command += " --homolog {0}_02.vcf".format(args.prefix)
            os.system(command)

        except StopIteration:
            break
    exit(0)