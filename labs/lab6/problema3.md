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
