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

     $$key[v] = \min(key[v], w(u, v))$$

## Resolución de laberintos usando algoritmos de búsqueda

### Explicación de la implementación de los algoritmos generados: 

#### 1. Breadth-First Search (BFS)

BFS es un algoritmo de búsqueda que explora un grafo nivel por nivel, expandiendo todos los nodos vecinos antes de pasar al siguiente nivel.

##### Funcionamiento:
- Utiliza una cola (FIFO) para almacenar los nodos a explorar
- Comienza desde el nodo inicial y explora todos sus vecinos
- Continúa explorando los vecinos de cada nodo en el orden en que fueron descubiertos
- Mantiene un registro de nodos visitados para evitar ciclos

##### Características:
- **Completitud**: Garantiza encontrar una solución si existe
- **Optimalidad**: Encuentra el camino más corto en términos de número de pasos
- **Complejidad espacial**: O(b^d) donde b es el factor de ramificación y d es la profundidad
- **Complejidad temporal**: O(b^d)

#### 2. Depth-First Search (DFS)

DFS es un algoritmo que explora tan profundo como sea posible a lo largo de cada rama antes de retroceder.

##### Funcionamiento:
- Utiliza una pila (LIFO) para almacenar los nodos a explorar
- Explora completamente un camino antes de retroceder
- Mantiene un registro de nodos visitados para evitar ciclos

##### Características:
- **Completitud**: Garantiza encontrar una solución si existe (en espacios finitos)
- **Optimalidad**: No garantiza encontrar el camino más corto
- **Complejidad espacial**: O(bm) donde b es el factor de ramificación y m es la profundidad máxima
- **Complejidad temporal**: O(b^m)

#### 3. Uniform Cost Search (UCS)

UCS es una variante del algoritmo de Dijkstra que expande nodos según su costo acumulado desde el inicio.

##### Funcionamiento:
- Utiliza una cola de prioridad ordenada por el costo acumulado
- Expande siempre el nodo con menor costo acumulado
- Mantiene un registro de costos para cada nodo y actualiza si encuentra un camino más corto

##### Características:
- **Completitud**: Garantiza encontrar una solución si existe
- **Optimalidad**: Garantiza encontrar el camino de menor costo
- **Complejidad espacial**: O(b^(C*/ε)) donde C* es el costo de la solución óptima y ε es el costo mínimo entre dos nodos
- **Complejidad temporal**: O(b^(C*/ε))

#### 4. A* Search

A* es un algoritmo de búsqueda informada que combina UCS con una heurística para guiar la búsqueda.

##### Funcionamiento:
- Utiliza una cola de prioridad ordenada por f(n) = g(n) + h(n)
  - g(n): Costo acumulado desde el inicio hasta el nodo n
  - h(n): Heurística estimada del costo desde n hasta la meta
- En esta implementación, utiliza la distancia Manhattan como heurística
- Expande siempre el nodo con menor valor de f(n)

##### Características:
- **Completitud**: Garantiza encontrar una solución si existe
- **Optimalidad**: Garantiza encontrar el camino óptimo si la heurística es admisible
- **Complejidad espacial**: O(b^d), pero generalmente mejor en la práctica
- **Complejidad temporal**: O(b^d), pero generalmente mejor en la práctica
- **Eficiencia**: Normalmente explora menos nodos que algoritmos no informados


### Solución de un tablero 60x80 usando BFS

Luego de implementar lo algoritmos, se generó un laberinto de tamaño relativamente grande (60 x 80) y se decidió utilizar el algoritmo BFS para resolverlo. En promedio, estos fueron los resultados obtenidos utilizando un laberinto generado con Kruskal y con pesos: 

| Nodos explorados | Longitud camino |
|------------------|-----------------|
| 9000             | 400             |

En la mayoría de casos, el algoritmo revisaba la mayoría de los nodos para encontrar el camino hacia la salida. 

## Comparativa de Algoritmos de Búsqueda en Laberintos Aleatorios No Ponderados

Este experimento evalúa el rendimiento de cuatro algoritmos clásicos de búsqueda al resolver **laberintos no ponderados** generados **aleatoriamente**. Cada algoritmo fue ejecutado en **25 laberintos distintos por conjunto**, para un total de **100 simulaciones por algoritmo**.

Para esta parte del proyecto, se busca comparar cuatro algoritmos de búsqueda al resolver laberintos. En nuestra simulación hicimos uso de laberintos generados aleatoriamente cada una de las ejecuciones, cambiando el punto de inicio y el punto final tomando en cuenta una distancia mínima de 10 unidades manhattan entre sí. Cada algoritmo se ejecuto en 25 laberintos aleatorios y los resultados promedios fueron guardados en tablas de estadística. 

