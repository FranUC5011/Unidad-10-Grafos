from grafos import GrafoPonderado

red_trafico = GrafoPonderado(dirigido=True)
enlaces = [
    ("R1", "R2", 5), ("R1", "R3", 10), ("R2", "R3", 2), ("R2", "R4", 7),
    ("R3", "R4", 1), ("R3", "R5", 9),  ("R4", "R5", 3), ("R5", "R1", 4),
]
for origen, destino, ms in enlaces:
    red_trafico.agregar_arista(origen, destino, ms)

lat, ruta = red_trafico.dijkstra_camino("R1", "R5")
print(f"Menor latencia R1 → R5: {lat} ms por {' → '.join(ruta)}")

lat2, ruta2 = red_trafico.dijkstra_camino("R5", "R2")
print(f"Menor latencia R5 → R2: {lat2} ms por {' → '.join(ruta2)}")

assert (lat, ruta) == (11, ["R1", "R2", "R3", "R4", "R5"])
assert (lat2, ruta2) == (9, ["R5", "R1", "R2"])   # la vuelta no es igual a la ida

print("\n✅ Ruta de menor latencia correcta (y distinta en cada sentido)")
