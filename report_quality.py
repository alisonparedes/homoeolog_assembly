import os
import sys
import random
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("ref_file")
    args = parser.parse_args()
    report_id = random.randint(0,1000)

    os.system("source activate mcbs913_2018")

    os.system("touch {0}_assembly_quality_{1}.tsv".format(args.ref_file, report_id))

    for line in sys.stdin:
        contig_file = line.strip()

        command = "cat {0} lambdaphage.fna | muscle -out ref_{0}.fa".format(contig_file)
        print(command)
        os.system(command)

        print(command)
        command = "csplit --prefix ref_{0}_ ref_{0}.fa ".format(contig_file)
        command += "'/>/' '{*}'"
        os.system(command)

        command = "python homoeolog_assembly/compare_fasta.py lambdaphage.fna ref_{0}_01 ref_{0}.vcf".format(contig_file)
        print(command)
        os.system(command)

        for i in range(1, 5):
            command = "python homoeolog_assembly/compare_vcf.py {0}_0{1}.vcf ref_{2}.vcf >> {0}_assembly_quality_{3}.tsv".format(args.ref_file, i, contig_file, report_id)
            print(command)
            os.system(command)