Para la clasificación de que algoritmo fue mejor tomamos en cuenta el tiempo que tardó en resolver el laberinto, y la cantidad de nodos que creó para hacerlo. 


Para cada conjunto de simulaciones se tomaron los promedios de:
- Tiempo de ejecución (segundos)
- Cantidad de nodos expandidos
- Longitud del camino encontrado
- Ranking combinados umando la posición en tiempo (T) y en nodos (N)

---

### Primer Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0005      | 509.2      | 211.0          | #1 (T:1, N:1) |
| UCS       | 0.0008      | 608.9      | 211.0          | #2 (T:2, N:3) |
| A*        | 0.0009      | 558.1      | 211.0          | #3 (T:3, N:2) |
| BFS       | 0.0014      | 609.6      | 211.0          | #4 (T:4, N:4) |

### Segundo Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0006      | 573.3      | 209.3          | #1 (T:1, N:2) |
| A*        | 0.0008      | 545.3      | 209.3          | #2 (T:2, N:1) |
| UCS       | 0.0008      | 602.2      | 209.3          | #3 (T:3, N:3) |
| BFS       | 0.0014      | 602.6      | 209.3          | #4 (T:4, N:4) |

### Tercer Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0006      | 591.5      | 243.4          | #1 (T:1, N:1) |
| A*        | 0.0010      | 596.8      | 243.4          | #2 (T:3, N:2) |
| UCS       | 0.0009      | 651.7      | 243.4          | #3 (T:2, N:4) |
| BFS       | 0.0015      | 651.5      | 243.4          | #4 (T:4, N:3) |

### Cuarto Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0007      | 621.8      | 277.1          | #1 (T:1, N:1) |
| A*        | 0.0010      | 631.8      | 277.1          | #2 (T:2, N:2) |
| UCS       | 0.0010      | 700.6      | 277.1          | #3 (T:3, N:3) |
| BFS       | 0.0016      | 701.1      | 277.1          | #4 (T:4, N:4) |

---

### Análisis General

Después de analizar los resultados de las 100 simulaciones por algoritmos, concluimos que: 

#### 1. Velocidad de Ejecución (Tiempo Promedio)
- **DFS** fue consistentemente el más rápido, con tiempos promedio entre 0.0005 y 0.0007 segundos.
- Le siguieron **UCS** y **A\***, con tiempos muy cercanos entre sí, ambos en torno a 0.0008 – 0.0010 segundos.
- **BFS** fue el más lento en todos los casos, alcanzando hasta 0.0016 segundos.

#### 2. Nodos Expandidos
- **DFS** también resultó ser el algoritmo que expandió menos nodos en la mayoría de las simulaciones.
- **A\*** se posicionó como el segundo más eficiente en expansión.
- **UCS** y **BFS** fueron los que más nodos expandieron, debido a que no utilizan información heurística y exploran en amplitud.

#### 3. Longitud de la Solución
- Cada laberinto en cada iteracion era igual para todos los algoritmos de búsqueda, y solo cambiaba cuando la iteración también lo hacía. Por ello la longitud fue la misma para todos.

#### 4. Ranking Compuesto (T+N)
- **DFS** fue el algoritmo más destacado, ubicándose en la primera posición en todos los conjuntos gracias a su bajo tiempo y eficiencia de expansión.
- **A\*** logró un excelente balance general, manteniéndose siempre en segundo lugar.
- **UCS** tuvo resultados aceptables, pero su falta de heurística lo hizo menos competitivo.
- **BFS** quedó consistentemente en último lugar, afectado por su costo computacional alto.

---

En este escenario específico de laberintos no ponderados y aleatorios, el algoritmos DFS demostró ser el más eficiente en tiempo y nodos, logrando además soluciones con valores cercanos a los algoritmos óptimos como UCS y A*. Aunque no garantiza caminos mínimos en todos los casos posibles, su rendimiento sobresaliente en esta situación lo hace muy competitivo.

**A\*** con heurística Manhattan mostró ser una alternativa sólida y balanceada, para escenarios donde se quiere una búsqueda informada y con buenas garantías.

**UCS** y **BFS**, aunque útiles conceptualmente, fueron menos eficientes tanto en tiempo como en nodos.

---

### Notas Técnicas

- Las simulaciones fueron realizadas en un entorno controlado, ejecutando 25 instancias por algoritmo en 4 conjuntos distintos (total 100 por algoritmo).
- El entorno de prueba utilizó laberintos generados aleatoriamente, no ponderados y sin ciclos negativos.
- La heurística Manhattan se aplicó únicamente en A\*, adaptada a las coordenadas del entorno del laberinto.

