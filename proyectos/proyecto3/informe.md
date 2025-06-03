# Informe Técnico: IA para Jugar Othello con Heurística Mejorada y Poda Alfa-Beta

Este informe describe el diseño e implementación de un agente de inteligencia artificial para el juego Othello. El sistema utiliza un algoritmo de búsqueda adversaria con heurística enriquecida, poda alfa-beta, un libro de aperturas, control del tiempo y adaptación a las fases del juego. Se explica cada componente del código con su razonamiento, fundamentos teóricos y referencias.

## Pseudocódigo General del Agente

1. Si no hay movimientos válidos, retorna None.
2. Si está en apertura, intenta aplicar el libro.
3. Si hay ≤12 casillas vacías, realiza barrido completo.
4. Si no, decide la profundidad según el momento.
5. Usa minimax con poda alfa-beta.
6. Si todo falla, elige jugada aleatoria.

```bash
function ai_move(board, player):
    if no hay movimientos válidos:
        return None

    if en apertura y se reconoce el patrón:
        return jugada del libro

    if en medio juego:
        usar minimax con poda alfa-beta a profundidad media

    if en final:
        usar minimax con poda alfa-beta a profundidad mayor
        si ≤ 12 huecos, barrido completo

    if no hay jugada clara:
        elegir movimiento aleatorio

    return mejor movimiento encontrado
```

## Parámetros Generales

```python
TIME_LIMIT  = 3.0
MID_DEPTH   = 3
END_DEPTH   = 5
SWEEP_LIMIT = 12
```

### Razonamiento

Se ajusta el tiempo de cómputo y profundidad de análisis dependiendo del momento del juego. Esto permite un equilibrio entre rendimiento y precisión.

## Libro de Aperturas

```python
OPENING_BOOK = {
    ((2, 3), (2, 2)): (3, 2),
    ((2, 3), (3, 2)): (2, 4),
    ((2, 3), (2, 4)): (3, 2),
}
```

Estas jugadas representan respuestas óptimas ante ciertas configuraciones iniciales, según principios estratégicos del juego Othello.

Las coordenadas representan las primeras jugadas de un jugador luego de la posición estándar inicial. Las aperturas seleccionadas tienen como objetivo:

1. **Evitar entregar el control de las esquinas**: Las esquinas son las posiciones más valiosas del tablero porque no pueden ser capturadas una vez tomadas.
2. **Controlar el centro y preparar ataques diagonales**: Los movimientos (3,2) o (2,4) aseguran que el jugador mantenga acceso al centro sin exponerse a ataques tempranos.
3. **Evitar configuraciones de "X-square" tempranas**: Estas jugadas previenen que el oponente tenga oportunidades de capturar esquinas colocando fichas en X-squares (diagonal inmediata a una esquina), que son peligrosas si se toman demasiado pronto.

### ¿Qué significan estas jugadas?

* `((2, 3), (2, 2)) → (3, 2)`
  Esta secuencia forma un patrón de apertura diagonal paralela. Al jugar (3,2) se evita ceder la esquina inferior izquierda y se extiende el control hacia el centro sin comprometer la estabilidad de los bordes.

* `((2, 3), (3, 2)) → (2, 4)`
  Movimiento perpendicular que sigue controlando el centro, buscando expandirse lateralmente sin empujar al oponente hacia los bordes.

* `((2, 3), (2, 4)) → (3, 2)`
  Una versión desplazada del patrón anterior, mantiene el control diagonal y evita regalar posiciones externas vulnerables.

