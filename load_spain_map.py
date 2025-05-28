import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Airspace import AirSpace  # Asegúrate de que esté disponible
import simplekml
import matplotlib.animation as animation
import numpy as np
from scipy.ndimage import gaussian_filter
import math


class AirspaceGUI:
   def __init__(self, root, airspace):
       self.airspace = airspace
       self.graph = nx.Graph()
       self.root = root
       self.root.title("Visualizador de Espacio Aéreo")
       self.root.rowconfigure(0, weight=1)
       self.root.columnconfigure(0, weight=1)


       self.fig, self.ax = plt.subplots(figsize=(8, 6))
       self.canvas = FigureCanvasTkAgg(self.fig, master=root)
       self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


       self.full_xlim = None
       self.full_ylim = None


       self.ani = None


       frame = tk.Frame(root)
       frame.pack()
       tk.Button(frame, text="Camino más corto entre aeropuertos", command=self.shortest_path).pack(side=tk.LEFT)
       tk.Button(frame, text="Ver vecinos de un nodo", command=self.show_neighbors).pack(side=tk.LEFT)
       tk.Button(frame, text="Restaurar vista completa", command=self.restore_full_view).pack(side=tk.LEFT)
       tk.Button(frame, text="Exportar a KML", command=self.export_to_kml).pack(side=tk.LEFT)


       self._build_graph()
       self._draw_graph()


       self.root.bind("<Configure>", self._on_resize)

   def _build_graph(self):
       for navpoint in self.airspace.navpoints.values():
           self.graph.add_node(navpoint.name, pos=(navpoint.lon, navpoint.lat))


       for segment in self.airspace.navsegments:
           origin = self.airspace.navpoints[segment.origin_id].name
           dest = self.airspace.navpoints[segment.dest_id].name
           self.graph.add_edge(origin, dest, weight=segment.distance)
    #Dibujar el radar
   def _draw_radar_overlay(self):
       if self.full_xlim is None or self.full_ylim is None:
           return
       x_min, x_max = self.full_xlim
       y_min, y_max = self.full_ylim

       # Tamaño de la imagen del radar
       width, height = 300, 300

       # Generar manchas aleatorias (ruido)
       raw_data = np.random.rand(height, width)

       # Aplicar filtro gaussiano para suavizar y crear "manchas de nubes"
       smoothed = gaussian_filter(raw_data, sigma=10)

       # Normalizar los datos
       radar_data = (smoothed - smoothed.min()) / (smoothed.max() - smoothed.min())

       # Dibujar como imagen sobre el gráfico
       self.ax.imshow(
           radar_data,
           extent=(x_min, x_max, y_min, y_max),
           origin='lower',
           cmap='nipy_spectral',  # Otros colores: 'turbo', 'jet', 'nipy_spectral'
           alpha=0.5,
           interpolation='bilinear',
           zorder=0
       )
    #Dibujar el espacio aèreo
   def _draw_graph(self, nodes_to_draw=None, edges_to_draw=None, highlight_path=None, neighbors=None):
       self.ax.clear()

       if nodes_to_draw is None:
           nodes_to_draw = list(self.graph.nodes)
       if edges_to_draw is None:
           edges_to_draw = list(self.graph.edges)

       pos = nx.get_node_attributes(self.graph, 'pos')
       pos = {node: coord for node, coord in pos.items() if node in nodes_to_draw}

       self.ax.set_facecolor('white')
       self._draw_radar_overlay()  # <- NUEVA LÍNEA para radar

       nx.draw_networkx_nodes(self.graph, pos, nodelist=nodes_to_draw, node_size=15, node_color='black', ax=self.ax)
       nx.draw_networkx_edges(self.graph, pos, edgelist=edges_to_draw, edge_color='cyan', width=0.5, ax=self.ax)

       for node, (x, y) in pos.items():
           self.ax.text(x, y + 0.05, node, fontsize=5, ha='center', va='bottom', color='black', zorder=3)

       edge_labels = {(u, v): f"{d['weight']:.1f}" for u, v, d in self.graph.edges(data=True)
                      if (u in pos and v in pos)}
       nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_size=2,
                                    font_color='black', label_pos=0.5, ax=self.ax)

       if highlight_path:
           path_edges = list(zip(highlight_path, highlight_path[1:]))
           nx.draw_networkx_nodes(self.graph, pos, nodelist=highlight_path, node_color='red', node_size=20, ax=self.ax)
           nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, edge_color='red', width=1, ax=self.ax)

       if neighbors:
           nx.draw_networkx_nodes(self.graph, pos, nodelist=neighbors, node_color='green', node_size=20, ax=self.ax)

       self.ax.grid(True, color='red', linestyle='--', linewidth=0.3)
       self.ax.set_title("Espacio aéreo", fontsize=10)
       self.ax.set_xlabel("Longitud")
       self.ax.set_ylabel("Latitud")

       if self.full_xlim is None or self.full_ylim is None:
           xs, ys = zip(*nx.get_node_attributes(self.graph, 'pos').values())
           self.full_xlim = (min(xs) - 0.1, max(xs) + 0.1)
           self.full_ylim = (min(ys) - 0.1, max(ys) + 0.1)

       self.ax.set_xlim(self.full_xlim)
       self.ax.set_ylim(self.full_ylim)

       self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
       self.canvas.draw()

   def _on_resize(self, event):
       if event.widget == self.root:
           width = self.canvas.get_tk_widget().winfo_width()
           height = self.canvas.get_tk_widget().winfo_height()
           dpi = self.fig.get_dpi()
           self.fig.set_size_inches(width / dpi, height / dpi)
           self.canvas.draw()

   def interpolate_coords(self, start, end, steps=20):
       xs = np.linspace(start[0], end[0], steps)
       ys = np.linspace(start[1], end[1], steps)
       return list(zip(xs, ys))
    #Avion que sigue la ruta
   def animate_plane(self, path):
       pos = nx.get_node_attributes(self.graph, 'pos')
       coords = []
       steps_per_segment = 20

       for i in range(len(path) - 1):
           start = pos[path[i]]
           end = pos[path[i + 1]]
           segment_coords = self.interpolate_coords(start, end, steps_per_segment)
           if i < len(path) - 2:
               segment_coords = segment_coords[:-1]
           coords.extend(segment_coords)

       if self.ani:
           self.ani.event_source.stop()
           self.ani = None

       # Inicialización con orientación inicial
       x0, y0 = coords[0]
       x1, y1 = coords[1]
       angle_deg = math.degrees(math.atan2(y1 - y0, x1 - x0))

       plane_text = self.ax.text(
           x0, y0, "✈️", fontsize=25, zorder=10,
           rotation=angle_deg, rotation_mode='anchor', transform_rotates_text=True,
           ha='center', va='center'
       )

       def update(frame):
           x, y = coords[frame]

           if frame < len(coords) - 1:
               x_next, y_next = coords[frame + 1]
               angle = math.degrees(math.atan2(y_next - y, x_next - x))
           else:
               angle = plane_text.get_rotation()

           plane_text.set_position((x, y))
           plane_text.set_rotation(angle)
           return plane_text,

       self.ani = animation.FuncAnimation(
           self.fig, update, frames=len(coords), interval=50,
           blit=True, repeat=False
       )
       self.canvas.draw()
    #Camino mas corto
   def shortest_path(self):
       start = simpledialog.askstring("Inicio", "Nombre del aeropuerto de origen:")
       end = simpledialog.askstring("Destino", "Nombre del aeropuerto de destino:")

       if not start or not end:
           return

       start_nav = self._get_airport_navpoint(start)
       end_nav = self._get_airport_navpoint(end)

       if not start_nav or not end_nav:
           messagebox.showerror("Error", "Uno o ambos aeropuertos no encontrados.")
           return

       try:
           path = nx.shortest_path(self.graph, start_nav.name, end_nav.name, weight='weight')
           edges = list(zip(path, path[1:]))

           self._draw_graph(nodes_to_draw=path, edges_to_draw=edges, highlight_path=path)
           self.animate_plane(path)

           save_kml = messagebox.askyesno("Exportar", "¿Deseas exportar la ruta más corta a KML?")
           if save_kml:
               kml = simplekml.Kml()

               for node in path:
                   lon, lat = self.graph.nodes[node]['pos']
                   kml.newpoint(name=node, coords=[(lon, lat)])

               coords = [self.graph.nodes[node]['pos'] for node in path]
               line = kml.newlinestring(name=f"Ruta de {start} a {end}", coords=coords)
               line.style.linestyle.color = simplekml.Color.red
               line.style.linestyle.width = 3

               filepath = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
               if filepath:
                   kml.save(filepath)
                   messagebox.showinfo("Exportado", f"Ruta exportada a:\n{filepath}")

       except nx.NetworkXNoPath:
           messagebox.showinfo("Sin camino", "No hay camino entre los aeropuertos especificados.")
    #Mostrar vecinos de un nodo
   def show_neighbors(self):
       node_name = simpledialog.askstring("Vecinos", "Nombre del nodo/navpoint:")
       if not node_name:
           return

       navpoint = next((np for np in self.airspace.navpoints.values() if np.name == node_name), None)
       if not navpoint:
           messagebox.showerror("Error", f"Nodo '{node_name}' no encontrado.")
           return

       neighbors_ids = self.airspace.get_neighbors(navpoint.id)
       neighbor_names = [self.airspace.navpoints[nid].name for nid in neighbors_ids]
       edges = [(navpoint.name, name) for name in neighbor_names]

       messagebox.showinfo("Vecinos", f"{navpoint.name} tiene como vecinos: {', '.join(neighbor_names)}")

       self._draw_graph(nodes_to_draw=[navpoint.name] + neighbor_names, edges_to_draw=edges,
                        neighbors=[navpoint.name] + neighbor_names)
    #Buscar el aeropuerto
   def _get_airport_navpoint(self, airport_name):
       for airport in self.airspace.navairports:
           if airport.name == airport_name and airport.sids:
               return airport.sids[0]
       return None

   def restore_full_view(self):
       self._draw_graph()
    #Exportar a KML 
   def export_to_kml(self):
       kml = simplekml.Kml()

       for navpoint in self.airspace.navpoints.values():
           kml.newpoint(name=navpoint.name, coords=[(navpoint.lon, navpoint.lat)])

       for airport in self.airspace.navairports:
           if airport.sids:
               sid = airport.sids[0]
               kml.newpoint(name=airport.name, coords=[(sid.lon, sid.lat)], description="Aeropuerto")

       for segment in self.airspace.navsegments:
           origin = self.airspace.navpoints[segment.origin_id]
           dest = self.airspace.navpoints[segment.dest_id]
           kml.newlinestring(
               name=f"{origin.name} - {dest.name}",
               coords=[(origin.lon, origin.lat), (dest.lon, dest.lat)]
           )

       filepath = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
       if filepath:
           kml.save(filepath)
           messagebox.showinfo("Exportado", f"Archivo KML guardado en:\n{filepath}")

# --- Punto de entrada ---
if __name__ == "__main__":
   airspace = AirSpace()
   airspace.load_from_files("Spain_nav.txt", "Spain_seg.txt", "Spain_aer.txt")
   root = tk.Tk()
   gui = AirspaceGUI(root, airspace)
   root.mainloop()
