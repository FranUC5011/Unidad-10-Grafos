from grafos import Grafo

import random

g = Grafo()
for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"), ("D", "E")]:
    g.agregar_arista(u, v)

print("DFS recursivo:", g.dfs("A"))
print("DFS iterativo:", g.dfs_iterativo("A"))
assert g.dfs_iterativo("A") == g.dfs("A")

# Comparación con 50 grafos aleatorios (dirigidos y no dirigidos)
random.seed(42)
for _ in range(50):
    gr = Grafo(dirigido=random.random() < 0.5)
    n = random.randint(3, 10)
    for _ in range(random.randint(n, 3 * n)):
        gr.agregar_arista(random.randrange(n), random.randrange(n))
    inicio = next(iter(gr.adj))
    assert gr.dfs_iterativo(inicio) == gr.dfs(inicio)

print("\n✅ El DFS iterativo coincide con el recursivo en 50 grafos aleatorios")
