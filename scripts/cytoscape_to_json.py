#!/usr/bin/python

import json
import pandas as pd
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="""
    
    python cytoscape_to_json.py nodes_file edges_file

    Example nodes file:

    nodeName        altName nodeAttr.nodesPresent...
    MMT00000159     Cdc2a   red
    MMT00000793     C330027C09Rik   red
    MMT00000840     Col5a3  red

    Example edges file:

    nodeName        altName nodeAttr.nodesPresent...
    MMT00000159     Cdc2a   red
    MMT00000793     C330027C09Rik   red

""")

    parser.add_argument('nodes_file')
    parser.add_argument('edges_file')

    #parser.add_argument('argument', nargs=1)
    #parser.add_argument('-o', '--options', default='yo',
    #					 help="Some option", type='str')
    #parser.add_argument('-u', '--useless', action='store_true', 
    #					 help='Another useless option')

    args = parser.parse_args()

    nodes = pd.read_csv(args.nodes_file, sep='\t')
    nodes.columns = ['id', 'name', 'color']

    edge_columns = {'fromNode': 'source', 'toNode': 'target', 'weight': 'value'}

    edges = pd.read_csv(args.edges_file, sep='\t')
    edges.rename(columns=edge_columns, inplace=True)
    edges['value'] *= 100

    print ('{"nodes":' +  nodes.to_json(orient='records') + "," +
            '"links":'  + edges[edge_columns.values()].to_json(orient='records') + '}')
    

if __name__ == '__main__':
    main()


