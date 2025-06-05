<!-- ---
header-includes:
  - \usepackage{amsmath}
  - \usepackage{amssymb}
  - \usepackage{fontspec}
  - \setmainfont{FiraCode Nerd Font}
  - \usepackage{setspace}
  - \setstretch{1.5}
  - \usepackage{fvextra}
  - \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}
  - \hypersetup{colorlinks=true, linkcolor=black, urlcolor=blue}
geometry: top=0.67in, bottom=0.67in, left=0.85in, right=0.85in
--- -->

# Informe Técnico: IA para Jugar Othello con Heurística, Poda Alfa-Beta y Gestión Adaptativa

El sistema utiliza un algoritmo de búsqueda adversaria con múltiples técnica:

* **Heurística**: evalúa esquinas, movilidad, X-squares y C-squares.
* **Poda alfa-beta con ordenación de jugadas**: mejora la eficiencia de la búsqueda adversaria.
* **Profundidad de búsqueda adaptativa**: se ajusta según el número de huecos y fase del juego.
* **Barrido completo** (exhaustivo) cuando hay menos o igual a 12 casillas vacías.
* **Libros de apertura diferenciados por color**: permite jugadas sólidas al inicio según el jugador.
* **Control de tiempo (time-out)**: asegura respuesta dentro del límite asignado; aplica jugada aleatoria como respaldo.

## Pseudocódigo General del Agente

1. Si no hay movimientos válidos, retorna `None`.
2. Si está en apertura y hay coincidencia en el libro correspondiente, aplica la jugada sugerida.
3. Si hay (<=12) casillas vacías, se realiza un barrido exacto con profundidad igual al número de huecos.
4. En otro caso, la profundidad se adapta según el número de jugadas válidas (más profundidad si hay pocas jugadas).
5. Se ejecuta Minimax con poda alfa-beta y ordenación de jugadas.
6. Si ocurre un *timeout* o error, se elige una jugada aleatoria válida como respaldo.

```python
function ai_move(board, player):
    if no hay jugadas válidas:
        return None

    if es apertura y hay coincidencia en libro:
        return jugada del libro

    if huecos <= SWEEP_LIMIT:
        depth = huecos  # barrido completo
    else:
        depth = MID_DEPTH si muchas jugadas, END_DEPTH si pocas

    ejecutar minimax con poda alfa-beta

    si no se encuentra jugada (por timeout):
        elegir jugada aleatoria

    return mejor jugada encontrada
```

## Parámetros Generales

```python
TIME_LIMIT  = 3.0           # segundos máximos de cómputo por jugada
MID_DEPTH   = 3             # profundidad típica en apertura y medio juego
END_DEPTH   = 5             # profundidad más alta en fases de cierre
SWEEP_LIMIT = 12            # umbral para realizar barrido exacto
INF         = float("inf")  # valor infinito simbólico
```

### Justificación

* **`TIME_LIMIT`**: garantiza que la IA responda siempre dentro del tiempo permitido.
* **`SWEEP_LIMIT`**: al llegar al 12 huecos (o menos), se permite jugar sin usar heurística.
* **Profundidad adaptativa**: más jugadas válidas implican menos profundidad (mayor ramificación); menos jugadas válidas permite mayor profundidad.

## Libro de Aperturas Diferenciado por Color

```python
OPENING_BOOK_WHITE = {
    ((2, 3), (2, 2)): (3, 2),
    ((2, 3), (3, 2)): (2, 4),
    ((2, 3), (2, 4)): (3, 2),
}

OPENING_BOOK_BLACK = {
    ((5, 4), (5, 5)): (4, 5),
    ((5, 4), (4, 5)): (5, 3),
    ((5, 4), (5, 3)): (4, 5),
}
```

El agente IA implementa un **libro de aperturas específico para cada color**. Esto permite un mejor inicio y estratégicamente diferenciado para blancas y negras, respetando las mejores prácticas de apertura en Othello.

