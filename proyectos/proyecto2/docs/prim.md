
# Algoritmo de Prim

El algoritmo de **Prim** es un método **greedy** para construir un Árbol de Expansión Mínima (MST) a partir de un grafo conectado. Este algoritmo comienza desde un nodo arbitrario e **incrementalmente expande el MST** seleccionando siempre la arista de menor costo que conecta un nodo visitado con uno no visitado.

## Conceptos Clave

* **Frontera:** Conjunto de casillas adyacentes a las ya visitadas. En el código, se maneja mediante `heapq` o mezcla aleatoria, según sea ponderado o no.
* **Ponderado en el Laberinto:**
  En el contexto de la generación del laberinto, que sea **ponderado** significa que a cada conexión posible entre casillas (arista) se le asigna un **peso o costo** aleatorio. Este peso influye directamente en el orden en que se conectan las casillas.

  * Las conexiones con menor peso son preferidas, formando caminos "más baratos" en la estructura final del laberinto.
  * Esto afecta la forma y complejidad del laberinto, priorizando ciertas rutas sobre otras.
  * Si el laberinto es **no ponderado**, todas las aristas tienen el mismo peso, por lo que no hay preferencia en las conexiones, y el resultado es un laberinto más equilibrado y simétrico.
* **Cola de Prioridad:** Utilizada en el caso ponderado para seleccionar de forma eficiente la casilla con menor peso en la frontera.

## Aplicación en la Generación de Laberintos

En la generación de laberintos, los nodos corresponden a las casillas del laberinto y las aristas a las posibles conexiones entre casillas adyacentes.

Prim construye el laberinto de la siguiente forma:

1. Se inicia desde una casilla aleatoria, marcándola como parte del camino.
2. Se identifican sus vecinos no visitados y se colocan en la **frontera** (estructura de prioridad).
3. En cada iteración:

   * Si el laberinto es **ponderado**, se elige la casilla de la frontera con el menor peso.
   * Si es **no ponderado**, la frontera se mezcla aleatoriamente y se elige cualquier casilla disponible.
4. Se conecta la casilla seleccionada a una casilla ya visitada, formando un camino.
5. Se actualiza la frontera con los vecinos de la nueva casilla añadida.
6. Se repite hasta que todas las casillas estén conectadas.

El algoritmo utiliza una **cola de prioridad** (`heapq`) para mantener las casillas frontera ordenadas por su peso en el caso ponderado, y una simple lista con mezcla aleatoria en el caso no ponderado.

## Control de Peso

* En el laberinto **ponderado**, al agregar una casilla a la frontera se le asigna un peso aleatorio. Esto afecta directamente la estructura del laberinto, generando caminos que siguen rutas de menor costo.
* En el laberinto **no ponderado**, todas las aristas tienen el mismo peso, por lo que las elecciones son completamente aleatorias.

## Formalización

Sea $V$ el conjunto de nodos (casillas) y $E$ el conjunto de aristas (posibles conexiones).
El algoritmo de Prim sigue estos pasos:

1. Inicializar $key[v] = \infty$ para todo $v \in V$, excepto el nodo de inicio $s$ donde $key[s] = 0$.
2. Mientras existan nodos no incluidos en el MST:

   * Seleccionar $u$ tal que $key[u]$ sea mínimo.
   * Agregar $u$ al MST.
   * Para cada vecino $v$ de $u$, si $v$ no está en el MST y $(u, v)$ es una arista válida:

     $$
     key[v] = \min(key[v], w(u, v))
     $$
