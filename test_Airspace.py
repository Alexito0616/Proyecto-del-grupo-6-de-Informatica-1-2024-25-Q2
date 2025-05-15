from Airspace import AirSpace


# Cargar datos
airspace = AirSpace()
airspace.load_from_files("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")


# Mostrar vecinos de un punto (ej: 6063 es IZA.D)
airspace.show_neighbors(6063)


# Mostrar camino más corto entre dos puntos
start = 6063  # IZA.D
end = 6937    # LAMPA
path = airspace.shortest_path(start, end)
print("Camino más corto:", path)