Los libros de apertura están diseñados para actuar si el agente detecta que se encuentra en uno de los primeros turnos y las dos primeras jugadas coinciden con una de las secuencias predefinidas. Si eso ocurre, se responde con una jugada óptima sin necesidad de buscar.

1. **Evitar regalar esquinas en turnos tempranos**
   Las esquinas son posiciones definitivas: una vez tomadas, no pueden perderse. Es vital no permitir que el rival acceda a ellas mediante jugadas precipitadas.

2. **Controlar el centro y mantener flexibilidad**
   Las aperturas propuestas dan al jugador influencia en el tablero sin crear puntos débiles inmediatos.

3. **Prevenir ocupación prematura de X-squares o C-squares**
   Estas casillas son peligrosas si no están respaldadas, ya que facilitan que el oponente tome esquinas más adelante.

### ¿Qué significan estas jugadas?

#### Blancas (`OPENING_BOOK_WHITE`)

* `((2, 3), (2, 2)) → (3, 2)`

  * Apertura de tipo **diagonal paralela**.
  * Prioriza el control interior evitando vulnerabilidad en la esquina superior izquierda.

* `((2, 3), (3, 2)) → (2, 4)`

  * Jugada **perpendicular**, busca expansión lateral con buena defensa del borde.

* `((2, 3), (2, 4)) → (3, 2)`

  * Variante desplazada que equilibra control central y defensa de flancos.

#### Negras (`OPENING_BOOK_BLACK`)

* `((5, 4), (5, 5)) → (4, 5)`

  * Jugada simétrica respecto a las blancas; se replica el patrón de control seguro.

* `((5, 4), (4, 5)) → (5, 3)`

  * Variante que prioriza lateralidad sin arriesgar esquinas.

* `((5, 4), (5, 3)) → (4, 5)`

  * Opción que mantiene la diagonal interna fuerte sin comprometer casillas peligrosas.

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

$$f: S \times A \rightarrow S$$

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

Esta función organiza las jugadas válidas según su valor estratégico antes de ser evaluadas por el algoritmo de búsqueda. La ordenación permite que el algoritmo explore primero las mejores jugadas, lo que incrementa la eficiencia de la poda y mejora la calidad de las decisiones en menos tiempo con el fin de reducir el espacio de búsqueda efectivo, priorizar posiciones más valiosas y evitar errores de elección de jugadas del tablero usando la siguiente lógica:

1. **Esquinas (`CORNERS`) → prioridad máxima (clave 0)**
   Son las posiciones más estables del tablero: una vez ocupadas no pueden ser revertidas. Además, otorgan control duradero y seguridad posicional.
   → Se procesan **primero** para permitir más poda.

2. **Jugadas normales → prioridad media (clave 1)**
   No están en esquinas ni en X-squares. Son generalmente seguras o neutras según el contexto.

3. **X-squares (`X_SQUARES`) → prioridad baja (clave 2)**
   Son peligrosas si se ocupan sin respaldo, ya que suelen permitir al oponente capturar una esquina inmediatamente después.
   → Se evalúan **al final** para evitar jugadas que debiliten la posición.

## Minimax con Poda Alfa-Beta

```python
def alphabeta(b, p, depth, alpha, beta, start):
    # Implementación clásica con poda y heurística
```

Esta función implementa el algoritmo **Minimax con poda alfa-beta** con las siguientes características:

* Control de tiempo (*timeout*)
* Ordenación de jugadas
* Detección de turnos sin jugadas válidas
* Evaluación exacta al final del juego
* Uso de heurística

### Explicación del Código

1. **Corte por tiempo límite**
   Si el tiempo restante es muy bajo (`< 0.05s`), se abandona la búsqueda y se retorna el valor heurístico del estado actual para evitar penalizaciones por demora:

   ```python
   if time.time() - start > TIME_LIMIT - 0.05:
       return heuristic(b, player), None
   ```

