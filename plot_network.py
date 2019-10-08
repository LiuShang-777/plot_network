# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:11:27 2019

@author: liushang
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import warnings
warnings.filterwarnings('ignore')
parser=argparse.ArgumentParser(description=
                               'network visualization plot')
parser.add_argument('-nf','--nodes_file',type=str,help='the path of file containing nodes\'s names')
parser.add_argument('-ef','--edges_file',type=str,help='the path of edges file containing edges\' names')
parser.add_argument('-ncf','--node_color_file',type=str,help='the path of nodes color file')
parser.add_argument('-ecf','--edge_color_file',type=str,help='the path of edges color file')
parser.add_argument('-ewf','--edges_weight_file',type=str,help='the path of weighted edges file')
parser.add_argument('-pf','--position_file',type=str,help='the path of position file')
parser.add_argument('-gc','--graph_class',type=str,help='the type of graph :directed or nondirected',choices=['nd','d'])
parser.add_argument('-gl','--graph_layout',type=str,help='the type of layout of graph',choices=['circle','random','spring','spectral','shell'])
parser.add_argument('-rf','--result_file',type=str,help='the result file')
parser.add_argument('-ew','--edge_weight',type=str,help='weighted edges or not',choices=['yes','no'])
args=parser.parse_args()
nodes_file=args.nodes_file
edges_file=args.edges_file
node_color_file=args.node_color_file
edge_color_file=args.edge_color_file
edges_weight_file=args.edges_weight_file
position_file=args.position_file
graph_class=args.graph_class
graph_layout=args.graph_layout
result_file=args.result_file
if args.edge_weight=='yes':    
    edge_weight=1
else:
    edge_weight=0
def get_colors(color_file):    
    with open(color_file) as file:
        color_list=[]
        for line in file:
            line=line.strip()
            color_list.append(line)
    return color_list
def fill_color(items,colors):
    color=[]
    for i,j in zip(items,colors):
            color.append(j)
    return color
def get_nodes(nodes_file):
    with open(nodes_file,'r') as file:
        nodes_line=[]
        for line in file:
            line=line.strip()
            nodes_line.append(line)
    return nodes_line
nodes=get_nodes(nodes_file)
print('nodes file has been loaded')
if node_color_file!=None:  
    node_color_list=get_colors(node_color_file)
    if len(node_color_list)!=len(nodes):
        exit('the type of nodes\' color isn\'t consistent with class of nodes ')
    node_colors=fill_color(nodes,node_color_list)
    print('the color list has been loaded')
else:
    node_colors=None
def get_edges_without_weight(edges_file):
    edges_list=[]
    with open(edges_file,'r') as file:
        for line in file:
            line=line.strip()
            edges_list.append((line.split('\t')[0],line.split('\t')[1]))
    return edges_list   
def get_edges_with_weight(edges_weight_file):
    edges_list=[]
    with open(edges_weight_file,'r') as file:    
        for line in file:
            line=line.strip()           
            edges_list.append((line.split('\t')[0],line.split('\t')[1],float(line.split('\t')[2])))
    return edges_list
if bool(edge_weight):  
    edges_with_weight=get_edges_with_weight(edges_weight_file)
    print('eighted nodes has been loaded')
else:
    edges_with_weight=get_edges_without_weight(edges_file)
    print('nodes without weight has been loaded')
if edge_color_file!=None: 
    edge_color_list=get_colors(edge_color_file)
    if len(edge_color_list)!=len(edges_with_weight):
        exit('the type of edges\' color isn\'t consistent with class of edges ')
    edge_colors=fill_color(edges_with_weight,edge_color_list)
else:
    edge_colors=None
if graph_class=='nd':   
    fg=nx.Graph()
elif graph_class=='d':    
    fg=nx.MultiDiGraph()
else:
    exit('the type of network only has two choices:nd and d')
def add_nodes(fg,items):
        fg.add_nodes_from(items)
def add_edges(fg,items):
    global graph_class
    if edge_weight:
            fg.add_weighted_edges_from(items)
    else:
            fg.add_edges_from(items)
