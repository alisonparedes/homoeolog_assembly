import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", dest="quast_dir", default="latest")
    args = parser.parse_args()
    print(args)