2. **Chequeo de jugadas válidas**
   Si el jugador actual no tiene movimientos posibles:

   * Si el oponente tampoco tiene, se evalúa el tablero exactamente (conteo de fichas).
   * Si el oponente sí tiene, se pasa el turno recursivamente.

   ```python
   if not moves:
       ...
   ```

3. **Condición de profundidad**
   Si la profundidad se agotó, se evalúa con la heurística:

   ```python
   if depth == 0:
       return heuristic(b, player), None
   ```

4. **Exploración recursiva (Minimax)**

   * Si el jugador es el agente (`player`): se comporta como **MAX**, buscando el mayor valor.
   * Si el jugador es el oponente: actúa como **MIN**, buscando el menor valor.

   En ambos casos:

   * Se ordenan las jugadas con `order_moves()` (esquinas primero).
   * Se aplican movimientos sobre una copia del tablero (`apply_move`).
   * Se actualizan los valores de `alpha` y `beta`.
   * Se realizan cortes si `alpha >= beta` (poda).

   ```python
   for m in order_moves(moves):
       score, _ = alphabeta(...)
       ...
       if alpha >= beta:
           break
   ```

#### Parámetros

| Parámetro | Descripción                                                         |
| --------- | ------------------------------------------------------------------- |
| `b`       | Estado actual del tablero (matriz 8×8).                             |
| `p`       | Jugador actual (`1` o `-1`).                                        |
| `depth`   | Profundidad restante de búsqueda.                                   |
| `alpha`   | Mejor valor que MAX puede garantizar hasta ahora.                   |
| `beta`    | Mejor valor que MIN puede garantizar hasta ahora.                   |
| `start`   | Marca de tiempo al inicio de la búsqueda (para control de timeout). |

## Extracción del Historial

```python
def extract_history(b):
    # Detecta los dos primeros movimientos para el libro de aperturas
```

Esta función detecta las primeras dos jugadas realizadas en la partida a partir del estado actual del tablero. Su propósito es permitir al agente IA consultar el libro de aperturas, que depende de reconocer patrones en las primeras jugadas.

1. Se construye un tablero base `initial` con la posición estándar inicial de Othello:

   * Fichas blancas en (3,3) y (4,4)
   * Fichas negras en (3,4) y (4,3)

2. Se recorre el tablero actual y se identifican las casillas que **difieren** de ese estado inicial:

   ```python
   moves = [(i, j) for i in range(8) for j in range(8) if b[i][j] != initial[i][j]]
   ```

3. Se devuelven las **primeras dos jugadas** encontradas, como una tupla `(move1, move2)`, o `None` si aún no hay suficientes movimientos para determinar una apertura válida:

   ```python
   return tuple(moves[:2]) if len(moves) >= 2 else None
   ```

Esto se hace con el fin de conocer la secuencia de jugadas al inicio del juego extrayendo la secuencia de jugadas sin necesidad de guardar un historial explícito de las mismas.

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

  * Cuando el espacio de búsqueda es pequeño (<=12 huecos), es posible jugar perfectamente (sin heurística).

## Referencias

1. **[Building an AI to Play Othello – Sam Harrison](https://samharrison00.medium.com/building-an-ai-to-play-my-favourite-board-game-othello-57f5aab1d6cf)**

   * Utilizada para justificar el uso de poda alfa-beta, ordenación de jugadas y heurísticas basadas en movilidad y esquinas.

2. **[Othello Strategy Guide – othello.nl](https://www.othello.nl/content/guides/comteguide/strategy.html)**

   * Fundamenta el valor de las esquinas, peligros de las X-squares y principios estratégicos para cada fase del juego.

3. **[Estrategia Reversista y Visualización de Aperturas – Lea Tosti (Othello Brasil)](https://othellobrasil.weebly.com/uploads/7/6/8/2/76824037/lea_tosti_-_estrategia_reversista_y_visualizaci%C3%B3n_de_aperturas_de_reversi.pdf)**

   * Aporta ejemplos y justificación táctica sobre secuencias de apertura efectivas y su impacto en el desarrollo del medio juego.
