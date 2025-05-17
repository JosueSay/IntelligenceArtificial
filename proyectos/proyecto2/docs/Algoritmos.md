## Resolución de laberintos usando algoritmos de búsqueda

### Explicación de la implementación de los algoritmos generados: 


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
