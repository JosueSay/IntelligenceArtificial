# Contexto

En este laboratorio vamos a resolver un juego adversario de Tic-Tac-Toe usando diferentes algoritmos de búsqueda.

Implementar una clase general llamada Tic-Tac-Toe que simule un juego de "totito" entre dos jugadores "X" y "O", mediante un árbol. Usted siempre es el jugador "X", y el adversario es el jugador "O". Las jugadas son siempre alternas (en ocasiones comenzará a jugar "X", y en otras comenzará el jugador "O").

Los nodos finales del árbol tienen valor $+1$, $0$ ó $-1$ según el juego acabe en victoria de "X", empate o victoria de "O", respectivamente. El valor del score siempre refleja la ganancia o pérdida para el jugador "X" (usted).

# Problema 1

Implementar una búsqueda minimax de $k$ niveles (a futuro) para obtener la mejor jugada en cada caso. Aquí, $k \geq 1$ se vuelve un parámetro que indica la profundidad máxima del sub-árbol a explorar. En este caso deberá construir una heurística que estime el valor de la utilidad para los nodos no finales.

Repetir $N$ experimentos, con $N = 1000$ para estimar el número esperado de victorias, empates y derrotas, así como el número promedio de nodos explorados en cada sub-árbol.

```python
Algoritmo: MINIMAX
Profundidad de búsqueda: 3
Total de juegos: 2000
Victorias: 1893 (94.65%)
Empates: 98 (4.90%)
Derrotas: 9 (0.45%)
Nodos explorados promedio por juego: 750.85
Tiempo total cuando el adversario empieza: 2.10 segundos
```

