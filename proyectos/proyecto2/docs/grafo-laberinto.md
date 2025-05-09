# Equivalencia Grafo-Laberinto

- Un grafo se define como $G = (V, E)$, donde:
  - $V$: Conjunto de vértices (**posiciones o casillas** en el laberinto).
  - $E$: Conjunto de aristas (**conexiones entre casillas adyacentes**: arriba, abajo, izquierda, derecha).

- Las **aristas conectadas** forman los **caminos transitables del laberinto**.
- Las **aristas no conectadas** representan las **paredes** del laberinto.

## Grid y Ponderación

- En el **grid** del laberinto:
  - Un **1** indica una **pared** (celda no transitable).
  - Un **0** indica un **camino** (celda transitable).

- Si el laberinto es **ponderado**:
  - Existe una segunda estructura de pesos (`weights`), donde **solo las celdas de camino (grid = 0)** tienen valores de peso **mayores a 0**.
  - Estos valores representan el **costo de transitar** por la celda.
  - Los muros no tienen peso (su valor en `weights` será 0 o no estará definido).

- Si el laberinto es **no ponderado**:
  - Todas las celdas de camino se asumen con un peso uniforme de **1**.

### Resumen de Estados

| Grid (Estructura) | Weights (Si ponderado) | Estado        |
|-------------------|------------------------|----------------|
| 1                 | N/A                    | Muro (Pared)   |
| 0                 | > 0                    | Camino ponderado (peso > 0) |
| 0                 | N/A                    | Camino no ponderado (peso = 1) |
