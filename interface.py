import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import CreateGraphFromFile, AddSegment, AddNode, RemoveNode, SaveGraphToFile, Graph, GetReachableNodes,GetShortestPath
from test_graph import CreateGraph_1, CreateGraph_2
from node import Node




class GraphInterface:
   def __init__(self, master):
       self.master = master
       self.master.title("Graph Interface")


       # Variables
       self.graph = None
       self.selected_node = None
       self.mode = None  # 'add_node', 'add_segment', 'delete_node', etc.
       self.first_segment_node = None


       # Matplotlib figure
       self.fig, self.ax = plt.subplots(figsize=(6, 6))
       self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
       self.canvas.get_tk_widget().pack(side=tk.LEFT)
       self.canvas.mpl_connect("button_press_event", self.on_click)


       # Botones
       frame = tk.Frame(master)
       frame.pack(side=tk.RIGHT, fill=tk.BOTH)


       tk.Button(frame, text="Mostrar Grafo Ejemplo", command=self.show_example_graph).pack(fill=tk.X)
       tk.Button(frame, text="Mostrar Grafo Inventado", command=self.show_invented_graph).pack(fill=tk.X)
       tk.Button(frame, text="Cargar Grafo desde Archivo", command=self.load_graph_from_file).pack(fill=tk.X)
       tk.Button(frame, text="Seleccionar Nodo y Ver Vecinos", command=self.select_node_mode).pack(fill=tk.X)
       tk.Button(frame, text="Mostrar Alcanzables", command=self.reachability_mode).pack(fill=tk.X)
       tk.Button(frame, text="Camino más corto", command=self.shortest_path_mode).pack(fill=tk.X)


       tk.Label(frame, text="------").pack()
       tk.Button(frame, text="Añadir Nodo", command=self.add_node_mode).pack(fill=tk.X)
       tk.Button(frame, text="Añadir Segmento", command=self.add_segment_mode).pack(fill=tk.X)
       tk.Button(frame, text="Eliminar Nodo", command=self.delete_node_mode).pack(fill=tk.X)
       tk.Button(frame, text="Nuevo Grafo", command=self.new_graph).pack(fill=tk.X)
       tk.Button(frame, text="Guardar Grafo", command=self.save_graph_to_file).pack(fill=tk.X)


   def on_click(self, event):
       if event.xdata is None or event.ydata is None:
           return


       if self.graph is None:
           return


       if self.mode == "add_node":
           name = simpledialog.askstring("Nuevo Nodo", "Introduce el nombre del nodo:")
           if name:
               new_node = Node(name, event.xdata, event.ydata)
               AddNode(self.graph, new_node)
               self.plot_graph()


       elif self.mode == "add_segment":
           clicked_node = self.get_node_at(event.xdata, event.ydata)
           if clicked_node:
               if not self.first_segment_node:
                   self.first_segment_node = clicked_node
                   messagebox.showinfo("Segmento", f"Primer nodo seleccionado: {clicked_node.name}")
               else:
                   AddSegment(self.graph, self.first_segment_node.name, clicked_node.name)
                   self.first_segment_node = None
                   self.plot_graph()


       elif self.mode == "delete_node":
           clicked_node = self.get_node_at(event.xdata, event.ydata)
           if clicked_node:
               RemoveNode(self.graph, clicked_node.name)
               self.plot_graph()


       elif self.mode == "select_node":
           clicked_node = self.get_node_at(event.xdata, event.ydata)
           if clicked_node:
               self.plot_node_neighbors(clicked_node)
       elif self.mode == "reachability":
           clicked_node = self.get_node_at(event.xdata, event.ydata)
           if clicked_node:
               reachable = GetReachableNodes(self.graph, clicked_node.name)
               self.plot_reachability(clicked_node, reachable)
       elif self.mode == "shortest_path":
           clicked_node = self.get_node_at(event.xdata, event.ydata)
           if clicked_node:
               if not self.first_segment_node:
                   self.first_segment_node = clicked_node
                   messagebox.showinfo("Camino más corto", f"Origen seleccionado: {clicked_node.name}")
               else:
                   path = GetShortestPath(self.graph, self.first_segment_node.name, clicked_node.name)
                   if path:
                       self.plot_shortest_path(path)
                   else:
                       messagebox.showwarning("Sin camino", "No hay un camino entre esos nodos.")
                   self.first_segment_node = None


   def get_node_at(self, x, y):
       # Devuelve el nodo más cercano si está cerca (por ejemplo, 0.5 de distancia)
       threshold = 0.5
       for node in self.graph.nodes:
           if ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5 < threshold:
               return node
       return None


   def plot_graph(self):
       self.ax.clear()


       if not self.graph:
           self.canvas.draw()
           return


       # Dibujar segmentos
       for seg in self.graph.segments:
           self.ax.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'b-')


       # Dibujar nodos
       for node in self.graph.nodes:
           self.ax.plot(node.x, node.y, 'ro')
           self.ax.text(node.x + 0.2, node.y + 0.2, node.name, fontsize=9)


       self.ax.set_title("Graph")
       self.ax.set_xlim(0, 20)
       self.ax.set_ylim(0, 22)
       self.ax.grid(True)
       self.canvas.draw()


   def plot_node_neighbors(self, origin):
       self.ax.clear()


       # Dibujar solo el nodo y sus vecinos
       for node in self.graph.nodes:
           if node == origin:
               self.ax.plot(node.x, node.y, 'bo')  # Azul el nodo seleccionado
           elif node in origin.neighbors:
               self.ax.plot(node.x, node.y, 'go')  # Verde vecinos
           else:
               self.ax.plot(node.x, node.y, 'ro')  # Rojo otros


           self.ax.text(node.x + 0.2, node.y + 0.2, node.name, fontsize=9)


       # Dibujar las conexiones
       for neighbor in origin.neighbors:
           self.ax.plot([origin.x, neighbor.x], [origin.y, neighbor.y], 'r-', linewidth=2)


       self.ax.set_title(f"Vecinos de {origin.name}")
       self.ax.set_xlim(0, 20)
       self.ax.set_ylim(0, 22)
       self.ax.grid(True)
       self.canvas.draw()


   def show_example_graph(self):
       self.graph = CreateGraph_1()
       self.plot_graph()


   def show_invented_graph(self):
       self.graph = CreateGraph_2()
       self.plot_graph()


   def load_graph_from_file(self):
       filename = filedialog.askopenfilename(title="Selecciona archivo de grafo", filetypes=[("Text files", "*.txt")])
       if filename:
           self.graph = CreateGraphFromFile(filename)
           if self.graph:
               self.plot_graph()


   def save_graph_to_file(self):
       filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
       if filename:
           if SaveGraphToFile(self.graph, filename):
               messagebox.showinfo("Guardado", "Grafo guardado correctamente.")
           else:
               messagebox.showerror("Error", "No se pudo guardar el grafo.")


   def select_node_mode(self):
       self.mode = "select_node"
       self.first_segment_node = None


   def add_node_mode(self):
       self.mode = "add_node"
       self.first_segment_node = None


   def add_segment_mode(self):
       self.mode = "add_segment"
       self.first_segment_node = None


   def delete_node_mode(self):
       self.mode = "delete_node"
       self.first_segment_node = None


   def new_graph(self):
       self.graph = Graph()
       self.plot_graph()


   def reachability_mode(self):
       self.mode = "reachability"
       self.first_segment_node = None


   def plot_reachability(self, origin, reachable_nodes):
       self.ax.clear()


       for node in self.graph.nodes:
           if node == origin:
               self.ax.plot(node.x, node.y, 'bo')  # azul = origen
           elif node in reachable_nodes:
               self.ax.plot(node.x, node.y, 'go')  # verde = alcanzables
           else:
               self.ax.plot(node.x, node.y, 'ro')  # rojo = no alcanzables


           self.ax.text(node.x + 0.2, node.y + 0.2, node.name, fontsize=9)


       for segment in self.graph.segments:
           self.ax.plot([segment.origin.x, segment.destination.x], [segment.origin.y, segment.destination.y], 'gray',
                        linestyle='--')


       self.ax.set_title(f"Nodos alcanzables desde {origin.name}")
       self.ax.set_xlim(0, 20)
       self.ax.set_ylim(0, 22)
       self.ax.grid(True)
       self.canvas.draw()


   def shortest_path_mode(self):
       self.mode = "shortest_path"
       self.first_segment_node = None


   def plot_shortest_path(self, path):
       self.ax.clear()


       # Dibujar nodos
       for node in self.graph.nodes:
           color = 'ro'
           if node == path[0]:
               color = 'bo'
           elif node == path[-1]:
               color = 'yo'
           elif node in path:
               color = 'go'
           self.ax.plot(node.x, node.y, color)
           self.ax.text(node.x + 0.2, node.y + 0.2, node.name, fontsize=9)


       # Dibujar todos los segmentos en gris claro
       for seg in self.graph.segments:
           self.ax.plot([seg.origin.x, seg.destination.x], [seg.origin.y, seg.destination.y], 'lightgray',
                        linestyle='--')


       # Dibujar camino más corto
       for i in range(len(path) - 1):
           self.ax.plot([path[i].x, path[i + 1].x], [path[i].y, path[i + 1].y], 'b-', linewidth=3)


       self.ax.set_title("Camino más corto")
       self.ax.set_xlim(0, 20)
       self.ax.set_ylim(0, 22)
       self.ax.grid(True)
       self.canvas.draw()


   def show_reachability(self):
       node_name = simpledialog.askstring("Nodo de origen", "Introduce el nombre del nodo:")
       node = next((n for n in self.graph.nodes if n.name == node_name), None)


       if node:
           reachable_nodes = self.get_reachable_nodes(node)
           reachable_node_names = [n.name for n in reachable_nodes]
           messagebox.showinfo("Alcanzabilidad",
                               f"Los nodos alcanzables desde {node_name} son: {', '.join(reachable_node_names)}")
       else:
           messagebox.showerror("Error", "Nodo no encontrado.")


   def get_reachable_nodes(self, node):
       # Realiza una búsqueda en anchura o profundidad para obtener nodos alcanzables.
       visited = set()
       reachable = []


       def dfs(current):
           visited.add(current)
           reachable.append(current)
           for neighbor in current.neighbors:
               if neighbor not in visited:
                   dfs(neighbor)


       dfs(node)
       return reachable




# --- Lanza la app ---
if __name__ == "__main__":
   root = tk.Tk()
   app = GraphInterface(root)
   root.mainloop()
