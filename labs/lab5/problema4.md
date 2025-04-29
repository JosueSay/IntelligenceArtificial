## Problema 4

### Algoritmo Minimax

Primero calculo los valores de los nodos del nivel inferior

- Primer nodo: min(-2, 4) = -2
- Segundo nodo: min(6, -8) = -8
- Tercer nodo: min(-3, -1) = -3
- Cuarto nodo: min(7, -5) = -5
- Quinto nodo: min(2, -4) = -4
- Sexto nodo: min(-6, 8) = -6
- Séptimo nodo: min(3, 1) = 1
- Octavo nodo: min(-7, 5) = -7

Nivel 3

- Primer nodo: max(-2, -8) = -2
- Segundo nodo: max(-3, -5) = -3
- Tercer nodo: max(-4, -6) = -4
- Cuarto nodo: max(1, -7) = 1

Nivel 2

- Primer nodo: min(-2, -3) = -3
- Segundo nodo: min(-4, 1) = -4

Nivel 1

- Raíz: max(-3, -4) = -3

**Respuesta**: Aplicando el algoritmo minimax, y con base a los calculos, la mejor acción para el jugador máximo en la raíz es elegir la rama izquierda que conduce a un valor minimax de -3.

### Algoritmo Minimax con Poda Alfa-Beta

Empezando en la raíz (max), con $\alpha = -\infty, \beta = \infty$:

1. En la rama izquierda con $\alpha = -\infty, \beta = \infty$:
   - El primer hijo, con $\alpha = -\infty, \beta = \infty$:
     - Primer nodo min: devuelve -2
     - Ahora $\alpha = -2$
     - Segundo nodo min: devuelve -8
     - Valor de este nodo max = -2
   - Este nodo min actualiza $\beta = -2$

   - Luego segundo hijo con $\alpha = -\infty, \beta = -2$:
     - Primer nodo min: valor = -3
     - El valor ahora es $\alpha = -3$
     - Como $\alpha = -3 \geq \beta = -2$, se poda el resto de este subárbol
     - Valor de este nodo max = -3
   - Este nodo min actualiza $\beta = -3$
   - Valor de este nodo min = -3

2. La raíz actualiza $\alpha = -3$

3. Visitando rama derecha con $\alpha = -3, \beta = \infty$:
   - Visitando primer hijo con $\alpha = -\infty, \beta = \infty$:
     - Exploramos nodos hoja y obtenemos valor = -4
   - Este nodo min actualiza $\beta = -4$

   - Visitando segundo hijo con $\alpha = -\infty, \beta = -4$:
     - Primer nodo min: valor = 1
     - Actualizamos $\alpha = 1$
     - Como $\alpha = 1 > \beta = -4$, también se poda el resto del subárbol actual
     - Valor de este nodo max = 1
   - Este nodo min actualiza $\beta = -4$
   - Valor de este nodo min = -4

4. La raíz actualiza $\alpha = \max(-3, -4) = -3$

**Respuesta**: Con la poda alfa-beta, la mejor acción para el jugador máximo en la raíz sigue siendo elegir la rama izquierda, con un valor minimax de -3.
