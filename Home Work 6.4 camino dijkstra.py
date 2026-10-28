from grafos import GrafoPonderado
import math

def construir_vuelos():
    """Red de vuelos de ejemplo: cada arista es una tarifa en euros."""
    tarifas = [
        ("Madrid", "París", 120), ("Madrid", "Roma", 95),   ("Madrid", "Lisboa", 70),
        ("París", "Londres", 80), ("París", "Berlín", 90),  ("Roma", "Berlín", 110),
        ("Lisboa", "Londres", 150), ("Berlín", "Londres", 60),
    ]
    vuelos = GrafoPonderado()
    for origen, destino, precio in tarifas:
        vuelos.agregar_arista(origen, destino, precio)
    return vuelos


vuelos = construir_vuelos()

costo, camino = vuelos.dijkstra_camino("Madrid", "Berlín")
print(f"Madrid → Berlín: {costo} € por {' → '.join(camino)}")

costo2, camino2 = vuelos.dijkstra_camino("Madrid", "Londres")
print(f"Madrid → Londres: {costo2} € por {' → '.join(camino2)}")

assert (costo, camino) == (205, ["Madrid", "Roma", "Berlín"])
assert (costo2, camino2) == (200, ["Madrid", "París", "Londres"])
assert vuelos.dijkstra_camino("Madrid", "Madrid") == (0, ["Madrid"])

# Caso sin camino: un destino aislado
aislado = construir_vuelos()
aislado.agregar_vertice("Tokio")
c, ruta_vacia = aislado.dijkstra_camino("Madrid", "Tokio")
print(f"Madrid → Tokio: costo={c}, camino={ruta_vacia}")
assert c == math.inf and ruta_vacia == []

print("\n✅ Dijkstra con reconstrucción de camino correcto")
