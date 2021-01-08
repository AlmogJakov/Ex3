
# EX3
Object Oriented Course Assignment - Creating and Implementing Directed Weighted Graph Theory.


In this project we were asked to implement an directed weighted graph with the algorithms of Graph Theory.
We will briefly explain the algorithms, the data structures we used and the complexities of the operations.
	
</table>

<table align="center">
	
<h3>Check out Wiki page for comparisons of runtime algorithms & more information</h3>
<tr><td>
<p align="center"><img src="https://github.com/AlmogJakov/Ex3/blob/main/images/plot_300.png"/></p>
</td>
<td> 
<p align="center"><img src="https://github.com/AlmogJakov/Ex3/blob/main/images/stats.png"/></p>
</td></tr>
</table>



<table align="center" width=100%>
<tr width=100%><td>

**Edge weight examples**  
from D to E: 1  
from B to C: 0.3  
from A to F: 0.9  

**Shortest Path examples:**  
**(lowest weight)**  
from B to A:  
B > A > E > F  
from A to D:  
A > E > F > D  

</td>

<td> 
	

```jsonc
Directed Weighted Graph illustration:
```
<p align="center"><img src="https://github.com/itay-rafee/Ex2/raw/main/data/images/dwgraph.png"/></p>

<!--
<p align="center">
<img src="https://github.com/AlmogJakov/AlmogJakov/blob/main/welcome-back-small.gif"/>
</p>
-->

</td></tr>
</table>

<h2> DiGraph Class (Represents a graph): </h2>

In this class we were asked to implement a class representing directed weighted graph
This class represents an directed weighted graph that can contain a very large amount of vertices and for that it is necessary to maintain efficient running time.
To do so there is a need for a data structure where all vertices can be accessed efficiently.
Therefore, the appropriate data structure fo performing operations on a very large list of vertex is dict. 
(such as returning a vertex value, checking neighbors between vertices etc.)

```diff 
@@ self.graph; @@ (for receiving any vertex by key).
``` 
```diff 
@@ self.ni; @@ (for receiving any vertex neighbors as keys while value = weight).
``` 
```diff 
@@ self.revers_ni; @@ (for receiving any vertex reversed neighbors as keys while value = weight).
``` 

The following functions can be performed:
- Return vertex by key - easily done by accessing the '_graph' HashMap in complexity O(1)
- Return edge between 2 vertices - performed by checking the existence of one vertex in the list of neighbors (HashMap) of the other.
- Adding a vertex to a graph - easily done by adding the vertex to each dict.
- Adding an edge to a graph between 2 vertices - done by adding a vertex to the list of neighbors of the other (two directions) with the edge.
- Returns a collection of all vertices of the graph - done by returning 'graph' dict.
- Returns a collection of all the out edges of specific vertex - done by a returning the 'ni' values of the vertex.
- Returns a collection of all the in edges of specific vertex - done by a returning the 'revers_ni' values of the vertex.
- Deleting a vertex from the graph - removing the vertex (after deleting all the edges connected to it).
- Deleting an edge from the graph - done by deleting a vertex from the list of neighbors of the other (two directions).
- Obtaining a numeric variable representing the number of vertices - easily done by the len() function on 'graph' dict.
- Receiving a numeric variable that represents the number of edges - easily done by a direct variable (stored in the class) updated with each operation of adding\deleting 
  an edge to the graph.
- Receiving a numeric variable that represents the number of MC (changes) in the class - easily done by a direct variable (stored in the class) updated with each action 
  of adding\deleting an vertex\edge in the graph or updating edge weight.

<h2></h2>
<h3> NodeData Class (Represents a vertex) [Internal Class of DiGraph Class]: </h3>  
In this class we were asked to implement a class that represents a vertex.  
The following functions can be performed:

- Return the key - easily performed by accessing the appropriate value stored in the object.  
- Return the tag - easily performed by accessing the appropriate value stored in the object.  
- Return the pos - easily performed by accessing the appropriate value stored in the object.  
- Return the DiGraph on which the vertex is associated - easily performed by accessing the appropriate value stored in the object.  


<h2> GraphAlgo Class (Represents the Graph Theory algorithms): </h2>

In this class we were asked to implement a class representing the algorithms of Graph Theory (directed weighted graph).

In this class some of the algorithms implemented using dijkstra algorithm.  
Intuitive explanation of the algorithm (source: Wikipedia.org):
```diff
 Algorithm loop:
   * As long as there are any unvisited vertices:
   * Mark the X vertex as visited. (current vertex. In the first iteration this is the vertex of the source S)
   * For each vertex Y which is a neighbor of X and we have not yet visited it:
        Y is updated so that its distance is equal to the minimum value between two values: between its current distance,
        and the weight of the edge connecting X and Y plus the distance between S and X.
   * Select a new vertex X as the vertex whose distance from the source S is the shortest (at this point) from all the
     vertices in the graph we have not yet visited.
 The algorithm ends when the new vertex X is the destination or (to find all the fastest paths) when we have visited all the vertices.
```
One of the algorithms implemented using BFS algorithm.  
Intuitive explanation of the algorithm (source: Wikipedia.org):
```diff
The algorithm uses a queue data structure to determine which is the next vertex it is going to visit.
	Each time we visits an vertex we marks it as being "visited", then inspects all the edged coming out of it.
	If an edge leads to an unvisited vertex, that node is added to the queue.
	This way it is ensured that the algorithm will scan the vertices in the order determined by their distance from the initial vertex
	(Because a vertex that enters the queue leaves it only after all the vertices that were in it before have left).
The complexity of the algorithm (in an almost completely linked graph) is in complexity O(v+e) where v=vertices, e=edges of the graph.
```
  
The following functions can be performed:
- Initializes the class object - easily done by referring this graph to the input graph (at the initialization of the graph)  
- Returning the connected components of the graph - in this function we used Kosaraju algorithm (using BFS).  
   Implementation is by the principle that the graph is strongly connected if the original graph is connected and also if after reversing the graph it still connected.  
- Returning the connected component of specific vertex in the graph - in this function we used Kosaraju algorithm (using BFS).  
   Implementation is by the principle that the graph is strongly connected if the original graph is connected and also if after reversing the graph it still connected.  
- Return the shortest path between 2 vertices - There are 2 goals that we implemented in a similar way:  
  * Returning the shortest path length (by weight).  
  * Returning the vertices of the shortest path  
      In this function we used the dijkstra algorithm as explained above,  
      That's because the algorithm scans the vertices in the order determined by their distance (by weight) from the initial vertex, And since we can attribute to each vertex 	the parent corresponding to it (which is closer [at one level] to the initial vertex), So inevitably when we reach the destined vertex we can build the shortest path (the path that weighs the least) and this is done by attributing each vertex to its "parent".  
- Save the graph as an object to an json file.
- Load the graph from an json file and initialize it.
- Plot the graph - Implementation is by 'matplotlib' built-in calss in Python.

