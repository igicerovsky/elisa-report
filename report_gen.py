import sys
import argparse

import readdata
from fitdata import fit_magic
from readdata import read_concat_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--xlsdata", help="xls data path", default='C:/work/report-gen/data/sample_data.xlsx')
    parser.add_argument("-f", "--fitdata", help="csv data path", default='C:/work/report-gen/data/fit_0.csv')
    args = parser.parse_args()

    data = read_concat_data(args.xlsdata)

    fit_magic(args.fitdata)


if __name__ == "__main__":
    main()
