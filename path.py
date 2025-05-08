from graph import Distance


class Path:
   def __init__(self):
       self.nodes = []  # Lista de nodos en el camino
       self.total_cost = 0  # Costo total del camino


   def AddNodeToPath(self, node):
       if self.nodes:
           last_node = self.nodes[-1]
           self.total_cost += Distance(last_node, node)  # Sumar la distancia del último nodo
       self.nodes.append(node)


   def ContainsNode(self, node):
       return node in self.nodes


   def CostToNode(self, node):
       if node in self.nodes:
           index = self.nodes.index(node)
           cost = sum(Distance(self.nodes[i], self.nodes[i+1]) for i in range(index))
           return cost
       return -1  # Si el nodo no está en el camino


   def PlotPath(self, graph):
       # Función para trazar el camino en el gráfico
       for i in range(len(self.nodes) - 1):
           start = self.nodes[i]
           end = self.nodes[i + 1]
           graph.ax.plot([start.x, end.x], [start.y, end.y], 'g-', linewidth=2)
           graph.ax.text(start.x + 0.2, start.y + 0.2, start.name, fontsize=9)
       graph.canvas.draw()
