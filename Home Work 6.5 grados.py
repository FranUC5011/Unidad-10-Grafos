from grafos import Grafo

arbol = Grafo(dirigido=True)
relaciones = [
    ("Juan", "Carlos"), ("María", "Carlos"),
    ("Juan", "Ana"),    ("María", "Ana"),
    ("Carlos", "Luis"), ("Carlos", "Sofía"),
    ("Ana", "Diego"),   ("Luis", "Mateo"),
]
for padre, hijo in relaciones:
    arbol.agregar_arista(padre, hijo)


g_dir = Grafo(dirigido=True)
for u, v in [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A"), ("D", "C")]:
    g_dir.agregar_arista(u, v)

grados_g = g_dir.grados()
for v, (ent, sal) in grados_g.items():
    print(f"{v}: entrada = {ent}, salida = {sal}")

assert grados_g == {"A": (1, 2), "B": (1, 1), "C": (3, 1), "D": (0, 1)}

total_entrada = sum(e for e, _ in grados_g.values())
total_salida = sum(s for _, s in grados_g.values())
assert total_entrada == total_salida == 5   # 5 aristas en total
print("\nSuma de entradas = suma de salidas = 5 aristas ✔")

# Aplicado al árbol genealógico de 5.1: entrada = padres, salida = hijos
print("\nÁrbol genealógico (padres, hijos):")
for persona, (padres, hijos) in arbol.grados().items():
    print(f"  {persona:<8} padres={padres}  hijos={hijos}")
assert arbol.grados()["Carlos"] == (2, 2)
print("\n✅ Grados calculados correctamente")
