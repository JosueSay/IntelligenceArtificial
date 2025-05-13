# Algoritmo de Kruskal

El algoritmo de Kruskal es un método **greedy** utilizado para encontrar el Árbol de Expansión Mínima (MST) en un grafo. Este algoritmo ordena el peso de las aristas y conectandolos siempre y cuando sean disjuntos.

## Conceptos

* **Union-Find (Disjoint Set):** Estructura utilizada para detectar ciclos de forma eficiente durante la construcción del MST. Permite saber rápidamente si dos casillas ya están conectadas indirectamente.
* **Ponderado en el Laberinto:**
  En el contexto de la generación del laberinto, que sea **ponderado** significa que a cada conexión posible entre casillas (arista) se le asigna un **peso o costo** aleatorio. Este peso influye directamente en el orden en que se conectan las casillas.

  * Las conexiones con menor peso son preferidas, formando caminos "más baratos" en la estructura final del laberinto.
  * Esto afecta la forma y complejidad del laberinto, priorizando ciertas rutas sobre otras.
  * Si el laberinto es **no ponderado**, todas las aristas tienen el mismo peso, por lo que no hay preferencia en las conexiones, y el resultado es un laberinto más equilibrado y simétrico.

## Implementación en la Generación de Laberintos

1. **Representación del Grafo:**

   * Cada casilla es un nodo.
   * Las conexiones horizontales y verticales entre casillas son las aristas.
   * Si se trabaja con un laberinto ponderado, se asigna un peso aleatorio a cada arista. Si no, todos los pesos son iguales.

2. **Preparación de las Aristas:**

   * Se generan todas las aristas posibles entre casillas adyacentes.
   * En el caso ponderado, se asigna un peso aleatorio a cada arista utilizando una semilla para garantizar reproducibilidad.
   * Las aristas se ordenan por peso. En el caso no ponderado, se barajan aleatoriamente para aleatorizar la generación del laberinto.

3. **Construcción del Laberinto:**

   * Se recorre la lista de aristas ordenadas.
   * Se utiliza la estructura Union-Find para verificar si la inclusión de una arista formaría un ciclo. Si no forma ciclo, se incluye en el laberinto.
   * Este proceso se repite hasta incluir $|V| - 1$ aristas, donde $|V|$ es el número de casillas del laberinto.

4. **Finalización:**

   * Al finalizar, el laberinto está completamente conectado y no posee ciclos, lo que garantiza la unicidad de los caminos entre casillas.

## Formalización Matemática

Dado un conjunto de aristas $E = {e_1, e_2, ..., e_m}$ ordenado de forma no decreciente según su peso $w$, se construye el MST iterando sobre las aristas y aplicando la siguiente regla:

$$
\text{Si } e_i \text{ conecta componentes disjuntas} \Rightarrow \text{añadir } e_i \text{ al MST}
$$

Se utiliza una estructura de conjuntos disjuntos \$F\$ de forma que:

* Si $F.\text{find}(u) \neq F.\text{find}(v)$, se realiza la unión de los conjuntos:

$$
F.\text{union}(u, v)
$$

Este proceso se repite hasta que el MST contiene exactamente $|V| - 1$ aristas.
