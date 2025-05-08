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

| Valor de $$k$$ | # De intentos | # De victorias | # De empates | # De derroras | Tiempo  |
| -------------- | ------------- | -------------- | ------------ | ------------- | ------- |
| 3              | 50            | 45             | 4            | 1             | 0.08 s  |
| 5              | 50            | 40             | 4            | 6             | 0.41 s  |
| 7              | 50            | 44             | 6            | 1             | 1.56 s  |
| 9              | 50            | 39             | 11           | 0             | 1.12 s  |
| 11             | 50            | 41             | 9            | 0             | 1.15 s  |
| 13             | 50            | 42             | 8            | 0             | 1.09 s  |


### Conclusiones


