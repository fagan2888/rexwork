#!/usr/bin/python

import argparse
import itertools as it
import json
import pandas as pd
import numpy as np
import sklearn.manifold as sklm
import sys

def main():
    parser = argparse.ArgumentParser(description="""
    
    python tsne.py expression_matrix

    Calculate the t-SNE clustering of the values in the matrix
    file.
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

    #print "matrix:", len(matrix.head().iloc[0].values[1:])

    #print >>sys.stderr, "head:", matrix.head().values[:,1:]
    mvalues = matrix.values[:,1:]
    model = sklm.TSNE(metric='cosine')

    print >>sys.stderr, "values:", mvalues

    f = model.fit_transform(mvalues)
    print >>sys.stderr, "f:", f
    

if __name__ == '__main__':
    main()


