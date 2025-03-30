# Desarrollo de Heurísticas para Algoritmos de Búsqueda: Análisis Matemático Detallado

## 1. Problema del TSP (Basado en Árbol de Expansión Mínima*

### Formulación Matemática Extendida

La heurística para el Problema TSP se define como:

$$h_{TSP}(n) = MST(C_R) + \min_{i \in C_V, j \in C_R} c(i,j) + \min_{k,l \in C_R, k \neq l} c(k,l)$$

donde:

- $C_V$ es el conjunto de ciudades visitadas
- $C_R$ es el conjunto de ciudades restantes por visitar
- $c(i,j)$ es el costo del arco entre las ciudades $i$ y $j$

### Demostración de Admisibilidad

- **Componente MST**:
    
    - Sea $H$ el tour óptimo restante. Si se elimina un arco de $H$, se obtiene un árbol de expansión.
    - Por definición de MST: $MST(C_R) \leq costo(H^* - \text{un arco})$
    - Por lo tanto: $$MST(C_R) \leq costo(H) - \min(\text{arcos de } H)$$

- **Componentes de conexión**:
    
    - Necesitamos al menos un arco para conectar el último nodo visitado ($i \in C_V$) a $C_R$
    - Necesitamos al menos un arco para regresar al inicio desde $C_R$
    - El mínimo global $\min_{k,l \in C_R} c(k,l)$ es un límite inferior para ambos

Matemáticamente, para cualquier tour completo $T$ que extienda el estado actual:

$$MST(C_R) + c_{min1} + c_{min2} \leq costo(T)$$

## 2. 8-Puzzle, (Basado en distancia Manhattan )


La heurística se define como:

$$h_{8P}(s) = \sum_{i=1}^8 d_M(i) + 2 \cdot LC(s)$$

donde $d_M(i) = |x_i - g_{ix}| + |y_i - g_{iy}|$ es la distancia Manhattan para la ficha $i$.

### Teorema de Conflictos Lineales

Un conflicto lineal ocurre cuando dos fichas $i$ y $j$ en la misma fila/columna satisfacen:

- Ambas están en su fila/columna objetivo
- $(x_i - g_{ix})(x_j - g_{jx}) < 0$ (sentidos opuestos)
- $|g_{ix} - g_{jx}| < |x_i - x_j|$ (se interponen)

Cada par de fichas en conflicto añade al menos 2 movimientos adicionales:

- Mover una ficha fuera de la fila/columna (+1)
- Moverla de regreso después (+1)

### Demostración de Consistencia

Para cualquier movimiento válido $a$ del estado $s$ a $s'$:

$$h(s) \leq c(s,a,s') + h(s')$$

Esto se cumple porque:

- La distancia Manhattan de una ficha cambia en $\pm 1$ por movimiento
- Los conflictos lineales solo pueden resolverse o reducirse con movimientos que compensen el cambio en $h$

## 3. Torres de Hanoi, (Basado en Análisis Recursivo)

### Formulación Recursiva

Para $n$ discos, se define la heurística como:

$$h_{TH}(s) = \sum_{i=1}^n 2^{i-1} \cdot \delta_i(s)$$

donde $$\delta_i(s) = \begin{cases} 0 & \text{si disco } i \text{ está en torre destino con discos menores encima} \ 1 & \text{en otro caso} \end{cases}$$

### Demostración por Inducción

**Caso base**: Para 1 disco, $h_{TH}(s) = 1$ si no está en destino (óptimo).

**Paso inductivo**: Asumimos válido para $k$ discos. Para $k+1$:

- Si disco $k+1$ no está en destino: necesita al menos $2^k$ movimientos (por hipótesis inductiva)
- Los $k$ discos menores deben moverse dos veces (antes y después de mover $k+1$)

La suma de pesos $2^{i-1}$ captura exactamente esta estructura recursiva.
