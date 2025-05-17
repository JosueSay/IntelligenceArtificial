# Comparativa de Algoritmos de Búsqueda en Laberintos Aleatorios No Ponderados

Este experimento evalúa el rendimiento de cuatro algoritmos clásicos de búsqueda al resolver **laberintos no ponderados** generados **aleatoriamente**. Cada algoritmo fue ejecutado en **25 laberintos distintos por conjunto**, para un total de **100 simulaciones por algoritmo**.

Para la parte 3 del proyecto, se busca comparar cuatro algoritmos de búsqueda al resolver laberintos. En nuestra simulación hicimos uso de laberintos generados aleatoriamente cada una de las ejecuciones, cambiando el punto de inicio y el punto final tomando en cuenta una distancia mínima de 10 unidades manhattan entre sí. Cada algoritmo se ejecuto en 25 laberintos aleatorios y los resultados promedios fueron guardados en tablas de estadística. 

Para la clasificación de que algoritmo fue mejor tomamos en cuenta el tiempo que tardó en resolver el laberinto, y la cantidad de nodos que creó para hacerlo. 

Los algoritmos evaluados fueron:

- DFS (Depth-First Search)
- BFS (Breadth-First Search)
- UCS/Dijkstra (Uniform Cost Search)
- A* con heurística de distancia Manhattan

Para cada conjunto de simulaciones se tomaron los promedios de:
- Tiempo de ejecución (segundos)
- Cantidad de nodos expandidos
- Longitud del camino encontrado
- Ranking combinados umando la posición en tiempo (T) y en nodos (N)

---

## Primer Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0005      | 509.2      | 211.0          | #1 (T:1, N:1) |
| UCS       | 0.0008      | 608.9      | 211.0          | #2 (T:2, N:3) |
| A*        | 0.0009      | 558.1      | 211.0          | #3 (T:3, N:2) |
| BFS       | 0.0014      | 609.6      | 211.0          | #4 (T:4, N:4) |

## Segundo Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0006      | 573.3      | 209.3          | #1 (T:1, N:2) |
| A*        | 0.0008      | 545.3      | 209.3          | #2 (T:2, N:1) |
| UCS       | 0.0008      | 602.2      | 209.3          | #3 (T:3, N:3) |
| BFS       | 0.0014      | 602.6      | 209.3          | #4 (T:4, N:4) |

## Tercer Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0006      | 591.5      | 243.4          | #1 (T:1, N:1) |
| A*        | 0.0010      | 596.8      | 243.4          | #2 (T:3, N:2) |
| UCS       | 0.0009      | 651.7      | 243.4          | #3 (T:2, N:4) |
| BFS       | 0.0015      | 651.5      | 243.4          | #4 (T:4, N:3) |

## Cuarto Conjunto de Simulaciones (25 ejecuciones)

| Algoritmo | Tiempo Prom | Nodos Prom | Longitud Prom | Ranking (T+N) |
|-----------|-------------|------------|----------------|---------------|
| DFS       | 0.0007      | 621.8      | 277.1          | #1 (T:1, N:1) |
| A*        | 0.0010      | 631.8      | 277.1          | #2 (T:2, N:2) |
| UCS       | 0.0010      | 700.6      | 277.1          | #3 (T:3, N:3) |
| BFS       | 0.0016      | 701.1      | 277.1          | #4 (T:4, N:4) |

---

## Análisis General

Después de analizar los resultados de las 100 simulaciones por algoritmos, concluimos que: 

### 1. Velocidad de Ejecución (Tiempo Promedio)
- **DFS** fue consistentemente el más rápido, con tiempos promedio entre 0.0005 y 0.0007 segundos.
- Le siguieron **UCS** y **A\***, con tiempos muy cercanos entre sí, ambos en torno a 0.0008 – 0.0010 segundos.
- **BFS** fue el más lento en todos los casos, alcanzando hasta 0.0016 segundos.

### 2. Nodos Expandidos
- **DFS** también resultó ser el algoritmo que expandió menos nodos en la mayoría de las simulaciones.
- **A\*** se posicionó como el segundo más eficiente en expansión.
- **UCS** y **BFS** fueron los que más nodos expandieron, debido a que no utilizan información heurística y exploran en amplitud.

### 3. Longitud de la Solución
- Cada laberinto en cada iteracion era igual para todos los algoritmos de búsqueda, y solo cambiaba cuando la iteración también lo hacía. Por ello la longitud fue la misma para todos.

### 4. Ranking Compuesto (T+N)
- **DFS** fue el algoritmo más destacado, ubicándose en la primera posición en todos los conjuntos gracias a su bajo tiempo y eficiencia de expansión.
- **A\*** logró un excelente balance general, manteniéndose siempre en segundo lugar.
- **UCS** tuvo resultados aceptables, pero su falta de heurística lo hizo menos competitivo.
- **BFS** quedó consistentemente en último lugar, afectado por su costo computacional alto.

---

En este escenario específico de laberintos no ponderados y aleatorios, el algoritmos DFS demostró ser el más eficiente en tiempo y nodos, logrando además soluciones con valores cercanos a los algoritmos óptimos como UCS y A*. Aunque no garantiza caminos mínimos en todos los casos posibles, su rendimiento sobresaliente en esta situación lo hace muy competitivo.

**A\*** con heurística Manhattan mostró ser una alternativa sólida y balanceada, para escenarios donde se quiere una búsqueda informada y con buenas garantías.

**UCS** y **BFS**, aunque útiles conceptualmente, fueron menos eficientes tanto en tiempo como en nodos.

---

## Notas Técnicas

- Las simulaciones fueron realizadas en un entorno controlado, ejecutando 25 instancias por algoritmo en 4 conjuntos distintos (total 100 por algoritmo).
- El entorno de prueba utilizó laberintos generados aleatoriamente, no ponderados y sin ciclos negativos.
- La heurística Manhattan se aplicó únicamente en A\*, adaptada a las coordenadas del entorno del laberinto.

