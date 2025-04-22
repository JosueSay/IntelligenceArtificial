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

