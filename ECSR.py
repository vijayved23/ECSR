import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def displayGraph(x_arr, p_arr, i_arr):
    print("x_arr = {}".format(x_arr))
    print("p_arr = {}".format(p_arr))
    print("i_arr = {}".format(i_arr))

def addEdge(p1, p2, w, perm_verts, perm_edges, buffer):
    global perm_verts_len
    if p1 in perm_verts and p2 in perm_verts:
        buffer[perm_verts[p1]].append((perm_verts[p2], w))
        buffer[perm_verts[p2]].append((perm_verts[p1], w))
    if p1 not in perm_verts and p2 in perm_verts:
        buffer[perm_verts[p2]].append((perm_verts[p1],w))
        buffer[perm_verts_len].append((perm_verts[p2], w))
        perm_verts[p1] = perm_verts_len
        perm_verts_len += 1 
    if p2 not in perm_verts and p1 in perm_verts:
        perm_verts[p2] = perm_verts_len
        buffer[perm_verts[p1]].append((perm_verts[p2] ,w))
        buffer[perm_verts_len].append((perm_verts[p1], w))
        
        perm_verts_len += 1 
    if p2 not in perm_verts and p1 not in perm_verts:
        buffer[perm_verts_len].append((perm_verts[p1], w))
        perm_verts[p1] = perm_verts_len
        perm_verts_len += 1 
        buffer[perm_verts_len].append((perm_verts[p2], w))
        perm_verts[p2] = perm_verts_len
        perm_verts_len += 1 

def addVertex(p1, perm_verts, buffer):
    global perm_verts_len
    if p1 in perm_verts:
        print("Point already in graph")
    else:
        #buffer[perm_verts_len] = p1
        perm_verts[p1] = perm_verts_len
        perm_verts_len += 1


def pushToGraph(buffer, perm_verts, perm_edges):
    edgesToPush = []
    perm_verts_flipped = {}
    for key in perm_verts:
        perm_verts_flipped[perm_verts[key]] = key
    i = 0
    for key in buffer:
        for edge in buffer[key]:
            print(edge)
            if key > edge[0]:
                edgesToPush.append((key, edge[0], edge[1] ))
    print(edgesToPush)
        #print(perm_verts.get(key), buffer[key[1]], buffer[key[2]])
        #perm_edges[perm_verts[key], buffer[key[1]]] = buffer[key[2]]
    
    for edges in edgesToPush:
        perm_edges[(perm_verts_flipped[edges[0]],perm_verts_flipped[edges[1]] )] = edges[2]
    print(perm_edges)

def graph(perm_edges):
    G = nx.Graph()
    for key in perm_edges:
        #print([key[1]])
        G.add_edge(key[0],key[1], weight=perm_edges[key])
    #print(G.edges(data=True))
    nx.draw_networkx(G)
    plt.show()

def edgeWeightFinder(perm_edges, n):
    print("The edges that have a weight greater than", n, "are: ")
    for key in perm_edges:
        if perm_edges[key] >= n:
            print(key)

def removeVertex(v, perm_verts, perm_edges, p_arr, x_arr, i_arr):
    for key in perm_verts.copy():
        if key == v:
            # print("Key matches")
            indStart = p_arr[perm_verts[v]]
            indEnd = p_arr[perm_verts[v]+1]

            for i in range(indStart,indEnd):
                x_arr[i] = -1
                i_arr[i] = -1
                p_arr[perm_verts[v]] = -1

            del perm_verts[key]

    for key in perm_edges.copy():
        if v in key:
            del perm_edges[key]

def removeEdge(u, v, perm_edges, perm_verts, p_arr, i_arr, x_arr):
    perm_verts_flipped = {}
    for key in perm_verts:
        perm_verts_flipped[perm_verts[key]] = key

    for key in perm_edges.copy():
        try:
            u_start = p_arr[perm_verts[u]]
            u_end = p_arr[perm_verts[u] + 1]

            v_start = p_arr[perm_verts[v]]
            v_end = p_arr[perm_verts[v] + 1]

            for i in range(u_start, u_end):
                if perm_verts_flipped[i] == v:
                    i_arr[i] = -1
                    x_arr[i] = -1

            for i in range(v_start, v_end):
                if perm_verts_flipped[i] == u:
                    i_arr[i] = -1
                    x_arr[i] = -1

            if u in key and v in key:
                del perm_edges[key]
        except:
            u_ind = p_arr[perm_verts[u]]
            v_ind = p_arr[perm_verts[v]]

            while i_arr[u_ind] != -1:
                if perm_verts_flipped[u_ind] == v:
                    i_arr[u_ind] = -1
                    x_arr[u_ind] = -1
                u_ind += 1

            while i_arr[v_ind] != -1:
                if perm_verts_flipped[v_ind] == u:
                    i_arr[v_ind] = -1
                    x_arr[v_ind] = -1
                v_ind += 1


        ## THINK ABOUT: how do we handle lonely vertices with no friends? :(
        ## THINK ABOUT: how do we handle p_arr during deletions?

