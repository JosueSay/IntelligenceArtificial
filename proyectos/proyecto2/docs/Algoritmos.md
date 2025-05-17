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



### Resultados de Algoritmos de Búsqueda en Laberinto

## Tabla Comparativa

| Algoritmo | Tiempo (s) | Nodos explorados | Longitud camino | Posición |
|-----------|------------|------------------|-----------------|----------|
| BFS       | 0.0003     | 200              | 79              | 1        |
| UCS       | 0.0007     | 201              | 79              | 2        |
| A*        | 0.0009     | 107              | 79              | 3        |
| DFS       | 0.0022     | 816              | 79              | 4        |

## Conclusión

En esta simulación de laberinto, todos los algoritmos encontraron el mismo camino óptimo con una longitud de 79 pasos, pero con diferencias significativas en eficiencia. BFS mostró el mejor rendimiento en tiempo de ejecución (0.0003s), seguido muy de cerca por UCS y A*.

Lo más destacable es que A* exploró significativamente menos nodos (107) que los demás algoritmos, demostrando su eficiencia en la exploración del espacio de búsqueda gracias a su función heurística.

En contraste, DFS resultó ser el menos eficiente en este escenario, explorando 816 nodos (casi 8 veces más que A*) y tomando el mayor tiempo de ejecución.

Estos resultados confirman que la elección del algoritmo de búsqueda puede tener un impacto considerable en el rendimiento, incluso cuando todos encuentran la solución óptima.
