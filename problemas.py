#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
problemas.py
------------

Tarea sobre búsquedas, donde lo que es importante es crear nuevas heurísticas

"""

import busquedas



# ------------------------------------------------------------
#  Desarrolla el modelo del Camión mágico
# ------------------------------------------------------------

class PbCamionMagico(busquedas.ProblemaBusqueda):
    """
    ---------------------------------------------------------------------------------
     Supongamos que quiero trasladarme desde la posición discreta $1$ hasta 
     la posicion discreta $N$ en una vía recta usando un camión mágico. 
    
     Puedo trasladarme de dos maneras:
      1. A pie, desde el punto $x$ hasta el punto $x + 1$ en un tiempo de 1 minuto.
      2. Usando un camión mágico, desde el punto $x$ hasta el punto $2x$ con un tiempo 
         de 2 minutos.

     Desarrollar la clase del modelo del camión mágico
    ----------------------------------------------------------------------------------
    
    """
    def __init__(self, meta=100):
        """
        Constructor del problema del camión mágico.

        Modelamos:
            - El estado como un entero x ≥ 1 que representa la posición actual.
            - El objetivo como el entero N almacenado en self.meta.

        @param meta: Posición objetivo N a la que queremos llegar.

        """
        self.meta = int(meta)

    def acciones(self, estado):
        """
        Lista de acciones legales en un estado dado.

        Desde la posición x se puede:
            - Avanzar a pie a x + 1 (acción 'A') si x < meta.
            - Tomar el camión mágico a 2x (acción 'C') si 2x <= meta.
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
        Estado sucesor y costo local al aplicar una acción.

        - 'A': caminar de x a x + 1 con costo 1.
        - 'C': tomar el camión mágico de x a 2x con costo 2.
        """
        x = estado
        if accion == 'A':
            return x + 1, 1
        if accion == 'C':
            return 2 * x, 2
        raise ValueError(f"Acción desconocida: {accion}")

    def terminal(self, estado):
        """
        Determina si se alcanzó la posición objetivo.
        """
        return estado == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

        """
        return f"Posición actual: {estado}"
 

# ------------------------------------------------------------
#  Desarrolla una política admisible.
# ------------------------------------------------------------

def h_1_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------

def h_2_camion_magico(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0

# ------------------------------------------------------------
#  Desarrolla el modelo del cubo de Rubik
# ------------------------------------------------------------

class PbCuboRubik(busquedas.ProblemaBusqueda):
    """
    La clase para el modelo de cubo de rubik, documentación, no olvides poner
    la documentación de forma clara y concisa.
    
    https://en.wikipedia.org/wiki/Rubik%27s_Cube
    
    """
    def __init__(self, meta=None):
        """
        Modelo simplificado de un “cubo de Rubik” 2D.

        Representamos el estado como una tupla de 9 enteros que describen
        un tablero 3x3:
            (c0, c1, c2,
             c3, c4, c5,
             c6, c7, c8)

        El estado meta por omisión es la configuración ordenada:
            (1, 2, 3, 4, 5, 6, 7, 8, 9)
        """
        self.meta = tuple(meta) if meta is not None else (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def acciones(self, estado):
        """
        Acciones legales en el “cubo”.

        Permitimos las siguientes acciones:
            - 'F0', 'F1', 'F2': rotar cíclicamente la fila 0, 1 o 2 a la derecha.
            - 'C0', 'C1', 'C2': rotar cíclicamente la columna 0, 1 o 2 hacia abajo.
        """
        return ['F0', 'F1', 'F2', 'C0', 'C1', 'C2']

    def sucesor(self, estado, accion):
        """
        Genera el sucesor aplicando una rotación de fila o columna.

        @param estado: Tupla de longitud 9.
        @param accion: Cadena en {'F0','F1','F2','C0','C1','C2'}.
        @return: (estado_sucesor, costo_local), con costo_local = 1.
        """
        s = list(estado)

        if accion[0] == 'F':
            fila = int(accion[1])
            i = 3 * fila
            # Rotación a la derecha de la fila (c0,c1,c2) -> (c2,c0,c1)
            s[i], s[i + 1], s[i + 2] = s[i + 2], s[i], s[i + 1]

        elif accion[0] == 'C':
            col = int(accion[1])
            # Índices de la columna col: (col, col+3, col+6)
            i0, i1, i2 = col, col + 3, col + 6
            # Rotación hacia abajo: (c0,c1,c2) -> (c2,c0,c1)
            s[i0], s[i1], s[i2] = s[i2], s[i0], s[i1]
        else:
            raise ValueError(f"Acción desconocida: {accion}")

        return tuple(s), 1

    def terminal(self, estado):
        """
        Verifica si se alcanzó el estado meta.
        """
        return tuple(estado) == self.meta

    @staticmethod
    def bonito(estado):
        """
        El prettyprint de un estado dado

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
    DOCUMENTA LA HEURÍSTICA QUE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0


# ------------------------------------------------------------
#  Desarrolla otra política admisible.
#  Analiza y di porque piensas que es (o no es) dominante una
#  respecto otra política
# ------------------------------------------------------------
def h_2_problema_1(nodo):
    """
    DOCUMENTA LA HEURÍSTICA DE DESARROLLES Y DA UNA JUSTIFICACIÓN
    PLATICADA DE PORQUÉ CREES QUE LA HEURÍSTICA ES ADMISIBLE

    """
    return 0



def compara_metodos(problema, pos_inicial, heuristica_1, heuristica_2):
    """
    Compara en un cuadro lo nodos expandidos y el costo de la solución
    de varios métodos de búsqueda

    @param problema: Un objeto del tipo ProblemaBusqueda
    @param pos_inicial: Una tupla con una posicion inicial
    @param heuristica_1: Una función de heurística
    @param heuristica_2: Una función de heurística

    """
    solucion1 = busquedas.busqueda_A_estrella(problema, heuristica_1, pos_inicial)
    solucion2 = busquedas.busqueda_A_estrella(problema, heuristica_2, pos_inicial)
    
    print('-' * 50)
    print('Método'.center(12) + 'Costo'.center(18) + 'Nodos visitados'.center(20))
    print('-' * 50 + '\n')
    print('A* con h1'.center(12) 
          + str(solucion1.costo).center(18) 
          + str(solucion1.nodos_visitados))
    print('A* con h2'.center(12) 
          + str(solucion2.costo).center(20) 
          + str(solucion2.nodos_visitados))
    print('-' * 50 + '\n')


if __name__ == "__main__":

    # Compara los métodos de búsqueda para el problema del camión mágico
    # con las heurísticas que desarrollaste
    pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCamionMagico( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, pos_inicial, h_1_camion_magico, h_2_camion_magico)
    
    # Compara los métodos de búsqueda para el problema del cubo de rubik
    # con las heurísticas que desarrollaste
    pos_inicial = XXXXXXXXXX  # <--- PONLE LA POSICIÓN INICIAL QUE QUIERAS
    problema = PbCuboRubik( XXXXXXXXXX )  # <--- PONLE LOS PARÁMETROS QUE NECESITES
    compara_metodos(problema, h_1_problema_1, h_2_problema_1)
    