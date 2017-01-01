#!/usr/bin/python

import itertools as it
import pandas as pd
import numpy as np
import scipy.stats as ss
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="""
    
    python maximum_spanning_correlations.py values_matrix 

    Calculate a graph of correlations. The rows of the values_matrix are the nodes
    and the columns are the samples
""")

    parser.add_argument('matrix_file')
    #parser.add_argument('-o', '--options', default='yo',
    #					 help="Some option", type='str')
    #parser.add_argument('-u', '--useless', action='store_true', 
    #					 help='Another useless option')
    parser.add_argument('-d', '--delimiter', default=None)
    parser.add_argument('--header', 
            help='Input line to use as the header', default=None)
    parser.add_argument('--head', help="Take the first n lines", 
            default=None, type=int)

    args = parser.parse_args()

    # headers?
    if args.header is not None:
        matrix = pd.read_csv(args.matrix_file,args.header, delimiter=args.delimiter)
    else:
        matrix = pd.read_csv(args.matrix_file,delimiter=args.delimiter)

    # crop the matrix?
    if args.head is not None:
        matrix = matrix.head(args.head)

    print "matrix:", len(matrix.head().iloc[0].values[1:])

    corrs = []

    for i,j in it.combinations(range(len(matrix)), r=2): 
        # skip the first column, which contains identifiers
        row1 = matrix.iloc[i].values
        row2 = matrix.iloc[j].values

        corr = ss.stats.pearsonr(row1[1:], row2[1:])

        if not np.isnan(corr[0]):
            corrs += [(corr[0], row1[0], row2[0])]

        print "corrs:", sorted(corrs, key=lambda x: -x[0])

if __name__ == '__main__':
    main()