add_nodes(fg,nodes)
add_edges(fg,edges_with_weight)
fig=plt.figure(figsize=(8,6))
if (node_colors!=None)&(edge_colors!=None):    
    if position_file!=None:    
        def get_pos(position_file):
            with open(position_file,'r') as file:
                position={}
                for line in file:
                    line=line.strip()
                    position[line.split(':')[0]]=(int(line.split(':')[1]),int(line.split(':')[2]))
            return position
        position=get_pos(position_file)
        nx.draw(fg,with_labels=True,node_color=node_colors,edge_color=edge_colors,pos=position)
    else:
        position=graph_layout
        if position=='spring':       
            nx.draw(fg,with_labels=True,node_color=node_colors,edge_color=edge_colors,pos=nx.spring_layout(fg))
        elif position=='circle':
            nx.draw(fg,with_labels=True,node_color=node_colors,edge_color=edge_colors,pos=nx.circular_layout(fg))
        elif position=='random':
            nx.draw(fg,with_labels=True,node_color=node_colors,edge_color=edge_colors,pos=nx.random_layout(fg))
        elif position=='shell':
            nx.draw(fg,with_labels=True,node_color=node_colors,edge_color=edge_colors,pos=nx.shell_layout(fg))
        elif position=='spectral':
            nx.draw(fg,with_labels=True,node_color=node_colors,edge_color=edge_colors,pos=nx.spectral_layout(fg))
        else:
            exit('the lay out could only in five format')
elif (node_colors!=None)&(edge_colors==None):
    if position_file!=None:    
        def get_pos(position_file):
            with open(position_file,'r') as file:
                position={}
                for line in file:
                    line=line.strip()
                    position[line.split(':')[0]]=(int(line.split(':')[1]),int(line.split(':')[2]))
            return position
        position=get_pos(position_file)
        nx.draw(fg,with_labels=True,node_color=node_colors,pos=position)
    else:
        position=graph_layout
        if position=='spring':       
            nx.draw(fg,with_labels=True,node_color=node_colors,pos=nx.spring_layout(fg))
        elif position=='circle':
            nx.draw(fg,with_labels=True,node_color=node_colors,pos=nx.circular_layout(fg))
        elif position=='random':
            nx.draw(fg,with_labels=True,node_color=node_colors,pos=nx.random_layout(fg))
        elif position=='shell':
            nx.draw(fg,with_labels=True,node_color=node_colors,pos=nx.shell_layout(fg))
        elif position=='spectral':
            nx.draw(fg,with_labels=True,node_color=node_colors,pos=nx.spectral_layout(fg))
        else:
            exit('the lay out could only in five format')
elif (node_colors==None)&(edge_colors!=None):
    if position_file!=None:    
        def get_pos(position_file):
            with open(position_file,'r') as file:
                position={}
                for line in file:
                    line=line.strip()
                    position[line.split(':')[0]]=(int(line.split(':')[1]),int(line.split(':')[2]))
            return position
        position=get_pos(position_file)
        nx.draw(fg,with_labels=True,edge_color=edge_colors,pos=position)
    else:
        position=graph_layout
        if position=='spring':       
            nx.draw(fg,with_labels=True,edge_color=edge_colors,pos=nx.spring_layout(fg))
        elif position=='circle':
            nx.draw(fg,with_labels=True,edge_color=edge_colors,pos=nx.circular_layout(fg))
        elif position=='random':
            nx.draw(fg,with_labels=True,edge_color=edge_colors,pos=nx.random_layout(fg))
        elif position=='shell':
            nx.draw(fg,with_labels=True,edge_color=edge_colors,pos=nx.shell_layout(fg))
        elif position=='spectral':
            nx.draw(fg,with_labels=True,edge_color=edge_colors,pos=nx.spectral_layout(fg))
        else:
            exit('the lay out could only in five format')
else:
    if position_file!=None:    
        def get_pos(position_file):
            with open(position_file,'r') as file:
                position={}
                for line in file:
                    line=line.strip()
                    position[line.split(':')[0]]=(int(line.split(':')[1]),int(line.split(':')[2]))
            return position
        position=get_pos(position_file)
        nx.draw(fg,with_labels=True,pos=position)
    else:
        position=graph_layout
        if position=='spring':       
            nx.draw(fg,with_labels=True,pos=nx.spring_layout(fg))
        elif position=='circle':
            nx.draw(fg,with_labels=True,pos=nx.circular_layout(fg))
        elif position=='random':
            nx.draw(fg,with_labels=True,pos=nx.random_layout(fg))
        elif position=='shell':
            nx.draw(fg,with_labels=True,pos=nx.shell_layout(fg))
        elif position=='spectral':
            nx.draw(fg,with_labels=True,pos=nx.spectral_layout(fg))
        else:
            exit('the lay out could only in five format')
plt.savefig(result_file,bbox_inches='tight',figsize=(8,6))
plt.clf()
print('>===the network has been finished===<')