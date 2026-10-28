"""
tarea_6_2_ciclos_dirigidos.py - Tarea 6.2: detectar ciclos en un grafo dirigido.

Ejecutar:  python tarea_6_2_ciclos_dirigidos.py
"""
from grafos import Grafo

# DAG (sin ciclos): un "rombo" donde D se alcanza por dos caminos distintos
dag = Grafo(dirigido=True)
for u, v in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]:
    dag.agregar_arista(u, v)

# Ciclo de tres vértices
ciclo = Grafo(dirigido=True)
for u, v in [("A", "B"), ("B", "C"), ("C", "A")]:
    ciclo.agregar_arista(u, v)

# Ciclo de un solo vértice (autobucle)
autociclo = Grafo(dirigido=True)
autociclo.agregar_arista("X", "X")

# Dos componentes: una sin ciclo (P→Q→R) y otra con ciclo (M→N→O→N)
mixto = Grafo(dirigido=True)
for u, v in [("P", "Q"), ("Q", "R"), ("M", "N"), ("N", "O"), ("O", "N")]:
    mixto.agregar_arista(u, v)

for nombre, g_dir in [("DAG (rombo)", dag), ("ciclo A-B-C", ciclo),
                      ("autociclo", autociclo), ("mixto", mixto)]:
    print(f"{nombre:<14} → tiene ciclo: {g_dir.tiene_ciclo()}")

assert dag.tiene_ciclo() is False
assert ciclo.tiene_ciclo() is True
assert autociclo.tiene_ciclo() is True
assert mixto.tiene_ciclo() is True

# Caso de error: grafo no dirigido
try:
    no_dirigido = Grafo()
    no_dirigido.agregar_arista("A", "B")
    no_dirigido.tiene_ciclo()
    raise AssertionError("Debió lanzar ValueError")
except ValueError as e:
    print("\nError esperado en no dirigidos:", e)

print("\n✅ Detección de ciclos correcta")