Estas jugadas fueron seleccionadas siguiendo los patrones estratégicos presentados en la **[Estrategia Reversista y Visualización de Aperturas](https://othellobrasil.weebly.com/uploads/7/6/8/2/76824037/lea_tosti_-_estrategia_reversista_y_visualizaci%C3%B3n_de_aperturas_de_reversi.pdf)**, donde se menciona la importancia de mantener un control en los primeros turnos y de no apresurarse a capturar esquinas ni bordes, que pueden volverse en contra si no están estabilizados correctamente.

## Heurística

```python
def heuristic(b, p):
    # Diferencia de fichas
    # Valoración de esquinas, X y C squares
    # Movilidad relativa
```

La función heurística permite evaluar estados del tablero cuando aún no se llega al final del juego. Esta evaluación es esencial cuando se aplica búsqueda con profundidad limitada, como ocurre en algoritmos como Minimax con poda alfa-beta.

Una heurística enriquecida mejora la calidad de las decisiones al incluir criterios más finos que el simple conteo de fichas. Considera factores posicionales que tienen un impacto estratégico importante, especialmente a mediano y largo plazo.

En Othello:

* **Esquinas** son posiciones valiosas: una vez capturadas no pueden revertirse y sirven como anclas defensivas.
* **X-squares** (diagonales adyacentes a esquinas) son peligrosas si se ocupan prematuramente, porque suelen permitir que el oponente tome la esquina.
* **C-squares** (adyacentes ortogonalmente a las esquinas) también tienden a favorecer al rival si no están bien soportadas.
* **Movilidad** es la cantidad de jugadas legales: tener más opciones significa controlar el ritmo del juego y limitar la capacidad de respuesta del adversario.

Esta heurística refleja principios estratégicos de Othello extraídos de:

* **[Construyendo una IA para Othello (Sam Harrison)](https://samharrison00.medium.com/building-an-ai-to-play-my-favourite-board-game-othello-57f5aab1d6cf)**: recomienda considerar movilidad y control de esquinas.
* **[Guía de Estrategia Othello](https://www.othello.nl/content/guides/comteguide/strategy.html)**: detalla la peligrosidad de X y C squares.
* **[Estrategia Reversista](https://othellobrasil.weebly.com/uploads/7/6/8/2/76824037/lea_tosti_-_estrategia_reversista_y_visualizaci%C3%B3n_de_aperturas_de_reversi.pdf)**: justifica tácticas posicionales como el control de bordes y esquinas.

### Explicación del Código

```python
CORNERS   = {(0, 0), (0, 7), (7, 0), (7, 7)}
X_SQUARES = {(1, 1), (1, 6), (6, 1), (6, 6)}
C_SQUARES = {(0, 1), (1, 0), (0, 6), (1, 7),
             (6, 0), (7, 1), (6, 7), (7, 6)}
```

Se definen tres conjuntos de coordenadas:

* `CORNERS`: las cuatro esquinas del tablero.
* `X_SQUARES`: casillas diagonales a las esquinas.
* `C_SQUARES`: casillas adyacentes lateralmente a las esquinas.

Estas zonas tienen un valor táctico distinto. El código asigna bonificaciones o penalizaciones según el control del jugador sobre estas casillas.

```python
def heuristic(b, p):
    my  = sum(r.count(p)   for r in b)
    opp = sum(r.count(-p)  for r in b)
    score = my - opp
```

#### Parámetros

* `b`: el tablero actual, una lista de listas de tamaño 8×8, donde cada celda contiene `0` (vacía), `1` (jugador 1) o `-1` (jugador 2).
* `p`: el jugador evaluado (`1` o `-1`).

Primero se calcula la diferencia simple de fichas entre el jugador `p` y su oponente `-p`. Esto da una primera noción de ventaja cuantitativa.

```python
for (x, y) in CORNERS:
    if   b[x][y] == p:   score += 25
    elif b[x][y] == -p:  score -= 25
```

Se bonifica o penaliza el puntaje según el control de las esquinas. Cada esquina controlada suma +25 puntos, mientras que una esquina controlada por el oponente resta -25.

```python
for (x, y) in X_SQUARES:
    if   b[x][y] == p:   score -= 12
    elif b[x][y] == -p:  score += 12
```

Se penaliza ocupar X-squares porque suelen ofrecer al rival la oportunidad de capturar una esquina. Por eso, tener una ficha en esa casilla resta -12. Por el contrario, si el oponente está allí, es una oportunidad y se suma +12.

```python
for (x, y) in C_SQUARES:
    if   b[x][y] == p:   score -= 8
    elif b[x][y] == -p:  score += 8
```

Las C-squares tienen un efecto similar pero ligeramente menos crítico. Se penaliza su ocupación con -8 y se recompensa si las ocupa el oponente con +8.

```python
score += 2 * (len(valid_movements(b, p)) -
              len(valid_movements(b, -p)))
```

Finalmente, se incorpora un factor de movilidad. Se calcula la diferencia entre la cantidad de jugadas válidas para el jugador `p` y su oponente. Se multiplica por 2 para ajustar su peso dentro de la puntuación total.

## Función de Transición de Estado

```python
def apply_move(b, move, p):
    # Simula la jugada y voltea fichas del oponente
```

La **función de transición de estados** se define formalmente como:

```math
f: S × A → S
```

Esto significa que, dado un **estado** `S` (el tablero actual) y una **acción** `A` (una jugada válida), se obtiene un **nuevo estado** `S'` (tablero actualizado tras aplicar la jugada).

### ¿Por qué se requiere generar un nuevo tablero?

Cuando se realiza una búsqueda adversaria (como Minimax o Alfa-Beta), es necesario evaluar múltiples futuros posibles. Para eso, se debe:

1. Simular cómo quedaría el tablero si se hace cierta jugada.
2. Evaluar ese nuevo estado sin alterar el estado actual (para poder seguir explorando otras ramas).

**Modificar directamente el tablero original sería un error**, ya que contaminaría las demás simulaciones. Por eso, se crea una copia antes de modificarlo.

### Explicación del Código

```python
def apply_move(b, move, p):
    nb = deepcopy(b)
```

* `b`: estado actual del tablero.
* `move`: tupla `(x, y)` indicando la jugada que se quiere hacer.
* `p`: el jugador que realiza la jugada (`1` o `-1`).
* `nb`: nuevo tablero generado como copia del original.

```python
    x, y = move
    nb[x][y] = p
```

Se coloca la ficha del jugador en la posición especificada.

```python
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        line = []
```

Se exploran las 8 direcciones posibles (norte, sur, este, oeste y diagonales) para buscar fichas del oponente que podrían ser capturadas.

```python
        while 0 <= nx < 8 and 0 <= ny < 8 and nb[nx][ny] == -p:
            line.append((nx, ny))
            nx += dx
            ny += dy
```

Se avanza en la dirección actual mientras se encuentren fichas del oponente (`-p`). Se guardan las coordenadas de esas fichas en una lista `line`.

```python
        if 0 <= nx < 8 and 0 <= ny < 8 and nb[nx][ny] == p:
            for fx, fy in line:
                nb[fx][fy] = p
```

Si al final de la línea se encuentra una ficha del jugador `p`, se confirma que las fichas intermedias están encerradas y por tanto deben voltearse. Todas esas coordenadas se actualizan en el tablero.

```python
    return nb
```

Finalmente, se retorna el nuevo tablero con todos los cambios aplicados.

## Ordenación de Jugadas

```python
def order_moves(moves):
    # Prioriza: esquinas > normales > X-squares
```

### ¿Por qué?

Las esquinas son estratégicamente valiosas, y priorizarlas mejora la poda alfa-beta. Así se evalúan primero las mejores jugadas, permitiendo cortar ramas más rápido.

## Minimax con Poda Alfa-Beta

```python
def alphabeta(b, p, depth, α, β, start):
    # Implementación clásica con poda y heurística
```

### ¿Por qué?

Permite tomar decisiones óptimas en juegos de suma cero, minimizando el número de nodos evaluados gracias a la poda. Se exploran primero las mejores jugadas para maximizar las podas.

## Extracción del Historial

```python
def extract_history(b):
    # Detecta los dos primeros movimientos para el libro de aperturas
```

## Características del algoritmo

| #  | Componente / técnica                                    | Para qué sirve                                                 | Dónde se ve en el código                |
| -- | ------------------------------------------------------- | -------------------------------------------------------------- | --------------------------------------- |
| 1  | **Libro de aperturas mínimo**                           | Jugadas sólidas al inicio, sin desperdiciar tiempo.            | `OPENING_BOOK` + consulta inicial       |
| 2  | **Heurística enriquecida**                              | Mejora la evaluación posicional.                               | función `heuristic`                     |
| 3  | **Generador de movimientos** y **aplicación de jugada** | Permite explorar posibles escenarios sin modificar el tablero. | `valid_movements`, `apply_move`         |
| 4  | **Ordenación de jugadas**                               | Optimiza el orden de exploración para poda.                    | `order_moves`                           |
| 5  | **Minimax con poda alfa-beta**                          | Mejora eficiencia sin perder calidad de decisión.              | `alphabeta`                             |
| 6  | **Gestión del “paso” forzado**                          | Regla del juego cuando no hay movimientos válidos.             | `alphabeta` cuando no hay movimientos   |
| 7  | **Control de tiempo global**                            | Previene exceder el límite de tiempo por jugada.               | Corte por `time.time()`                 |
| 8  | **Profundidad adaptativa**                              | Ajusta profundidad según número de jugadas.                    | flujo principal                         |
| 9  | **Barrido completo (perfect play)**                     | Evalúa todos los estados terminales si hay pocos huecos.       | `depth = empties`                       |
| 10 | **Último recurso aleatorio**                            | Siempre garantiza una jugada válida.                           | `if best is None: random.choice(moves)` |
| 11 | **Registro de tiempo de cómputo**                       | Métricas para evaluación del agente.                           | `print("[IA] Tiempo de cálculo: ...")`  |

## Fundamento Teórico de Clase

Los componentes del agente se basan en:

* **Búsqueda adversaria en juegos de suma cero**

  * El juego se representa como un árbol con estados y transiciones.
  * Cada jugador busca maximizar (MAX) o minimizar (MIN) la utilidad.
* **Algoritmo Minimax**

  * Se explora recursivamente hasta una profundidad.
  * Cada nodo alterna entre MAX y MIN.
* **Poda alfa-beta**

  * Reduce nodos innecesarios: corta ramas sin beneficio.
  * Mejora si se ordenan bien las jugadas (mejores primero).
* **Heurísticas en profundidad limitada**

  * Evalúan estados no terminales.
  * Combinan movilidad, posicionamiento y estabilidad.
* **Exploración completa en estados pequeños**

  * Cuando el espacio de búsqueda es pequeño (≤12 huecos), es posible jugar perfectamente (sin heurística).

## Referencias

1. **[Building an AI to Play Othello – Sam Harrison](https://samharrison00.medium.com/building-an-ai-to-play-my-favourite-board-game-othello-57f5aab1d6cf)**

   * Utilizada para justificar el uso de poda alfa-beta, ordenación de jugadas y heurísticas basadas en movilidad y esquinas.

2. **[Othello Strategy Guide – othello.nl](https://www.othello.nl/content/guides/comteguide/strategy.html)**

   * Fundamenta el valor de las esquinas, peligros de las X-squares y principios estratégicos para cada fase del juego.

3. **[Estrategia Reversista y Visualización de Aperturas – Lea Tosti (Othello Brasil)](https://othellobrasil.weebly.com/uploads/7/6/8/2/76824037/lea_tosti_-_estrategia_reversista_y_visualizaci%C3%B3n_de_aperturas_de_reversi.pdf)**

   * Aporta ejemplos y justificación táctica sobre secuencias de apertura efectivas y su impacto en el desarrollo del medio juego.
