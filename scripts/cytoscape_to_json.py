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
    parser.add_argument('-w', '--weight-filter', default=None, type=float)
    parser.add_argument('-s', '--sample-edges', default=None, type=int,
            help="Sample only n edges from the entire set")
    parser.add_argument('-n', '--sample-nodes', default=None, type=int,
            help="Sample only n nodes from the entire set")

    args = parser.parse_args()

    edges = pd.read_csv(args.edges_file, sep='\t')
    edge_columns = {'fromNode': 'source', 'toNode': 'target', 'weight': 'value'}
    edges.rename(columns=edge_columns, inplace=True)

    nodes = pd.read_csv(args.nodes_file, sep='\t')
    nodes.columns = ['id', 'name', 'color']

    print >>sys.stderr, edges.head()

    if args.sample_nodes is not None:
        nodes = nodes.sample(args.sample_nodes)

    print >>sys.stderr, "nodes", nodes.head()
    node_ids = set(nodes['id'])

    #print >>sys.stderr, [e in node_ids for e in edges['source'].values]

    edges = edges[[e in node_ids for e in edges['source'].values]]
    edges = edges[[e in node_ids for e in edges['target'].values]]

    print >>sys.stderr, "edges:", edges


    nodes['name'] = nodes['id']

    if args.sample_edges is not None:
        edges = edges.sample(args.sample_edges)


    if args.weight_filter is not None:
        edges = edges[edges['value'] > args.weight_filter]

    print ('{"nodes":' +  nodes.to_json(orient='records') + "," +
            '"links":'  + edges[edge_columns.values()].to_json(orient='records') + '}')
    print >>sys.stderr, "Num nodes:", len(nodes.index), "Num edges:", len(edges.index)
    

if __name__ == '__main__':
    main()


