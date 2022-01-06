import random as rd
import numpy as np
from queue import PriorityQueue
import pygame
import math

blanco = (255, 255, 255)
negro = (0, 0, 0)
gris = (205, 205, 205)
radio=5
min_dist=20
size_x=600
size_y=300

# Creamos la clase Nodo
class Nodo:
    def __init__(self, id):
        self.id = id
        self.grado = 0
        self.visitado = False
        self.vecinos = []
        self.padre = None
        self.distancia = float('inf')
        self.coordenadas=[rd.randint(1,size_x),rd.randint(1,size_y)] #x,y
        self.color=gris

    def __str__(self):
        return str(self.id)


# Creamos la clase Arista
class Arista:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.id = str(a) + ' -> ' + str(b)
        self.peso = rd.randint(100, 500)

    def __str__(self):
        return str(self.id)

    def __lt__(self, otraArista):
        return self.peso < otraArista.peso


# Creamos la clase Grafo
class Grafo:
    def __init__(self, id="Graph"):
        self.id = id
        self.nodos = {}
        self.aristas = {}
        self.pariente = []
        self.nivel = []

    def agregarnodo(self, v):
        if not v in self.nodos:
            self.nodos[v] = Nodo(v)
            # print("nodos:", self.nodos[v].id)

    def agregararista(self, a, b):
        if a in self.nodos and b in self.nodos:
            new = Arista(self.nodos[a], self.nodos[b])
            self.aristas[new.id] = new
            self.nodos[a].grado += 1
            self.nodos[b].grado += 1
            print("nodos_surce: ", self.nodos[a].grado)
            print("nodos_target: ", self.nodos[b].grado)
            print("aris_id: ", self.aristas[new.id])
            print("arista_peso", self.aristas[new.id].peso, "\n")

    def nodo_krusk_prim(self, nodo_kru_prim):
        self.nodos[nodo_kru_prim.id] = nodo_kru_prim

    def arista_krusk_prim(self, aris_kru_prim):
        self.aristas[aris_kru_prim.id] = aris_kru_prim

    def ariname(self, a):
        if self.pariente[a] == a:
            return a
        return self.ariname(self.pariente[a])

    def distancia(self, lista):
        if len(lista) > 0:
            m = self.nodos[lista[0]].distancia
            print("m1", m)
            v = lista[0]
            for e in lista:
                print("e", e)
                if m > self.nodos[e].distancia:
                    m = self.nodos[e].distancia
                    v = e
                    print("m", m)
                    print("v", v)
            return v

    def dijkstra(self, a):
        if a in self.nodos:
            self.nodos[a].distancia = 0  # Actualiza la dist del nodo padre = 0
            actual = a
            nodvisitado = []  # Conjunto de nodos

            for v in self.nodos:
                if v != a:
                    self.nodos[v].distancia = float('inf')  # los nodos previamente identifi se asigna valor inf peso
                nodvisitado.append(v)
                # print("distancia", self.nodos[v].distancia)
                # print("padre", self.nodos[v].padre)
                # print("vecinos", self.nodos[v].vecinos)
                # print("nodovisit", nodvisitado)
                # print("visitado", self.nodos[v].visitado, "\n")

            while len(nodvisitado) > 0:  # Mientras la cola no este vacia
                for vecino in self.nodos[actual].vecinos:
                    print("vecino0", vecino[0], "vecino1", vecino[1])
                    if self.nodos[vecino[0]].visitado == False:
                        if self.nodos[vecino[0]].distancia > self.nodos[actual].distancia + vecino[1]:
                            self.nodos[vecino[0]].distancia = self.nodos[actual].distancia + vecino[1]
                            self.nodos[vecino[0]].padre = actual
                            print("test1", self.nodos[vecino[0]].distancia)
                            print("test2", self.nodos[vecino[0]].padre)
                self.nodos[actual].visitado = True
                nodvisitado.remove(actual)
                actual = self.distancia(nodvisitado)
            print("actual", actual)
        else:
            return False

    def Kruskal_D(self):
        name = self.id + ' Kruskal'
        graph_kru = Grafo(name)
        q = PriorityQueue()
        nod = len(self.nodos) + 1

        for a in range(nod):
            self.pariente.append(False)
            self.nivel.append(float('inf'))

        for key, value in self.nodos.items():
            self.pariente[value.id] = value.id
            self.nivel[value.id] = 0

        for ar in self.aristas:  # Se ordena las aristas por peso
            q.put(self.aristas[ar])
            # uu = q.get()
            # print("uu", uu.weight)
        Costo_MST = 0
        for key, value in self.nodos.items():
            graph_kru.nodo_krusk_prim(self.nodos[value.id])
        while not q.empty():
            u = q.get()
            raiz_1 = self.ariname(u.a.id)
            raiz_2 = self.ariname(u.b.id)

            if raiz_1 != raiz_2:
                graph_kru.arista_krusk_prim(u)
                Costo_MST += u.peso
                if self.nivel[raiz_1] < self.nivel[raiz_2]:
                    self.pariente[raiz_1] = raiz_2
                    self.nivel[raiz_2] += 1
                else:
                    self.pariente[raiz_2] = raiz_1
                    self.nivel[raiz_1] += 1

        print('MST:', Costo_MST)
        return graph_kru

    def prim(self):

        visitado = []
        nod_dist = []
        name = self.id + ' prim'
        graph_prim = Grafo(name)
        nod = len(self.nodos) + 1

        for a in range(nod):
            visitado.append(False)
            nod_dist.append(float('inf'))

        n = int(input("Con cual nodo inicializa prim:"))
        q = PriorityQueue()
        Costo_MST = 0
        q.put((0, n))  # distancia, nodo
        print("q", q.queue)

        while not q.empty():
            peso, nodo = q.get()
            if visitado[nodo]:
                continue
            Costo_MST += peso
            visitado[nodo] = True
            vecinos = self.Vecinos(nodo)

            for vecino in vecinos:
                peso_arista = self.peso_prim(nodo, vecino)

                if (not visitado[vecino]) and (nod_dist[vecino] > peso_arista):
                    q.put((peso_arista, vecino))
                    nod_dist[vecino] = peso_arista
                    self.nodos[vecino].padre = nodo
        for key, value in self.nodos.items():
            graph_prim.nodo_krusk_prim(self.nodos[value.id])
            if value.padre != None:
                if self.valido_arist(value.id, value.padre):
                    nueva_arista = self.arista_prim(value.id, value.padre)
                    graph_prim.arista_krusk_prim(nueva_arista)

        print('Prim - MST costo:', Costo_MST)
        return graph_prim

    def Vecinos(self, nodo):
        nod_conect = []
        for key, value in self.aristas.items():
            if value.a == self.nodos[nodo]:
                nod_conect.append(int(str(value.b)))
            if value.b == self.nodos[nodo]:
                nod_conect.append(int(str(value.a)))
        return nod_conect

    def valido_arist(self, a, b):
        arist1 = Arista(self.nodos[a], self.nodos[b])
        arist2 = Arista(self.nodos[b], self.nodos[a])
        if arist1.id in self.aristas:
            return True
        if arist2.id in self.aristas:
            return True
        return False

    def peso_prim(self, a, b):
        arist1 = Arista(self.nodos[a], self.nodos[b])
        arist2 = Arista(self.nodos[b], self.nodos[a])
        if arist1.id in self.aristas:
            return self.aristas[arist1.id].peso
        if arist2.id in self.aristas:
            return self.aristas[arist2.id].peso

    def arista_prim(self, a, b):
        arist1 = Arista(self.nodos[a], self.nodos[b])
        arist2 = Arista(self.nodos[b], self.nodos[a])
        if arist1.id in self.aristas:
            return self.aristas[arist1.id]
        if arist2.id in self.aristas:
            return self.aristas[arist2.id]

    def Ghephi(self):

        val = 'digraph example{\n'
        for key, value in self.aristas.items():
            val += value.id+'[label= '+'"'+str(value.peso)+'"'+'];\n'
        val += "}\n"
        nombre = self.id+'.dot'
        file = open(nombre, "w")
        file.write(val)
        file.close()
    # --------------------------------PYGAME---------------------------------------------

    def pinta_nodo(self,imagen):
        for aa, bb in self.nodos.items():
            pygame.draw.circle(imagen, bb.color, (bb.coordenadas[0], bb.coordenadas[1]), radio)

    def pinta_arist(self, imagen):
        for aa, bb in self.aristas.items():
            pygame.draw.line(imagen, negro, (bb.a.coordenadas[0], bb.a.coordenadas[1]),
                             (bb.b.coordenadas[0], bb.b.coordenadas[1]))

    def calcula_Spring(self):

        for a, b in self.nodos.items():
            vecinos = self.nodos[b.id].vecinos
            eje_x = 0
            eje_y = 0

            for a1, b1 in self.nodos.items():
                if b.id == b1.id:
                    continue
                if b1.id not in vecinos:
                    d = math.sqrt((b1.coordenadas[0] - b.coordenadas[0]) ** 2 + (
                                b1.coordenadas[1] - b.coordenadas[1]) ** 2)
                    if d < 30:
                        continue
                    else:
                        # Atraccion nodos
                        d = math.sqrt((b1.coordenadas[0]-b.coordenadas[0])**2+(b1.coordenadas[1]-b.coordenadas[1])**2)
                        if d == 0:
                            continue
                        tracc = .06 / math.sqrt(d)
                        radians = math.atan2(b1.coordenadas[1]-b.coordenadas[1], b1.coordenadas[0]-b.coordenadas[0])
                        eje_x += tracc*math.cos(radians)
                        eje_y += tracc*math.sin(radians)

            b.coordenadas[0] += 1 * eje_x

            b.coordenadas[1] += 1 * eje_y

    def actualiza_Grafo(self, imagen):

        imagen.fill(blanco)
        self.pinta_arist(imagen)
        self.pinta_nodo(imagen)
        pygame.display.update()
        self.calcula_Spring()

    def Spring_Grafo(self):

        size_x = 800
        size_y = 500

        imagen = pygame.display.set_mode((size_x, size_y))

        play = True
        paused = False

        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
            if not paused:
                self.actualiza_Grafo(imagen)


