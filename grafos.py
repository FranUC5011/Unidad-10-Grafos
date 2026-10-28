"""
grafos.py - Librería de grafos de la Unidad 10.

Contiene las clases Grafo (no ponderado) y GrafoPonderado, con los métodos
que piden los ejercicios 5.2, 5.3, 6.1, 6.2, 6.4 y 6.5.
Importar este archivo no imprime nada.
"""
# =====================================================================
#  LIBRERÍA DE GRAFOS: Unidad 10
#  Base tomada del material; métodos nuevos marcados con su ejercicio.
# =====================================================================
from collections import deque
import heapq
import math


class Grafo:
    """Grafo no ponderado con lista de adyacencia (diccionario)."""

    def __init__(self, dirigido=False):
        self.adj = {}
        self.dirigido = dirigido

    # ---------- Operaciones básicas (material) ----------
    def agregar_vertice(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def agregar_arista(self, u, v):
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adj[u].append(v)
        if not self.dirigido:
            self.adj[v].append(u)

    def vecinos(self, v):
        return self.adj.get(v, [])

    def mostrar(self):
        for v, vecinos in self.adj.items():
            print(f"{v} -> {vecinos}")

    def _validar_vertices(self, *vertices):
        """Lanza ValueError si algún vértice no existe en el grafo."""
        for v in vertices:
            if v not in self.adj:
                raise ValueError(f"El vértice {v!r} no existe en el grafo.")

    # ---------- Recorridos (material) ----------
    def bfs(self, inicio):
        visitados = {inicio}
        cola = deque([inicio])
        resultado = []
        while cola:
            actual = cola.popleft()
            resultado.append(actual)
            for vecino in self.vecinos(actual):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        return resultado

    def dfs(self, inicio, visitados=None, resultado=None):
        if visitados is None:
            visitados = set()
            resultado = []
        visitados.add(inicio)
        resultado.append(inicio)
        for vecino in self.vecinos(inicio):
            if vecino not in visitados:
                self.dfs(vecino, visitados, resultado)
        return resultado

    # ---------- Auxiliar (usado en 5.1 y 5.2) ----------
    def transpuesto(self):
        """Copia del grafo con todas las aristas invertidas (u->v pasa a v->u)."""
        t = Grafo(dirigido=True)
        for v in self.adj:
            t.agregar_vertice(v)
        for u in self.adj:
            for v in self.vecinos(u):
                t.agregar_arista(v, u)
        return t

    # ---------- Ejercicio 5.2 ----------
    def es_conexo(self):
        """
        No dirigido: conexo si BFS desde cualquier vértice alcanza a todos.
        Dirigido: conexión fuerte (BFS en el grafo y en su transpuesto).
        """
        if not self.adj:
            return True  # convención: el grafo vacío es conexo
        inicio = next(iter(self.adj))
        n = len(self.adj)
        if len(self.bfs(inicio)) != n:
            return False
        if self.dirigido:
            return len(self.transpuesto().bfs(inicio)) == n
        return True

    # ---------- Ejercicio 5.3 ----------
    def camino_mas_corto_bfs(self, inicio, fin):
        """Ruta con menor número de saltos. Devuelve lista de vértices o None."""
        self._validar_vertices(inicio, fin)
        padre = {inicio: None}
        cola = deque([inicio])
        while cola:
            actual = cola.popleft()
            if actual == fin:
                break
            for vecino in self.vecinos(actual):
                if vecino not in padre:
                    padre[vecino] = actual
                    cola.append(vecino)
        if fin not in padre:
            return None
        camino = []
        nodo = fin
        while nodo is not None:
            camino.append(nodo)
            nodo = padre[nodo]
        return camino[::-1]

    # ---------- Tarea 6.1 ----------
    def dfs_iterativo(self, inicio):
        """DFS sin recursión, usando una pila explícita (lista LIFO)."""
        self._validar_vertices(inicio)
        visitados = set()
        resultado = []
        pila = [inicio]
        while pila:
            actual = pila.pop()
            if actual in visitados:
                continue
            visitados.add(actual)
            resultado.append(actual)
            # Se meten al revés para que el primer vecino quede arriba
            for vecino in reversed(self.vecinos(actual)):
                if vecino not in visitados:
                    pila.append(vecino)
        return resultado

    # ---------- Tarea 6.2 ----------
    def tiene_ciclo(self):
        """Detecta ciclos en un grafo dirigido usando DFS con tres colores."""
        if not self.dirigido:
            raise ValueError("tiene_ciclo() está pensado para grafos dirigidos.")
        BLANCO, GRIS, NEGRO = 0, 1, 2   # no visitado / en el camino actual / terminado
        color = {v: BLANCO for v in self.adj}

        def visitar(u):
            color[u] = GRIS
            for v in self.vecinos(u):
                if color[v] == GRIS:          # volvemos a un antecesor: ciclo
                    return True
                if color[v] == BLANCO and visitar(v):
                    return True
            color[u] = NEGRO
            return False

        return any(color[v] == BLANCO and visitar(v) for v in self.adj)

    # ---------- Tarea 6.5 ----------
    def grados(self):
        """Devuelve {vértice: (grado_entrada, grado_salida)}."""
        entrada = {v: 0 for v in self.adj}
        for u in self.adj:
            for v in self.vecinos(u):
                entrada[v] += 1
        return {v: (entrada[v], len(self.vecinos(v))) for v in self.adj}


class GrafoPonderado(Grafo):
    """Grafo con pesos. adj[u] guarda tuplas (vecino, peso)."""

    def agregar_arista(self, u, v, peso):
        if peso < 0:
            raise ValueError("Dijkstra no admite pesos negativos.")
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adj[u].append((v, peso))
        if not self.dirigido:
            self.adj[v].append((u, peso))

    def vecinos(self, v):
        """Solo los nombres de los vecinos, sin el peso (compatible con BFS/DFS)."""
        return [w for w, _ in self.adj.get(v, [])]

    def dijkstra(self, inicio):
        """Distancia mínima desde 'inicio' hasta todos los vértices."""
        self._validar_vertices(inicio)
        distancias = {v: math.inf for v in self.adj}
        distancias[inicio] = 0
        pq = [(0, inicio)]
        while pq:
            dist_actual, actual = heapq.heappop(pq)
            if dist_actual > distancias[actual]:
                continue
            for vecino, peso in self.adj[actual]:
                nueva = dist_actual + peso
                if nueva < distancias[vecino]:
                    distancias[vecino] = nueva
                    heapq.heappush(pq, (nueva, vecino))
        return distancias

    # ---------- Tarea 6.4 ----------
    def dijkstra_camino(self, origen, fin):
        """
        Devuelve (costo_minimo, [camino]) entre origen y fin.
        Si no hay camino devuelve (inf, []).
        """
        self._validar_vertices(origen, fin)
        distancias = {v: math.inf for v in self.adj}
        previo = {}
        distancias[origen] = 0
        pq = [(0, origen)]
        while pq:
            dist_actual, actual = heapq.heappop(pq)
            if dist_actual > distancias[actual]:
                continue
            if actual == fin:          # distancia ya definitiva: podemos parar
                break
            for vecino, peso in self.adj[actual]:
                nueva = dist_actual + peso
                if nueva < distancias[vecino]:
                    distancias[vecino] = nueva
                    previo[vecino] = actual
                    heapq.heappush(pq, (nueva, vecino))
        if distancias[fin] == math.inf:
            return math.inf, []
        camino = [fin]
        while camino[-1] != origen:    # reconstruir hacia atrás
            camino.append(previo[camino[-1]])
        return distancias[fin], camino[::-1]
