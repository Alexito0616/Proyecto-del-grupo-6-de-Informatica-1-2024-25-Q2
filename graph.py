import matplotlib.pyplot as plt
from segment import Segment
from node import AddNeighbor, Distance, Node
import heapq
from path import Path
from tkinter import simpledialog, messagebox
class Graph:
   def __init__(self):
       self.nodes = []
       self.segments = []




def AddNode(g, n):
   if n in g.nodes:
       return False
   g.nodes.append(n)
   return True




def AddSegment(g, nameOriginNode, nameDestinationNode):
   origin = None
   destination = None


   # Find the origin and destination nodes
   for node in g.nodes:
       if node.name == nameOriginNode:
           origin = node
       if node.name == nameDestinationNode:
           destination = node


   # If either node is not found, return False
   if origin is None or destination is None:
       return False


   # Create the segment and add it to the graph
   segment = Segment(nameOriginNode + "-" + nameDestinationNode, origin, destination)
   g.segments.append(segment)


   # Add the destination as a neighbor of the origin
   AddNeighbor(origin, destination)


   return True




def GetClosest(g, x, y):
   if not g.nodes:
       return None


   min_node = g.nodes[0]
   min_distance = ((min_node.x - x) ** 2 + (min_node.y - y) ** 2) ** 0.5


   for node in g.nodes[1:]:
       dist = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
       if dist < min_distance:
           min_node = node
           min_distance = dist


   return min_node




def Plot(g):
   plt.figure(figsize=(8, 8))


   # Dibujar todos los nodos
   for node in g.nodes:
       plt.plot(node.x, node.y, 'o', color='red')
       plt.text(node.x + 0.1, node.y + 0.1, node.name, fontsize=9)


   # Dibujar todos los segmentos
   for seg in g.segments:
       x_values = [seg.origin.x, seg.destination.x]
       y_values = [seg.origin.y, seg.destination.y]
       plt.plot(x_values, y_values, 'b-')  # línea azul


       # Escribir el costo en medio
       mid_x = (seg.origin.x + seg.destination.x) / 2
       mid_y = (seg.origin.y + seg.destination.y) / 2
       plt.text(mid_x, mid_y, f"{seg.cost:.1f}", color='black', fontsize=8)


   plt.title("Graph Plot")
   plt.grid(True)
   plt.axis('equal')
   plt.show()




def PlotNode(g, nameOrigin):
   plt.figure(figsize=(8, 8))
   origin = None
   for node in g.nodes:
       if node.name == nameOrigin:
           origin = node
           break


   if origin is None:
       return False


   plt.figure(figsize=(8, 8))


   for node in g.nodes:
       color = 'gray'
       if node == origin:
           color = 'blue'
       elif node in origin.neighbors:
           color = 'green'
       plt.plot(node.x, node.y, 'o', color=color)
       plt.text(node.x + 0.1, node.y + 0.1, node.name, fontsize=9)


   for neighbor in origin.neighbors:
       x_values = [origin.x, neighbor.x]
       y_values = [origin.y, neighbor.y]
       plt.plot(x_values, y_values, 'r-', linewidth=2)  # línea roja gruesa


       # Escribir el costo en medio
       mid_x = (origin.x + neighbor.x) / 2
       mid_y = (origin.y + neighbor.y) / 2
       cost = Distance(origin, neighbor)
       plt.text(mid_x, mid_y, f"{cost:.1f}", color='black', fontsize=8)


   plt.title(f"Node '{origin.name}' and its Neighbors")
   plt.grid(True)
   plt.axis('equal')
   plt.show()


   return True




class Graph:
   def __init__(self):
       self.nodes = []
       self.segments = []




def AddNode(g, n):
   if n not in g.nodes:
       g.nodes.append(n)
       return True
   return False




def AddSegment(g, origin_name, destination_name):
   origin = None
   destination = None


   for node in g.nodes:
       if node.name == origin_name:
           origin = node
       if node.name == destination_name:
           destination = node


   if origin is None or destination is None:
       return False


   segment = Segment(origin_name + "-" + destination_name, origin, destination)
   g.segments.append(segment)
   AddNeighbor(origin, destination)


   return True




def CreateGraphFromFile(filename):
   g = Graph()


   try:
       with open(filename, 'r') as file:
           lines = file.readlines()


       node_section = True  # Flag para saber si estamos leyendo nodos o segmentos


       for line in lines:
           line = line.strip()
           if not line or line.startswith("#"):
               continue


           if line == "# Segments":
               node_section = False
               continue


           data = line.split()


           if node_section:
               # Formato: Nombre x y
               if len(data) != 3:
                   raise ValueError(f"Invalid node line: '{line}'")
               node_name = data[0]
               x = float(data[1])
               y = float(data[2])
               new_node = Node(node_name, x, y)
               AddNode(g, new_node)
           else:
               # Formato: NombreOrigen NombreDestino
               if len(data) != 2:
                   raise ValueError(f"Invalid segment line: '{line}'")
               node1_name = data[0]
               node2_name = data[1]
               AddSegment(g, node1_name, node2_name)


       return g




   except FileNotFoundError:
       print(f"Error: The file '{filename}' was not found.")
       return None
   except Exception as e:
       print(f"Error reading the file: {e}")
       return None