# Creamos clase algoritmos
class algoritmos:
    def __int__(self):
        self.Listas = []

    def malla(self, m, n):
        g = Grafo()
        m = n * n
        print("total nodos", m)

        for i in range(1, m + 1):
            g.agregarnodo(i)

        for i in range(1, m):
            # print("i", i)
            if not i % n == 0:
                g.agregararista(i, i + 1)
            if i + n <= m:
                g.agregararista(i, i + n)
        return g

    def erdos(self, n):

        g = Grafo()
        graf = []
        for i in range(n):
            g.agregarnodo(i)
        count = 0
        while (count < n):
            nodo1 = rd.randint(0, n - 1)
            nodo2 = rd.randint(0, n - 1)
            if nodo1 == nodo2:
                continue
            if not g.arista_prim(nodo1, nodo2):
                g.agregararista(nodo1, nodo2)
                count += 1
        return g

    def gilbert(self, n, a):

        g = Grafo()

        for i in range(n):
            g.agregarnodo(i)

        for i in range(n):
            for j in range(n):
                if rd.random() < a:
                    if i == j:
                        continue
                    if not g.arista_prim(i, j):
                        g.agregararista(i, j)
        return g

    def geo(self, n, r):

        g = Grafo()

        if n == 0:
            return g

        coordenadas = {}

        for i in range(n):
            g.agregarnodo(i)
            coordenadas[i] = [rd.random(), rd.random()]


        for i in range(n):
            origen = coordenadas[i]
            for j in range(n):
                destino = coordenadas[j]

                distancia = ((destino[0] - origen[0]) ** 2 + (destino[1] - origen[1]) ** 2) ** 0.5

                if not distancia <= r:
                    continue

                if i == j:
                    continue
                if not g.arista_prim(i, j):
                    g.agregararista(i, j)

        return g

    def bara(self, n, a):

        g = Grafo()
        var = []

        for i in range(n):
            g.agregarnodo(i)

        for j in range(1, n + 1):
            # print("j", j)
            var.append(j)
            rd.shuffle(var)
            for k in range(j):
                # print("k", k)
                grad = var[k]
                p = 1 - (grad / a)
                # print("p", p)
                if rd.random() < p:
                    if var[k] == j:
                        continue
                    g.agregararista(j, k)
        return g


