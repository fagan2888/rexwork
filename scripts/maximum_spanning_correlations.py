#!/usr/bin/python

import argparse
import itertools as it
import json
import pandas as pd
import networkx as nx
import numpy as np
import scipy.stats as ss
import sys

def graph_to_json(G):
    '''
    Dump a networkx graph to JSON.

    Args:

    G (A networkx graph): The graph to be dumped.

    Return:

    dictionary: JSON representation of the graph
    '''
    nodes = [{'id': n} for n in G.nodes()]
    edges = [{'source': f, 'target': t, 'value': w } for (f,t,w) in G.edges(data='corr')]

    return {'nodes': nodes, 'links': edges}


def create_graph_from_corrs(corrs):
    '''
    Create a maximum spanning tree for the list of correlations

    Args:
    
    corrs (list of tuples): (corr, from, to)

    Return:

    A networkx graph
    '''
    G = nx.Graph()
    nodes = set()

    corrs = sorted(corrs, key=lambda x: -x[0])
    print >>sys.stderr, "corrs:", corrs[:10]

    topn = 400
    count = 0
    

    for (corr, from_node, to_node) in corrs:
        if from_node not in nodes or to_node not in nodes:
            # we haven't seen one of the nodes yet, so we add them
            G.add_edge(from_node, to_node, corr=corr)
            nodes.add(from_node)
            nodes.add(to_node)
            continue

        if count < topn:
            count +=1 
            G.add_edge(from_node, to_node)
            continue

        try:
            if nx.bidirectional_dijkstra(G, from_node, to_node):
                # there's already a path between these nodes
                # no need to connect them
                continue
        except:
            pass

        G.add_edge(from_node, to_node, corr=abs(corr))

        if len(list(nx.connected_components(G))) == 1:
            # graph is fully connected, time to go home
            break

    return G

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

    #print "matrix:", len(matrix.head().iloc[0].values[1:])

    corrs = []

    for i,j in it.combinations(range(len(matrix)), r=2): 
        # skip the first column, which contains identifiers
        row1 = matrix.iloc[i].values
        row2 = matrix.iloc[j].values

        corr = ss.stats.pearsonr(row1[1:], row2[1:])

        if not np.isnan(corr[0]):
            corrs += [(corr[0], row1[0], row2[0])]

        #print "corrs:", sorted(corrs, key=lambda x: -x[0])

    G = create_graph_from_corrs(corrs)
    graph_json = graph_to_json(G)
    print json.dumps(graph_json, indent=1)

if __name__ == '__main__':
    main()