def RemoveNode(g, node_name):
   # Encuentra el nodo
   node_to_remove = None
   for node in g.nodes:
       if node.name == node_name:
           node_to_remove = node
           break
   if not node_to_remove:
       return False


   # Eliminar todos los segmentos relacionados
   g.segments = [s for s in g.segments if s.origin != node_to_remove and s.destination != node_to_remove]


   # Eliminar de vecinos
   for node in g.nodes:
       if node_to_remove in node.neighbors:
           node.neighbors.remove(node_to_remove)


   # Eliminar el nodo
   g.nodes.remove(node_to_remove)
   return True




def SaveGraphToFile(g, filename):
   try:
       with open(filename, 'w') as file:
           for node in g.nodes:
               file.write(f"{node.name} {node.x} {node.y}\n")
           file.write("# Segments\n")
           for seg in g.segments:
               file.write(f"{seg.origin.name} {seg.destination.name}\n")
       return True
   except Exception as e:
       print(f"Error saving graph: {e}")
       return False


def GetReachableNodes(graph, start_node_name):
   start_node = next((n for n in graph.nodes if n.name == start_node_name), None)
   if not start_node:
       return []


   visited = set()
   stack = [start_node]


   while stack:
       current = stack.pop()
       if current not in visited:
           visited.add(current)
           stack.extend([n for n in current.neighbors if n not in visited])


   return list(visited)


def GetShortestPath(graph, start_name, end_name):
   start = next((n for n in graph.nodes if n.name == start_name), None)
   end = next((n for n in graph.nodes if n.name == end_name), None)
   if not start or not end:
       return None  # Nodo no encontrado


   distances = {node: float('inf') for node in graph.nodes}
   previous = {node: None for node in graph.nodes}
   distances[start] = 0


   queue = [(0, start)]


   while queue:
       current_dist, current_node = heapq.heappop(queue)


       if current_node == end:
           break


       for neighbor in current_node.neighbors:
           seg = next((s for s in graph.segments if
                       (s.origin == current_node and s.destination == neighbor) or
                       (s.destination == current_node and s.origin == neighbor)), None)
           if not seg:
               continue


           alt = current_dist + seg.cost
           if alt < distances[neighbor]:
               distances[neighbor] = alt
               previous[neighbor] = current_node
               heapq.heappush(queue, (alt, neighbor))


   # Reconstruir el camino
   path = []
   node = end
   while node:
       path.insert(0, node)
       node = previous[node]


   if path[0] != start:
       return None  # No hay camino


   return path


def FindShortestPath(graph, origin_name, destination_name):
   origin = next((n for n in graph.nodes if n.name == origin_name), None)
   destination = next((n for n in graph.nodes if n.name == destination_name), None)


   if not origin or not destination:
       return None  # Si no se encuentran los nodos


   # Crear un nuevo camino y agregar el nodo de origen
   path = Path()
   path.AddNodeToPath(origin)


   visited = set()
   queue = [(origin, path)]  # Almacenamos los nodos junto con su camino actual


   while queue:
       current_node, current_path = queue.pop(0)


       if current_node == destination:
           return current_path  # Si llegamos al nodo de destino, retornamos el camino


       visited.add(current_node)


       for neighbor in current_node.neighbors:
           if neighbor not in visited:
               new_path = Path()
               new_path.nodes = current_path.nodes.copy()  # Copiar el camino hasta ahora
               new_path.total_cost = current_path.total_cost  # Copiar el costo acumulado
               new_path.AddNodeToPath(neighbor)  # Añadir el nodo vecino al nuevo camino
               queue.append((neighbor, new_path))  # Añadir el vecino a la cola


   return None  # Si no se encuentra un camino


def show_shortest_path(self):
   origin_name = simpledialog.askstring("Nodo de origen", "Introduce el nombre del nodo de origen:")
   destination_name = simpledialog.askstring("Nodo de destino", "Introduce el nombre del nodo de destino:")


   if origin_name and destination_name:
       path = FindShortestPath(self.graph, origin_name, destination_name)
       if path:
           path.PlotPath(self.graph)  # Dibuja el camino más corto en el gráfico
           messagebox.showinfo("Camino más corto", f"El costo total es: {path.total_cost}")
       else:
           messagebox.showerror("Error", "No hay camino entre esos nodos.")
