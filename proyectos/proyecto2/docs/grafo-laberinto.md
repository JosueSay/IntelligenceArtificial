# Equivalencia Grafo-Laberinto

En el contexto de laberintos, el algoritmo permite generar en los que existe **un único camino entre cualquier par de casillas**, sin ciclos y completamente conectados siguiendo un algoritmo greedy para formar un **Árbol de expansión mínima (MST)**.

* El laberinto puede ser modelado como un grafo $G = (V, E)$, donde:
  * $V$ es el conjunto de **nodos** o **casillas** del laberinto.
  * $E$ es el conjunto de **aristas**, que representan las **conexiones posibles entre casillas adyacentes** (arriba, abajo, izquierda, derecha).
* Las **aristas seleccionadas** durante la ejecución del algoritmo forman los **caminos transitables** del laberinto.
* Las **aristas no seleccionadas** definen las **paredes** del laberinto.

## Conceptos Clave

* **Árbol de Expansión Mínima (MST):**
  Subconjunto de aristas del grafo que conecta todos los nodos (casillas) minimizando el costo total y sin formar ciclos.
* **Aristas:**
  Representan las posibles conexiones entre casillas adyacentes en el laberinto.
* **Ponderado en el Laberinto:**
  * Si el laberinto es **ponderado**, a cada posible conexión entre casillas (arista) se le asigna un **peso aleatorio**.
    Este peso influye en la estructura del laberinto, priorizando la creación de caminos con menor costo.
  * Si el laberinto es **no ponderado**, todas las conexiones tienen el mismo peso, lo que produce laberintos más balanceados y simétricos.

## Estructura del Grid y Ponderación

* En el **grid** del laberinto:
  * Un valor de **1** indica una **pared** (celda no transitable).
  * Un valor de **0** indica un **camino** (celda transitable).
* En laberintos **ponderados**:
  * Existe una estructura secundaria de pesos (`weights`), donde **solo las celdas de camino** (aquellas con grid = 0) tienen valores mayores a 0.
  * Estos valores representan el **costo de transitar** por esa casilla.
* En laberintos **no ponderados**:
  * Todas las celdas transitables tienen un peso implícito de **1**.

## Conversión de Coordenadas en el Grid

El laberinto se representa con un **grid de tamaño** $(2 \cdot \text{filas} + 1) \times (2 \cdot \text{columnas} + 1)$ para intercalar muros entre celdas transitables:

* **Celdas de paso (nodos del grafo):**
  Se ubican en posiciones impares del grid:

  $$
  \text{Fila}_{\text{grid}} = 2 \cdot r + 1, \quad \text{Columna}_{\text{grid}} = 2 \cdot c + 1
  $$

  donde $(r, c)$ es la posición de la casilla en coordenadas del grafo.

* **Muros o caminos entre dos celdas adyacentes:**
  La posición de la pared o camino entre dos casillas se calcula como:

  $$
  \text{Fila}_{\text{camino}} = r_1 + r_2 + 1, \quad \text{Columna}_{\text{camino}} = c_1 + c_2 + 1
  $$

  donde $(r\_1, c\_1)$ y $(r\_2, c\_2)$ son las posiciones de las dos casillas adyacentes.

## Conversión de Coordenadas 2D a 1D

Para optimizar las búsquedas y gestionar la estructura de componentes conectados (Union-Find), se realiza la conversión de coordenadas 2D a un índice 1D de la siguiente forma:

$$
\text{Índice 1D} = r \cdot \text{columnas} + c
$$

Esto permite manejar las casillas de forma eficiente como un arreglo lineal.

## Resumen de Estados de las Celdas

| Grid (Estructura) | Weights (Si ponderado) | Estado              |
| ----------------- | ---------------------- | ------------------- |
| 1                 | 0                      | Muro (Pared)        |
| 0                 | > 0                    | Camino ponderado    |
| 0                 | 0                      | Camino no ponderado |
