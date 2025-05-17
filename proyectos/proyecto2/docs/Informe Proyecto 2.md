# Informe Proyecto 2

Este proyecto implementa la aplicación de varios algoritmos de búsqueda para generar un laberinto y resolverlo. 
La estructura del proyecto está contenida dentro del directorio:

- ```bash
   proyectos/proyecto2
   ```

  Para ejecutar los programas, se recomienda [**clonar el repositorio**](https://github.com/JosueSay/IntelligenceArtificial). Se deben instalar las dependencias necesarias ejecutando el siguiente comando:

- ```bash
   pip install -r requirements.txt
   ```

Una vez instalado todo, se ejecutar los archivos del `interfaz.py`, `Problema2.py` y `Problema3.py`  con los siguientes comandos para ejecutar cada problema que se menciona en el informe:

- ```bash
   python Problema2.py
   python Problema3.py
   python interfaz.py
   ```


## Equivalencia Grafo-Laberinto

En el contexto de laberintos, el algoritmo permite generar en los que existe **un único camino entre cualquier par de casillas**, sin ciclos y completamente conectados siguiendo un algoritmo greedy para formar un **Árbol de expansión mínima (MST)**.

* El laberinto puede ser modelado como un grafo $G = (V, E)$, donde:
  * $V$ es el conjunto de **nodos** o **casillas** del laberinto.
  * $E$ es el conjunto de **aristas**, que representan las **conexiones posibles entre casillas adyacentes** (arriba, abajo, izquierda, derecha).
* Las **aristas seleccionadas** durante la ejecución del algoritmo forman los **caminos transitables** del laberinto.
* Las **aristas no seleccionadas** definen las **paredes** del laberinto.

### Conceptos Clave

* **Árbol de Expansión Mínima (MST):**
  Subconjunto de aristas del grafo que conecta todos los nodos (casillas) minimizando el costo total y sin formar ciclos.
* **Aristas:**
  Representan las posibles conexiones entre casillas adyacentes en el laberinto.
* **Ponderado en el Laberinto:**
  * Si el laberinto es **ponderado**, a cada posible conexión entre casillas (arista) se le asigna un **peso aleatorio**.
    Este peso influye en la estructura del laberinto, priorizando la creación de caminos con menor costo.
  * Si el laberinto es **no ponderado**, todas las conexiones tienen el mismo peso, lo que produce laberintos más balanceados y simétricos.

### Estructura del Grid y Ponderación

* En el **grid** del laberinto:
  * Un valor de **1** indica una **pared** (celda no transitable).
  * Un valor de **0** indica un **camino** (celda transitable).
* En laberintos **ponderados**:
  * Existe una estructura secundaria de pesos (`weights`), donde **solo las celdas de camino** (aquellas con grid = 0) tienen valores mayores a 0.
  * Estos valores representan el **costo de transitar** por esa casilla.
* En laberintos **no ponderados**:
  * Todas las celdas transitables tienen un peso implícito de **1**.

### Conversión de Coordenadas en el Grid

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

  donde $(r_1, c_1)$ y $(r_2, c_2)$ son las posiciones de las dos casillas adyacentes.

### Conversión de Coordenadas 2D a 1D

Para optimizar las búsquedas y gestionar la estructura de componentes conectados (Union-Find), se realiza la conversión de coordenadas 2D a un índice 1D de la siguiente forma:

$$
\text{Índice 1D} = r \cdot \text{columnas} + c
$$

Esto permite manejar las casillas de forma eficiente como un arreglo lineal.

## Algoritmo de Kruskal

El algoritmo de Kruskal es un método **greedy** utilizado para encontrar el Árbol de Expansión Mínima (MST) en un grafo. Este algoritmo ordena el peso de las aristas y conectandolos siempre y cuando sean disjuntos.

### Conceptos

* **Union-Find (Disjoint Set):** Estructura utilizada para detectar ciclos de forma eficiente durante la construcción del MST. Permite saber rápidamente si dos casillas ya están conectadas indirectamente.
* **Ponderado en el Laberinto:**
  En el contexto de la generación del laberinto, que sea **ponderado** significa que a cada conexión posible entre casillas (arista) se le asigna un **peso o costo** aleatorio. Este peso influye directamente en el orden en que se conectan las casillas.

  * Las conexiones con menor peso son preferidas, formando caminos "más baratos" en la estructura final del laberinto.
  * Esto afecta la forma y complejidad del laberinto, priorizando ciertas rutas sobre otras.
  * Si el laberinto es **no ponderado**, todas las aristas tienen el mismo peso, por lo que no hay preferencia en las conexiones, y el resultado es un laberinto más equilibrado y simétrico.

### Implementación en la Generación de Laberintos

1. **Representación del Grafo:**

   * Cada casilla es un nodo.
   * Las conexiones horizontales y verticales entre casillas son las aristas.
   * Si se trabaja con un laberinto ponderado, se asigna un peso aleatorio a cada arista. Si no, todos los pesos son iguales.

2. **Preparación de las Aristas:**

   * Se generan todas las aristas posibles entre casillas adyacentes.
   * En el caso ponderado, se asigna un peso aleatorio a cada arista utilizando una semilla para garantizar reproducibilidad.
   * Las aristas se ordenan por peso. En el caso no ponderado, se barajan aleatoriamente para aleatorizar la generación del laberinto.

3. **Construcción del Laberinto:**

   * Se recorre la lista de aristas ordenadas.
   * Se utiliza la estructura Union-Find para verificar si la inclusión de una arista formaría un ciclo. Si no forma ciclo, se incluye en el laberinto.
   * Este proceso se repite hasta incluir $|V| - 1$ aristas, donde $|V|$ es el número de casillas del laberinto.

4. **Finalización:**

   * Al finalizar, el laberinto está completamente conectado y no posee ciclos, lo que garantiza la unicidad de los caminos entre casillas.

### Formalización Matemática

Dado un conjunto de aristas $E = {e_1, e_2, ..., e_m}$ ordenado de forma no decreciente según su peso $w$, se construye el MST iterando sobre las aristas y aplicando la siguiente regla:

$$
\text{Si } e_i \text{ conecta componentes disjuntas} \Rightarrow \text{añadir } e_i \text{ al MST}
$$

Se utiliza una estructura de conjuntos disjuntos \$F\$ de forma que:

* Si $F.\text{find}(u) \neq F.\text{find}(v)$, se realiza la unión de los conjuntos:

$$
F.\text{union}(u, v)
$$

Este proceso se repite hasta que el MST contiene exactamente $|V| - 1$ aristas.


## Algoritmo de Prim

El algoritmo de **Prim** es un método **greedy** para construir un Árbol de Expansión Mínima (MST) a partir de un grafo conectado. Este algoritmo comienza desde un nodo arbitrario e **incrementalmente expande el MST** seleccionando siempre la arista de menor costo que conecta un nodo visitado con uno no visitado.

### Conceptos Clave

* **Frontera:** Conjunto de casillas adyacentes a las ya visitadas. En el código, se maneja mediante `heapq` o mezcla aleatoria, según sea ponderado o no.
* **Ponderado en el Laberinto:**
  En el contexto de la generación del laberinto, que sea **ponderado** significa que a cada conexión posible entre casillas (arista) se le asigna un **peso o costo** aleatorio. Este peso influye directamente en el orden en que se conectan las casillas.

  * Las conexiones con menor peso son preferidas, formando caminos "más baratos" en la estructura final del laberinto.
  * Esto afecta la forma y complejidad del laberinto, priorizando ciertas rutas sobre otras.
  * Si el laberinto es **no ponderado**, todas las aristas tienen el mismo peso, por lo que no hay preferencia en las conexiones, y el resultado es un laberinto más equilibrado y simétrico.
* **Cola de Prioridad:** Utilizada en el caso ponderado para seleccionar de forma eficiente la casilla con menor peso en la frontera.

### Aplicación en la Generación de Laberintos

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

### Control de Peso

* En el laberinto **ponderado**, al agregar una casilla a la frontera se le asigna un peso aleatorio. Esto afecta directamente la estructura del laberinto, generando caminos que siguen rutas de menor costo.
* En el laberinto **no ponderado**, todas las aristas tienen el mismo peso, por lo que las elecciones son completamente aleatorias.

### Formalización

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


