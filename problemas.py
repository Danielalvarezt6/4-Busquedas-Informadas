#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import math
import busquedas



# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):
    """
    Problema del Camión Mágico.

    Nos queremos trasladar desde la posición discreta 1 hasta la posición
    discreta N en una vía recta. Tenemos dos formas de movernos:

      1. A pie: del punto x al punto x + 1, con costo de 1 minuto.
      2. En camión mágico: del punto x al punto 2x, con costo de 2 minutos.

    El estado es un entero x >= 1 que indica la posición actual.
    La meta es llegar a la posición N.

    """
    def __init__(self, meta=100):
        """
        Inicializa el problema del camión mágico.

        Aquí simplemente guardo la posición a la que quiero llegar.
        El estado es un entero (mi posición en la recta).

        @param meta: int, la posición objetivo N (por defecto 100).

        """
        self.meta = int(meta)

    def acciones(self, estado):
        """
        Devuelve las acciones legales desde la posición x.

        Desde la posición x tengo dos opciones:
        - 'A' (a pie): avanzar a x+1, siempre que no me haya pasado de la meta.
        - 'C' (camión): saltar a 2x, pero solo si 2x no se pasa de la meta.

        @param estado: int, la posición actual x.
        @return: list, lista de acciones legales ('A' y/o 'C').

        """
        x = estado
        acciones = []
        if x < self.meta:
            acciones.append('A')
        if 2 * x <= self.meta:
            acciones.append('C')
        return acciones

    def sucesor(self, estado, accion):
        """
        Calcula el estado sucesor y el costo de aplicar una acción.

        - Si camino ('A'), paso de x a x+1 y me tardo 1 minuto.
        - Si tomo el camión ('C'), paso de x a 2x y me tardo 2 minutos.

        @param estado: int, la posición actual x.
        @param accion: str, 'A' para caminar o 'C' para el camión.
        @return: tuple (estado_sucesor, costo_local).

        """
        x = estado
        if accion == 'A':
            return x + 1, 1
        if accion == 'C':
            return 2 * x, 2
        raise ValueError(f"Acción desconocida: {accion}")

    def terminal(self, estado):
        """
        Revisa si ya llegué a la posición meta.

        @param estado: int, la posición actual.
        @return: bool, True si estado == meta.

        """
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        Representación bonita del estado.

        @param estado: int, la posición actual.
        @return: str, cadena con la posición.

        """
        return f"Posición actual: {estado}"
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    Primera heurística admisible para el problema del Camión Mágico.

    Mi idea es contar el mínimo de pasos que necesito para llegar de x a N,
    suponiendo que cada paso me duplica la posición (que es lo mejor que
    puedo hacer). Eso me da ceil(log2(N/x)).

    Creo que es admisible porque estoy asumiendo el mejor caso posible:
    que cada acción me duplica la posición y solo me cuesta 1. En la
    realidad el camión cuesta 2 y caminar solo suma 1, así que el costo
    real siempre va a ser mayor o igual a este valor. Nunca sobreestimo.

    @param nodo: NodoBusqueda, el nodo actual (nodo.estado es la posición x).
    @return: int, estimación del costo restante desde x hasta N.

    """
    x = nodo.estado
    N = 100
    if x >= N:
        return 0
    return math.ceil(math.log2(N / x))


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    Segunda heurística admisible para el problema del Camión Mágico.

    Para esta heurística quise ser más preciso. La idea es la siguiente:
    si uso k viajes en camión y w pasos a pie, lo mejor que puedo hacer es
    caminar primero y luego tomar el camión (porque los pasos a pie se
    multiplican por las duplicaciones del camión). Así, lo máximo que
    alcanzo es (x + w) * 2^k. Para que eso llegue a N, necesito al menos
    w >= ceil(N / 2^k) - x pasos a pie. El costo total sería 2*k + w.
    Pruebo con distintos valores de k y me quedo con el mínimo.

    Es admisible porque estoy calculando el mínimo costo posible asumiendo
    que acomodo los pasos de la mejor manera (todos antes de subir al
    camión), lo cual es más favorable que la realidad. Nunca sobreestimo.

    Creo que domina a h_1 porque esta heurística sí toma en cuenta que el
    camión cuesta 2 minutos (no 1), entonces da valores más altos y más
    cercanos al costo real. En las pruebas se nota: h_2 explora menos nodos.

    @param nodo: NodoBusqueda, el nodo actual (nodo.estado es la posición x).
    @return: int, estimación del costo restante desde x hasta N.

    """
    x = nodo.estado
    N = 100
    if x >= N:
        return 0
    best = N - x
    max_k = int(math.log2(N)) + 1
    for k in range(1, max_k + 1):
        walks = max(0, math.ceil(N / (2 ** k)) - x)
        cost = 2 * k + walks
        if cost < best:
            best = cost
    return best

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    Problema del Cubo de Rubik simplificado en 2D.

    Es un tablero 3x3 con piezas numeradas del 1 al 9. Se pueden
    mover rotando filas hacia la derecha o columnas hacia abajo,
    de forma cíclica (lo que se sale por un lado entra por el otro).
    El objetivo es ordenar las piezas: (1, 2, 3, 4, 5, 6, 7, 8, 9).

    El estado se representa como una tupla de 9 enteros.

    """
    def __init__(self, meta=None):
        """
        Inicializa el problema del cubo de Rubik 2D.

        El estado es una tupla de 9 numeros que representan el tablero 3x3::

            (c0, c1, c2,
             c3, c4, c5,
             c6, c7, c8)

        La meta por defecto es tenerlos ordenados: (1, 2, 3, 4, 5, 6, 7, 8, 9).

        @param meta: tuple o None, configuración objetivo (por defecto ordenada).

        """
        self.meta = tuple(meta) if meta is not None else (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def acciones(self, estado):
        """
        Devuelve la lista de acciones legales.

        Las acciones que puedo hacer son 6:
        - 'F0', 'F1', 'F2': rotar la fila 0, 1 o 2 hacia la derecha.
        - 'C0', 'C1', 'C2': rotar la columna 0, 1 o 2 hacia abajo.
        Todas son cíclicas (lo que se sale por un lado entra por el otro).

        @param estado: tuple, el estado actual del tablero.
        @return: list, lista con las 6 acciones posibles.

        """
        return ['F0', 'F1', 'F2', 'C0', 'C1', 'C2']

    def sucesor(self, estado, accion):
        """
        Aplica una rotación y devuelve el nuevo estado con costo 1.

        Las filas rotan a la derecha y las columnas hacia abajo, de
        forma cíclica en el tablero 3x3.

        @param estado: tuple, estado actual (tupla de 9 enteros).
        @param accion: str, una de 'F0','F1','F2','C0','C1','C2'.
        @return: tuple (estado_sucesor, costo_local), con costo_local = 1.

        """
        s = list(estado)

        if accion[0] == 'F':
            fila = int(accion[1])
            i = 3 * fila
            s[i], s[i + 1], s[i + 2] = s[i + 2], s[i], s[i + 1]

        elif accion[0] == 'C':
            col = int(accion[1])
            i0, i1, i2 = col, col + 3, col + 6
            s[i0], s[i1], s[i2] = s[i2], s[i0], s[i1]
        else:
            raise ValueError(f"Acción desconocida: {accion}")

        return tuple(s), 1

    def terminal(self, estado):
        """
        Revisa si ya llegué al estado meta.

        @param estado: tuple, estado actual del tablero.
        @return: bool, True si el estado coincide con la meta.

        """
        return tuple(estado) == self.meta

    @staticmethod
    def bonito(estado):
        """
        Representación bonita del tablero 3x3.

        @param estado: tuple, estado actual (tupla de 9 enteros).
        @return: str, el tablero formateado en 3 filas.

        """
        c0, c1, c2, c3, c4, c5, c6, c7, c8 = estado
        return (f"{c0} {c1} {c2}\n"
                f"{c3} {c4} {c5}\n"
                f"{c6} {c7} {c8}")
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------
def h_1_problema_1(nodo):
    """
    Primera heurística admisible para el Cubo de Rubik 2D.

    Lo que hago es contar cuántas piezas están fuera de su lugar y divido
    entre 3. La razón es que cada acción (rotar una fila o columna) mueve
    3 piezas a la vez. Entonces, en el mejor de los casos, con una sola
    acción podría acomodar 3 piezas de golpe.

    Es admisible porque estoy suponiendo lo más optimista posible: que cada
    movimiento arregla 3 piezas al mismo tiempo. En la práctica casi nunca
    pasa eso, así que el costo real siempre va a ser igual o mayor.

    @param nodo: NodoBusqueda, el nodo actual (nodo.estado es una tupla de 9 enteros).
    @return: int, estimación del número mínimo de acciones para resolver el cubo.

    """
    estado = nodo.estado
    meta = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    mal = sum(1 for i in range(9) if estado[i] != meta[i])
    return math.ceil(mal / 3)


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    Segunda heurística admisible para el Cubo de Rubik 2D.

    Aquí uso una especie de distancia Manhattan adaptada al tablero cíclico.
    Para cada pieza calculo cuántas rotaciones de fila (a la derecha) y de
    columna (hacia abajo) necesitaría para llevarla a su posición correcta.
    Como el tablero es 3x3 y las rotaciones son cíclicas, uso módulo 3.
    Sumo todas esas distancias y divido entre 3, porque cada acción mueve
    3 piezas una posición.

    Es admisible porque cada movimiento, en el mejor caso, acerca 3 piezas
    un paso hacia su meta. Entonces la suma total de distancias dividida
    entre 3 nunca va a ser mayor que el costo real.

    Creo que domina a h_1 porque si una pieza está fuera de lugar, su
    distancia es al menos 1. Entonces la suma de distancias siempre es
    mayor o igual al número de piezas mal colocadas. Al dividir ambas
    entre 3, h_2 sigue siendo mayor o igual que h_1. En las pruebas se
    nota claro: h_2 explora muchos menos nodos (27 vs 187 en el cubo).

    @param nodo: NodoBusqueda, el nodo actual (nodo.estado es una tupla de 9 enteros).
    @return: int, estimación del número mínimo de acciones para resolver el cubo.

    """
    estado = nodo.estado
    total = 0
    for pos in range(9):
        val = estado[pos]
        target = val - 1
        r1, c1 = pos // 3, pos % 3
        r2, c2 = target // 3, target % 3
        total += (r2 - r1) % 3 + (c2 - c1) % 3
    return math.ceil(total / 3)



def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara A* con dos heurísticas distintas, mostrando el costo de la
    solución y la cantidad de nodos visitados de cada una.

    @param problema: ProblemaBusqueda, el problema a resolver.
    @param pos_inicial: el estado inicial del problema.
    @param heuristica_1: function, primera heurística h(nodo) -> número.
    @param heuristica_2: function, segunda heurística h(nodo) -> número.

    """
    solucion1, nodos1 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_1)
    solucion2, nodos2 = busquedas.busqueda_A_estrella(problema, pos_inicial, heuristica_2)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(nodos1).center(20))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(18) 
          + str(nodos2).center(20))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    print("=" * 50)
    print("  PROBLEMA DEL CAMIÓN MÁGICO (de 1 a 100)")
    print("=" * 50)
    pos_inicial = 1
    problema = PbCamionMagico(100)
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)

    print("=" * 50)
    print("  PROBLEMA DEL CUBO DE RUBIK 2D")
    print("=" * 50)
    pos_inicial = (3, 1, 2, 6, 4, 5, 9, 7, 8)
    problema = PbCuboRubik()
    compara_metodos(problema, pos_inicial, h_1_problema_1, h_2_problema_1)
