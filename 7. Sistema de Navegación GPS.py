import heapq, math, os, unicodedata
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# país: (lat, lon) aproximada de su capital, solo para dibujar
POS = {"Guatemala": (14.63, -90.51), "El Salvador": (13.69, -89.22), "Honduras": (14.07, -87.19),
       "Nicaragua": (12.13, -86.27), "Costa Rica": (9.93, -84.08), "Panamá": (8.98, -79.52)}
# carreteras: (origen, destino, minutos aproximados)
RUTAS = [("Guatemala", "El Salvador", 240), ("El Salvador", "Honduras", 300),
         ("Guatemala", "Honduras", 360), ("Honduras", "Nicaragua", 540),
         ("Nicaragua", "Costa Rica", 540), ("Costa Rica", "Panamá", 840)]
ALIAS = {"salvador": "El Salvador"}
CARPETA = r"C:\Users\Seong JeUC\Videos\U10\Imagen Grafo"

def clave(t):
    t = "".join(c for c in unicodedata.normalize("NFKD", t) if not unicodedata.combining(c))
    return " ".join(t.lower().split())

NOMBRES = {clave(n): n for n in POS} | {clave(a): v for a, v in ALIAS.items()}
ADJ = {n: {} for n in POS}
for a, b, m in RUTAS:
    ADJ[a][b] = ADJ[b][a] = m

def buscar(t):
    if clave(t) not in NOMBRES:
        raise ValueError(f"'{t}' no es un país. Usa la opción 1 para ver la lista.")
    return NOMBRES[clave(t)]

def ruta(origen, destino):
    o, d = buscar(origen), buscar(destino)
    dist, previo, cola = {n: math.inf for n in ADJ}, {}, [(0, o)]
    dist[o] = 0
    while cola:
        c, u = heapq.heappop(cola)
        if c > dist[u]:
            continue
        for v, m in ADJ[u].items():
            if c + m < dist[v]:
                dist[v], previo[v] = c + m, u
                heapq.heappush(cola, (c + m, v))
    if dist[d] == math.inf:
        raise ValueError(f"No hay carreteras entre {o} y {d}.")
    camino = [d]
    while camino[-1] != o:
        camino.append(previo[camino[-1]])
    return dist[d], camino[::-1]

def dibujar(camino=None, archivo="grafo_gps_centroamerica.png"):
    fig, ax = plt.subplots(figsize=(11, 8))
    en_ruta = set(zip(camino, camino[1:])) | set(zip(camino[1:], camino)) if camino else set()
    for a in ADJ:
        for b, m in ADJ[a].items():
            if a < b:
                r = (a, b) in en_ruta
                (la, oa), (lb, ob) = POS[a], POS[b]
                ax.plot([oa, ob], [la, lb], "#d64545" if r else "#9aa5b1", lw=4 if r else 1.5)
                ax.text((oa + ob) / 2, (la + lb) / 2, f"{m:g} min", fontsize=8, ha="center",
                        bbox=dict(fc="white", ec="none", alpha=0.85))
    for n, (la, lo) in POS.items():
        ax.scatter(lo, la, s=400, zorder=3, color="#d64545" if camino and n in camino else "#2f80ed")
        ax.text(lo, la - 0.35 if n == "El Salvador" else la + 0.3, n, fontsize=10, fontweight="bold", ha="center")
    titulo = "Carreteras entre países de Centroamérica (tiempos aproximados)"
    if camino:
        titulo += f"\nRuta: {' → '.join(camino)}"
    ax.set_title(titulo)
    ax.set_aspect("equal")
    ax.axis("off")
    try:
        os.makedirs(CARPETA, exist_ok=True)
        ruta_archivo = os.path.join(CARPETA, archivo)
        fig.savefig(ruta_archivo, dpi=150, bbox_inches="tight")
        print(f"Imagen guardada: {ruta_archivo}")
    except OSError as e:
        print(f"No se pudo guardar: {e}")
    finally:
        plt.close(fig)

if __name__ == "__main__":
    camino = None
    while True:
        print("\n1. Ver países\n2. Agregar carretera\n3. Ruta más rápida\n4. Guardar imagen\n0. Salir")
        op = input("Opción: ").strip()
        if op == "0":
            break
        try:
            if op == "1":
                print(", ".join(sorted(ADJ)))
            elif op == "2":
                a, b = buscar(input("Origen: ")), buscar(input("Destino: "))
                m = float(input("Minutos: "))
                if m <= 0 or a == b:
                    raise ValueError("Minutos positivos y países distintos.")
                ADJ[a][b] = ADJ[b][a] = m
                print("Listo.")
            elif op == "3":
                total, camino = ruta(input("Origen: "), input("Destino: "))
                print(" → ".join(camino), f"| {total:g} min")
            elif op == "4":
                dibujar(camino)
            else:
                print("?")
        except (ValueError, OSError) as e:
            print("Error:", e)
    dibujar(camino)
