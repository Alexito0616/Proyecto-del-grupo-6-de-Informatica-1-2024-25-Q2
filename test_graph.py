import matplotlib.pyplot as plt
from graph import *
from node import Node




def CreateGraph_1():
   G = Graph()
   AddNode(G, Node("A", 1, 20))
   AddNode(G, Node("B", 8, 17))
   AddNode(G, Node("C", 15, 20))
   AddNode(G, Node("D", 18, 15))
   AddNode(G, Node("E", 2, 4))
   AddNode(G, Node("F", 6, 5))
   AddNode(G, Node("G", 12, 12))
   AddNode(G, Node("H", 10, 3))
   AddNode(G, Node("I", 19, 1))
   AddNode(G, Node("J", 13, 5))
   AddNode(G, Node("K", 3, 15))
   AddNode(G, Node("L", 4, 10))


   AddSegment(G, "A", "B")
   AddSegment(G, "A", "E")
   AddSegment(G, "A", "K")
   AddSegment(G, "B", "A")
   AddSegment(G, "B", "C")
   AddSegment(G, "B", "F")
   AddSegment(G, "B", "K")
   AddSegment(G, "B", "G")
   AddSegment(G, "C", "D")
   AddSegment(G, "C", "G")
   AddSegment(G, "D", "G")
   AddSegment(G, "D", "H")
   AddSegment(G, "D", "I")
   AddSegment(G, "E", "F")
   AddSegment(G, "F", "L")
   AddSegment(G, "G", "B")
   AddSegment(G, "G", "F")
   AddSegment(G, "G", "H")
   AddSegment(G, "I", "D")
   AddSegment(G, "I", "J")
   AddSegment(G, "J", "I")
   AddSegment(G, "K", "A")
   AddSegment(G, "K", "L")
   AddSegment(G, "L", "K")
   AddSegment(G, "L", "F")
   return G




def CreateGraph_2():
   G2 = Graph()
   AddNode(G2, Node("C", 15, 20))
   AddNode(G2, Node("D", 18, 15))
   AddNode(G2, Node("G", 12, 12))


   AddSegment(G2, "C", "D")
   AddSegment(G2, "C", "G")
   return G2




print("Probando el grafo...")


G = CreateGraph_1()


# 1. Mostrar todo el grafo
Plot(G)
plt.show()
plt.close()


# 2. Mostrar el nodo 'C' y sus vecinos
PlotNode(G, "C")
plt.show()
plt.close()


# 3. Probar GetClosest
n = GetClosest(G, 15, 5)
print(n.name)  # La respuesta debe ser J


n = GetClosest(G, 8, 19)
print(n.name)  # La respuesta debe ser B


# 4. Crear un segundo grafo inventado
G2 = CreateGraph_2()


# 5. Mostrar el segundo grafo
Plot(G2)
plt.show()
plt.close()


import matplotlib.pyplot as plt
from graph import *
from node import Node, AddNeighbor
from segment import Segment




def TestCreateGraphFromFile():
   print("Creating graph from file...")


   # Create the graph from the file
   G = CreateGraphFromFile("graph_data.txt")


   # Check if the graph was created successfully
   if G:
       # Plot the graph
       Plot(G)
       print("Graph created successfully.")
   else:
       print("Failed to create graph.")




# Run the test
TestCreateGraphFromFile()
