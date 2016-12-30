#!/usr/bin/python

from __future__ import print_function

import argparse
import os.path as op
import pandas as pd
import sys

def filename_only(filepath):
    '''
    Extract the filename without the directory and extensions.

    Args:
        filepath (str): The full filepath of the file

    Returns:
        filename (str): The filename withouth the directory and extension
    '''
    return op.splitext(op.basename(filepath))[0]

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
    print("args.filenames[0]", args.filenames[0], file=sys.stderr)
    table = pd.read_csv(args.filenames[0], compression='gzip', sep=args.sep, header=None)
    table.rename(columns={1: filename_only(args.filenames[0])}, inplace=True)

    for filename in args.filenames[1:]:
        table = table.merge(pd.read_csv(filename, sep=args.sep, header=None),
                left_on=0, right_on=0, how='inner')
        table.rename(columns={1: filename_only(filename)}, inplace=True)

    for column in table.columns[1:]:
        table[column] = table[column].astype(float)

    table.rename(columns={table.columns[0]: 'gene'}, inplace=True)

    out = table.to_csv(sep='\t')
    print(out)

if __name__ == '__main__':
    main()


