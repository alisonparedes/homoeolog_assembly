import os
import sys


def read_contigs():
    for line in sys.stdin:
        yield line


if __name__ == "__main__":
    contigs = read_contigs()
    while True:
        try:
            contig = next(contigs)
            command = "python /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_vcf.py "
            command += "lambda_diploid_snp05_01.vcf {0} --homolog lambda_diploid_snp05_03.vcf --homoeolog lambda"
            print(command)
            os.system(command)
        except StopIteration:
            break