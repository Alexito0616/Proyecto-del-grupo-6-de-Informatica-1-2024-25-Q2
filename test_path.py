from graph import Node, Segment, Graph, FindShortestPath
from path import Path


def test_AddNodeToPath():
   graph = Graph()
   n1 = Node('A', 0, 0)
   n2 = Node('B', 3, 4)
   graph.nodes.append(n1)
   graph.nodes.append(n2)
   segment = Segment('AB', n1, n2)
   graph.segments.append(segment)


   path = Path()
   path.AddNodeToPath(n1)
   path.AddNodeToPath(n2)


   assert path.ContainsNode(n1) == True
   assert path.ContainsNode(n2) == True
   assert path.CostToNode(n2) == 5.0  # Distancia entre A y B


def test_FindShortestPath():
   graph = Graph()
   n1 = Node('A', 0, 0)
   n2 = Node('B', 3, 4)
   n3 = Node('C', 6, 8)
   graph.nodes.extend([n1, n2, n3])


   segment1 = Segment('AB', n1, n2)
   segment2 = Segment('BC', n2, n3)
   graph.segments.extend([segment1, segment2])


   path = FindShortestPath(graph, 'A', 'C')
   assert path is not None
   assert path.CostToNode(n2) == 5.0  # A -> B
   assert path.CostToNode(n3) == 10.0  # A -> B -> C


   path = FindShortestPath(graph, 'A', 'D')
   assert path is None  # No hay nodo D
