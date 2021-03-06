#!/usr/bin/python

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="""
    
    python int_to_float.py expr_file
""")

    parser.add_argument('expr_file')
    #parser.add_argument('-o', '--options', default='yo',
    #					 help="Some option", type='str')
    #parser.add_argument('-u', '--useless', action='store_true', 
    #					 help='Another useless option')

    args = parser.parse_args()

    if args.expr_file == '-':
        f = sys.stdin
    else:
        f = open(args.expr_file, 'r')

    for line in f:
        parts = line.strip().split('\t')
        new_parts = []
        for part in parts:
            try:
                ipart = int(part)
                new_parts += [float(part)]
            except ValueError:
                new_parts += [part]
        try:
            print("\t".join(map(str,new_parts)))
        except IOError:
            continue
    

if __name__ == '__main__':
    main()