# Creamos la clase principal
class Main:
    h = algoritmos()

    # listDij = []
    h = algoritmos()
    g = Grafo()
    # peso = []
    # listDij = []

    # n = int(input("introduzca el numero de nodos:"))
    # a = int(input("introduzca el numero de aristas por nodo:"))
    # a = float(input("introduzca el rango de cobertura (0-1):"))
    n = int(input("valor de malla nxn: "))

    grafo = h.malla(n, n)  # cambia depende el algoritmo
    print("grafo_nombre:", grafo.id)
    print("grafo_nodos:", len(grafo.nodos.items()))
    print("grafo_aristas:", len(grafo.aristas.items()))
    grafo.Ghephi()
    grafo.Spring_Grafo()

    '''graph_krus = grafo.Kruskal_D()
    print("graph_krus_nombre:", graph_krus.id)
    print("graph_krus_nodos:", len(graph_krus.nodos.items()))
    print("graph_krus_aristas:", len(graph_krus.aristas.items()))
    graph_krus.Ghephi()

    graph_prim = grafo.prim()
    print("graph_prim_nombre:", graph_prim.id)
    print("graph_prim_nodos:", len(graph_prim.nodos.items()))
    print("ggraph_prim_aristas:", len(graph_prim.aristas.items()))
    graph_prim.Ghephi()'''


Main()
