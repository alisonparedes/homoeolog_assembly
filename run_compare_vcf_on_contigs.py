import os
import sys


def read_contigs():
    for line in sys.stdin:
        yield line.rstrip()


if __name__ == "__main__":
    contigs = read_contigs()
    header = "haplotype\tcontig\tfound\tall\tpercent\tminlen\tmaxlen\tmedlen\tavglen\thomoeolog\tdlthefound\tdltheall"
    header += "\tdlthepercent\tdltheminlen\tdlthemaxlen\tdlthemedlen\tdltheavglen\thomolog\tdlthofound\tdlthoall"
    header += "\tdlthopercent\tdlthominlen\tdlthomaxlen\tdlthomedlen\tdlthoavglen"
    print(header)
    while True:
        try:
            contig = next(contigs)
            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "lambda_diploid_snp05_01.vcf {0}".format(contig)
            command += " --homoeolog lambda_diploid_snp05_02.vcf"
            command += " --homolog lambda_diploid_snp05_03.vcf "
            os.system(command)

            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "lambda_diploid_snp05_02.vcf {0}".format(contig)
            command += " --homoeolog lambda_diploid_snp05_01.vcf"
            command += " --homolog lambda_diploid_snp05_04.vcf "
            os.system(command)

            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "lambda_diploid_snp05_03.vcf {0}".format(contig)
            command += " --homoeolog lambda_diploid_snp05_02.vcf"
            command += " --homolog lambda_diploid_snp05_01.vcf "
            os.system(command)

            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "lambda_diploid_snp05_04.vcf {0}".format(contig)
            command += " --homoeolog lambda_diploid_snp05_01.vcf"
            command += " --homolog lambda_diploid_snp05_02.vcf "
            os.system(command)

        except StopIteration:
            break
    exit(0)