def updateCSR( p_arr, i_arr, x_arr, perm_verts, perm_edges):
    index = 0
    for key1 in perm_verts:
        p_arr[perm_verts[key1]] = index
        for key2 in perm_edges:
            if key1 in key2:
                if key1 == key2[0]:
                    i_arr[index] = perm_verts[key2[1]]
                    x_arr[index] = perm_edges[key2]
                else:
                    i_arr[index] = perm_verts[key2[0]]
                    x_arr[index] = perm_edges[key2]
                index += 1

def main():
    # Intialize.
    size = 10
    size_buffer = 5
   
    # Keep in mind: don't run out of indices for the perm array.
    perm_verts = {"A" : 0, "B" : 1, "C" : 2}
    perm_edges = {("A", "B") : 9, ("A", "C") : 8, ("B", "C") : 5}
    
    global perm_verts_len
    perm_verts_len = len(perm_verts)
   # addVertex("D", perm_verts)
    #addEdge("C", "D", 5, perm_verts, perm_edges)
    #addEdge("B", "D", 10, perm_verts, perm_edges)
    
    # Keep in mind: resizing of arrays might occur.
    p_arr = [-1] * size
    i_arr = [-1] * (size * 2)
    x_arr = [-1] * (size * 2)

    # Initialize p_arr, i_arr, and x_arr.
    index = 0
    for key1 in perm_verts:
        p_arr[perm_verts[key1]] = index
        for key2 in perm_edges:
            if key1 in key2:
                if key1 == key2[0]:
                    i_arr[index] = perm_verts[key2[1]]
                    x_arr[index] = perm_edges[key2]
                else:
                    i_arr[index] = perm_verts[key2[0]]
                    x_arr[index] = perm_edges[key2]
                index += 1



    # Initialize insert buffer.
    buffer = {}
    for i in range(20):
        buffer[i] = []
    #init_list = [-1] * size_buffer

    #for i in range(size):
    #    buffer.append(init_list.copy())

    #print("buffer = {}".format(buffer))

    # Add Edge
  
    
    print(perm_verts)
    displayGraph(x_arr, p_arr, i_arr)
    addEdge("B", "C", 5, perm_verts, perm_edges, buffer)
    addEdge("C", "D", 2, perm_verts, perm_edges, buffer)
    addVertex("E", perm_verts, buffer)
    addEdge("D", "E", 3, perm_verts, perm_edges, buffer)
    addVertex("F", perm_verts, buffer)
    addEdge("E", "F", 6, perm_verts, perm_edges, buffer)
    addEdge("D", "E", 14, perm_verts, perm_edges, buffer)
    addEdge("E", "C", 5, perm_verts, perm_edges, buffer )
    
    print(buffer)
    print(perm_verts)
    print(perm_edges)
    pushToGraph(buffer, perm_verts, perm_edges)
    #print("GRAPH")
    #edgeWeightFinder(perm_edges, 6)
    
    #print("REMOVING A VERTEX:")
    #removeVertex("A", perm_verts, perm_edges, p_arr, x_arr, i_arr)
    #displayGraph(x_arr, p_arr, i_arr)
    #print(perm_verts)
    #print(perm_edges)

    print()

    #print("REMOVING AN EDGE:")
    #removeEdge("B", "C", perm_edges, perm_verts, p_arr, i_arr, x_arr)
    #displayGraph(x_arr, p_arr, i_arr)
    #print(perm_verts)
    #print(perm_edges)

    graph(perm_edges)
    updateCSR(p_arr, i_arr, x_arr, perm_verts, perm_edges)

    displayGraph(x_arr, p_arr, i_arr)
#main()  

if __name__ == "__main__":
    main()
    
