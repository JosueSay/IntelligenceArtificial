# Árbol de Expansión Mínima (Kruskal)

Los algoritmos **greedy** como Kruskal tienen el propósito de construir un Árbol de Expansión Mínima (MST), especialmente aplicados a **grafos ponderados**.

## Inicio del Algoritmo de Kruskal (Aplicado al Laberinto)

El objetivo es conectar las casillas del laberinto minimizando el peso total de las aristas conectadas.  
Se seleccionan las conexiones de menor peso disponibles sin formar ciclos.

Un **ciclo**, en el contexto del laberinto, significa cerrar un camino que conecte de nuevo al mismo punto sin necesidad, lo que rompería la estructura de laberinto.

Cada arista se representa como un triplete $(u, v, w)$, donde:

- $u$ y $v$: Casillas conectadas.
- $w$: Peso de la conexión.

La búsqueda de soluciones explora subconjuntos de aristas que formen árboles, y la cantidad de posibles MST crece exponencialmente con el número de nodos.

### Procedimiento del Algoritmo Kruskal

1. Ordenar las aristas de forma ascendente según su peso.
2. Inicializar un conjunto disjunto (**Union-Find**) para detectar ciclos.
3. Recorrer las aristas en orden creciente:
   - Si la arista conecta dos componentes diferentes (**no forma ciclo**), se incluye en el MST.
   - Si forma un ciclo, se descarta.
4. Termina cuando se han incluido $|V| - 1$ aristas.

   Esto debido a que en un árbol con V vértices, exactamente V - 1 aristas son necesarias y suficientes para conectar todos los nodos sin formar ciclos. Agregar más aristas crearía ciclos; menos aristas dejaría el grafo desconectado.

### Formalización

Dado $E = \{e_1, e_2, ..., e_m\}$ ordenado tal que $w(e_1) \leq w(e_2) \leq \dots \leq w(e_m)$, se seleccionan las aristas $e_i$ que cumplan:

$$
\text{Si } e_i \text{ conecta componentes disjuntas } \Rightarrow \text{añadir a } T
$$

Se mantiene una estructura de conjuntos disjuntos $F$ tal que:

- $F.find(u) \neq F.find(v) \Rightarrow F.union(u, v)$