- [**Enlace a repositorio**](https://github.com/JosueSay/IntelligenceArtificial/blob/main/labs/lab6/MiniMax.py)

# Problema 2

Implementar una búsqueda minimax de $k$ niveles (a futuro), con un esquema de $\alpha - \beta$ pruning, para obtener la mejor jugada en cada caso. Aquí, $k \geq 1$ se vuelve un parámetro que indica la profundidad máxima del sub-árbol a explorar. Use la misma heurística del Ejercicio 1.

Repetir $N$ experimentos, con $N = 1000$ para estimar el número esperado de victorias, empates y derrotas, así como el número promedio de nodos explorados en cada sub-árbol.

```python
Algoritmo: ALPHA_BETA
Profundidad de búsqueda: 3
Total de juegos: 2000
Victorias: 1883 (94.15%)
Empates: 102 (5.10%)
Derrotas: 15 (0.75%)
Nodos explorados promedio por juego: 285.67
Tiempo total cuando el adversario empieza: 0.75 segundos
```

- [**Enlace a repositorio**](https://github.com/JosueSay/IntelligenceArtificial/blob/main/labs/lab6/MiniMax.py)

# Problema 3

Implementar una búsqueda Monte Carlo Tree Search (MCTS) para obtener la mejor jugada en cada caso. En este caso deberá implementar y decidir los parámetros necesarios para el MCTS.

Repetir $N$ experimentos, con $N = 1000$ para estimar el número esperado de victorias, empates y derrotas, así como el número promedio de nodos explorados en cada sub-árbol.

## Respuesta

Usando la función `UCF`:

$$ u(i) = \frac{w_i}{s_i} + c \cdot \sqrt{\frac{\log(s_p)}{s_i}} $$

Donde:

- $w_i$: número de victorias desde el nodo $i$
- $s_i$: número de simulaciones desde el nodo $i$
- $s_p$: número de simulaciones desde el nodo padre de $i$
- $c$: constante de exploración (por ejemplo, $\sqrt{2}$)

Interpretación:

- Primer término $\frac{w_i}{s_i}$: favorece nodos exitosos ya explorados (**explotación**).
- Segundo término $c \cdot \sqrt{\frac{\log(s_p)}{s_i}}$: favorece nodos poco explorados (**exploración**).

Implementación de estructura para el juego `TicTacToe.py` y la implementación del algoritmo Montecarlo en `MTC.py` con uno de sus resultados igual al siguiente:

```python
Victorias: 886
Empates: 0
Derrotas: 114
Nodos explorados promedio por partida: 331.6
```

- [**Enlace a repositorio**](https://github.com/JosueSay/IntelligenceArtificial/blob/main/labs/lab6/problema3.md)
- [**Enlace a video demostrativo**](https://youtu.be/RUQL_VmOTkA)

# Problema 4

Elabora una tabla comparativa de los tres experimentos anteriores, variando los valores de $k$, y variando los parámetros del MCTS, y compare los resultados del número de victorias, empates y pérdidas, y tiempo de ejecución promedio, para al menos 6 variantes de los algoritmos anteriores.

En esa tabla deberá comparar los dos casos siguientes:

- Cuando usted "X" es el jugador que comienza la partida.  
- Cuando el adversario "O" es el jugador que inicia la partida.


### Minimax con profundidad limitada

#### Cuando X (jugador) empieza

| Valor de $$k$$ | # De intentos | # De victorias | # De empates | # De derroras | Tiempo  |
| -------------- | ------------- | -------------- | ------------ | ------------- | ------- |
| 3              | 50            | 50             | 0            | 0             | 0.10 s  |
| 5              | 50            | 49             | 1            | 0             | 1.46 s  |
| 7              | 50            | 49             | 1            | 0             | 5.85 s  |
| 9              | 50            | 50             | 0            | 0             | 3.36 s  |
| 11             | 50            | 50             | 0            | 0             | 3.25 s  |
| 13             | 50            | 50             | 0            | 0             | 3.63 s  |

#### Cuando O (adversario/CPU) comienza

| Valor de $$k$$ | # De intentos | # De victorias | # De empates | # De derroras | Tiempo  |
| -------------- | ------------- | -------------- | ------------ | ------------- | ------- |
| 3              | 50            | 44             | 5            | 1             | 0.19 s  |
| 5              | 50            | 49             | 1            | 0             | 3.63 s  |
| 7              | 50            | 49             | 1            | 0             | 32.82 s |
| 9              | 50            | 43             | 7            | 0             | 30.63 s |
| 11             | 50            | 38             | 12           | 0             | 28.97 s |
| 13             | 50            | 35             | 15           | 0             | 36.98 s |


### Mini max con alpha-betta prunning

#### Cuando X (jugador) empieza

| Valor de $$k$$ | # De intentos | # De victorias | # De empates | # De derroras | Tiempo  |
| -------------- | ------------- | -------------- | ------------ | ------------- | ------- |
| 3              | 50            | 49             | 1            | 0             | 0.04 s  |
| 5              | 50            | 50             | 0            | 0             | 0.17 s  |
| 7              | 50            | 48             | 2            | 0             | 0.33 s  |
| 9              | 50            | 50             | 0            | 0             | 0.23 s  |
| 11             | 50            | 49             | 1            | 0             | 0.23 s  |
| 13             | 50            | 50             | 0            | 0             | 0.21 s  |

#### Cuando O (adversario/CPU) comienza

| Valor de $$k$$ | # De intentos | # De victorias | # De empates | # De derroras | Tiempo  |
| -------------- | ------------- | -------------- | ------------ | ------------- | ------- |
| 3              | 50            | 45             | 4            | 1             | 0.08 s  |
| 5              | 50            | 40             | 4            | 6             | 0.41 s  |
| 7              | 50            | 44             | 6            | 1             | 1.56 s  |
| 9              | 50            | 39             | 11           | 0             | 1.12 s  |
| 11             | 50            | 41             | 9            | 0             | 1.15 s  |
| 13             | 50            | 42             | 8            | 0             | 1.09 s  |


### Monte Carlo Tree Search

#### Cuando X (jugador) empieza

| Variante | Configuración | Victorias | Empates | Derrotas | Win Rate | Tiempo promedio (s) |
|----------|---------------|-----------|---------|----------|----------|---------------------|
| 1 | iterPerMove=50, cParam=1.41, maxDepth=None | 42 | 0 | 8 | 84% | 0.0044 |
| 2 | iterPerMove=200, cParam=1.41, maxDepth=None | 45 | 0 | 5 | 90% | 0.0190 |
| 3 | iterPerMove=100, cParam=0.7, maxDepth=None | 43 | 0 | 7 | 86% | 0.0081 |
| 4 | iterPerMove=100, cParam=2.0, maxDepth=None | 47 | 0 | 3 | 94% | 0.0080 |
| 5 | iterPerMove=100, cParam=1.41, maxDepth=5 | 46 | 0 | 4 | 92% | 0.0081 |
| 6 | iterPerMove=100, cParam=1.41, maxDepth=15 | 42 | 0 | 8 | 84% | 0.0083 |

#### Cuando O (adversario/CPU) comienza

| Variante | Configuración | Victorias | Empates | Derrotas | Win Rate | Tiempo promedio (s) |
|----------|---------------|-----------|---------|----------|----------|---------------------|
| 1 | iterPerMove=50, cParam=1.41, maxDepth=None | 14 | 24 | 12 | 28% | 0.0035 |
| 2 | iterPerMove=200, cParam=1.41, maxDepth=None | 11 | 31 | 8 | 22% | 0.0163 |
| 3 | iterPerMove=100, cParam=0.7, maxDepth=None | 24 | 23 | 3 | 48% | 0.0073 |
| 4 | iterPerMove=100, cParam=2.0, maxDepth=None | 21 | 21 | 8 | 42% | 0.0071 |
| 5 | iterPerMove=100, cParam=1.41, maxDepth=5 | 19 | 22 | 9 | 38% | 0.0075 |
| 6 | iterPerMove=100, cParam=1.41, maxDepth=15 | 16 | 29 | 5 | 32% | 0.0074 |


### Conclusiones

- Minimax con profundidad limitada es extremadamente efectivo en  el juego, pues logro casi 100% de victorias/empates cuando el jugador inicia, independientemente de la profundidad.
- Minimax con poda alfa-beta mantiene la misma efectividad que Minimax anterior pero con tiempos significativamente menores.
- MCTS muestra mayor variabilidad en su rendimiento, siendo generalmente menos efectivo que los enfoques basados en Minimax en este juego. 
- Todos los algoritmos son más efectivos cuando X (el jugador que usa el algoritmo) comienza la partida, lo que confirma la ventaja teórica del primer jugador en totito
- La diferencia es especialmente notable en MCTS, donde el win rate baja drásticamente cuando el jugador no comienza (de ~90% a ~30-40%)
- Minimax con profundidad limitada muestra crecimiento exponencial del tiempo con la profundidad, especialmente cuando el oponente comienza (llegando a 36.98s con k=13).
- Minimax con poda alfa-beta es dramáticamente más rápido (30-40 veces) para profundidades altas (1.09s vs 36.98s para k=13).
- MCTS es el más rápido de todos (milisegundos vs segundos), incluso con configuraciones complejas.





