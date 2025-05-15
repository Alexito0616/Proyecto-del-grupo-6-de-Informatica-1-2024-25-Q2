import tkinter as tk
from tkinter import messagebox
from Airspace import AirSpace
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class AirspaceGUI:
   def __init__(self, master):
       self.master = master
       self.master.title("Visualizador de espacio aéreo - Catalunya")


       # Cargar el airspace
       self.airspace = AirSpace()
       self.airspace.load_from_files("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")


       # Variables para selección de nodos
       self.selected_nodes = []


       # Crear figura de matplotlib
       self.fig, self.ax = plt.subplots(figsize=(10, 8))
       self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
       self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
       self.canvas.mpl_connect("button_press_event", self.on_click)


       # Botones
       btn_frame = tk.Frame(master)
       btn_frame.pack()


       self.btn_vecinos = tk.Button(btn_frame, text="Mostrar vecinos", command=self.show_neighbors)
       self.btn_vecinos.pack(side=tk.LEFT)


       self.btn_ruta = tk.Button(btn_frame, text="Camino más corto", command=self.shortest_path)
       self.btn_ruta.pack(side=tk.LEFT)


       self.btn_limpiar = tk.Button(btn_frame, text="Limpiar selección", command=self.clear_selection)
       self.btn_limpiar.pack(side=tk.LEFT)


       self.draw_graph()


   def draw_graph(self, path=None, highlight_neighbors=None):
       self.ax.clear()


           # Dibujar segmentos
       for seg in self.airspace.navsegments:
           p1 = self.airspace.navpoints[seg.origin_id]
           p2 = self.airspace.navpoints[seg.dest_id]
           color = 'lightblue'
           if path and seg.origin_id in path and seg.dest_id in path:
               i = path.index(seg.origin_id)
               if i + 1 < len(path) and path[i + 1] == seg.dest_id:
                   color = 'red'
           elif highlight_neighbors and seg.origin_id == highlight_neighbors[0] and seg.dest_id in highlight_neighbors[
               1]:
               color = 'orange'
           self.ax.plot([p1.lon, p2.lon], [p1.lat, p2.lat], color=color)


       # Dibujar nodos
       for np in self.airspace.navpoints.values():
           color = 'black'
           if np.id in self.selected_nodes:
               color = 'green'
           self.ax.plot(np.lon, np.lat, 'o', color=color)
           self.ax.text(np.lon, np.lat, np.name, fontsize=6)


       self.ax.set_title("Mapa de navegación aérea - Catalunya")
       self.ax.set_xlabel("Longitud")
       self.ax.set_ylabel("Latitud")
       self.ax.grid(True)
       self.canvas.draw()


   def on_click(self, event):
       if event.xdata is None or event.ydata is None:
           return


       closest = self.airspace.get_closest(event.xdata, event.ydata)
       if closest:
           if closest.id not in self.selected_nodes:
               self.selected_nodes.append(closest.id)
               if len(self.selected_nodes) > 2:
                   self.selected_nodes.pop(0)
           self.draw_graph()


   def show_neighbors(self):
       if not self.selected_nodes:
           messagebox.showinfo("Info", "Selecciona un nodo.")
           return
       nid = self.selected_nodes[-1]
       np = self.airspace.navpoints[nid]
       neighbors = self.airspace.get_neighbors(nid)
       names = [self.airspace.navpoints[n].name for n in neighbors]
       messagebox.showinfo("Vecinos", f"Nodo {np.name} tiene vecinos: {', '.join(names)}")
       self.draw_graph(highlight_neighbors=(nid, neighbors))


   def shortest_path(self):
       if len(self.selected_nodes) != 2:
           messagebox.showwarning("Advertencia", "Selecciona dos nodos.")
           return
       path = self.airspace.shortest_path(self.selected_nodes[0], self.selected_nodes[1])
       self.draw_graph(path)


   def clear_selection(self):
       self.selected_nodes = []
       self.draw_graph()




if __name__ == "__main__":
   root = tk.Tk()
   app = AirspaceGUI(root)
   root.mainloop()

