import os
import sys
import random
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ref_file")
    args = parser.parse_args()

    for line in sys.stdin:
        contig_file = line.strip()
        os.system("cat {0} lambdaphage.fna | muscle -out ref_contig01.fa".format(contig_file))
        command = "csplit --prefix ref_{0}_ ref_{0}.fa \"/>/\" \"{*}\"".format(contig_file)
        print(command)
        os.system(command)
        os.system("python compare_fasta.py lambdaphage.fna ref_{0}_01 ref_{0}.vcf".format(contig_file))
        report_id = random.randint(0,1000)
        os.system("touch {0}_assembly_quality_{1}.tsv".format(args.ref_file, report_id))
        for i in range(1, 4):
            os.system("python compare_vcf.py {0}_0{1}.vcf ref_{1}.vcf >> {0}assembly_quality_{2}.tsv".format(args.ref_file, i, contig_file))