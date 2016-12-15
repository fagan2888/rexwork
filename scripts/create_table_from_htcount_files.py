#!/usr/bin/python

from __future__ import print_function

import argparse
import pandas as pd
import sys

def main():
    parser = argparse.ArgumentParser(description="""
    
    python create_table_from_htcount_files.py file1.gz ...

    Place the data from a set of files into one table. Each file should have the following format:

    key value

    The resulting table will have the following format

    keys    filename1       filename2
    key1     value1_f1      value1_f2
    key2     value2_f1      value2_f2

""")

    parser.add_argument('filenames', nargs='+')
    parser.add_argument('--sep', help='The separator in each data file')
    #parser.add_argument('-o', '--options', default='yo',
    #					 help="Some option", type='str')
    #parser.add_argument('-u', '--useless', action='store_true', 
    #					 help='Another useless option')

    args = parser.parse_args()

    for filename in args.filenames[:1]:
        table = pd.read_csv(filename, sep=args.sep, header=None)
        print('filename:', filename)
        print('columns:', table.columns)
        print("table.head():", table.head())

if __name__ == '__main__':
    main()


