import os
import sys
import random
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("root_file")
    args = parser.parse_args()
    report_id = random.randint(0,1000)

    os.system("source activate mcbs913_2018")

    for line in sys.stdin:
        contig_file = line.strip()

        command = "cat {0} lambdaphage.fna | muscle -out ref_{0}.fa".format(contig_file)
        print(command, file=sys.stderr)
        os.system(command)

        command = "csplit --prefix ref_{0}_ ref_{0}.fa ".format(contig_file)
        command += "'/>/' '{*}'"
        print(command, file=sys.stderr)
        os.system(command)

        command = "python3 /home/mcbs913_2018/shared/homoeologs_assembly/homoeolog_assembly/compare_fasta.py {1}_{0}_01 ref_{0}.vcf".format(contig_file, args.root_file)
        print(command, file=sys.stderr)
        os.system(command)