import numpy as np
import random
from TicTacToe import TicTacToe

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state              # Estado actual del juego
        self.parent = parent            # Nodo padre (None si es la raíz)
        self.children = []              # Hijos generados desde este nodo
        self.visits = 0                 # Cantidad de veces que se ha visitado este nodo
        self.wins = 0                   # Suma de resultados obtenidos desde este nodo

    # Expansión: genera todos los posibles hijos desde este nodo
    def expand(self):
        for move in self.state.availableMoves():
            nextState = self.state.clone()
            nextState.makeMove(move)
            self.children.append(MCTSNode(nextState, self))

    # Verifica si ya se generaron todos los hijos posibles
    def isFullyExpanded(self):
        return len(self.children) == len(self.state.availableMoves())

    # Selección: elige el mejor hijo usando la fórmula UCT
    """
    $$ u(i) = \frac{w_i}{s_i} + c \cdot \sqrt{\frac{\log(s_p)}{s_i}} $$

    Donde:

    - $w_i$: número de victorias desde el nodo $i$
    - $s_i$: número de simulaciones desde el nodo $i$
    - $s_p$: número de simulaciones desde el nodo padre de $i$
    - $c$: constante de exploración (por ejemplo, $\sqrt{2}$)

    Interpretación:

    - Primer término $\frac{w_i}{s_i}$: favorece nodos exitosos ya explorados (**explotación**).
    - Segundo término $c \cdot \sqrt{\frac{\log(s_p)}{s_i}}$: favorece nodos poco explorados (**exploración**).
    """
    def bestChild(self, cParam):
        choicesWeights = [
            (child.wins / (child.visits + 1e-5)) +
            cParam * np.sqrt(np.log(self.visits + 1) / (child.visits + 1e-5))
            for child in self.children
        ]
        return self.children[np.argmax(choicesWeights)]

    # Simulación (rollout): juega desde este estado hasta el final
    def rollout(self, rolloutPolicy=None, maxDepth=None):
        currentState = self.state.clone()
        depth = 0
        while not currentState.isTerminal():
            moves = currentState.availableMoves()
            # Política de simulación (aleatoria por defecto)
            move = rolloutPolicy(currentState, moves) if rolloutPolicy else random.choice(moves)
            currentState.makeMove(move)
            depth += 1
            # Si hay un límite de profundidad, detener
            if maxDepth is not None and depth >= maxDepth:
                break
        return currentState.score()
    
    # Backpropagation: propaga el resultado hacia la raíz
    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(-result)

def mcts(root, iterLimit=100, cParam=1.41, rolloutPolicy=None, maxDepth=None):
    for _ in range(iterLimit):
        node = root
        # 1. Selección: bajar hasta nodo hoja o no totalmente expandido
        while node.children and node.isFullyExpanded():
            node = node.bestChild(cParam)
        # 2. Expansión: generar hijos si no es terminal
        if not node.state.isTerminal():
            node.expand()
            if node.children:
                node = random.choice(node.children)
        # 3. Simulación (rollout)
        result = node.rollout(rolloutPolicy=rolloutPolicy, maxDepth=maxDepth)
        # 4. Backpropagation
        node.backpropagate(result)
    return root.bestChild(cParam=0) # Al final, devolver mejor jugada (sin exploración)

# Ejecuta múltiples partidas contra jugador aleatorio para medir rendimiento
def runExperiments(n=1000, iterPerMove=100, cParam=1.41, rolloutPolicy=None, maxDepth=None):
    wins = draws = losses = 0
    totalNodes = []

    for _ in range(n):
        game = TicTacToe()
        nodesExplored = 0
        while not game.isTerminal():
            if game.currentPlayer == 'X': # MCTS juega como 'X'
                root = MCTSNode(game.clone())
                best = mcts(root, iterLimit=iterPerMove, cParam=cParam,
                            rolloutPolicy=rolloutPolicy, maxDepth=maxDepth)
                game = best.state
                nodesExplored += iterPerMove
            else: # Jugador aleatorio como 'O'
                move = random.choice(game.availableMoves())
                game.makeMove(move)
        score = game.score()
        if score == 1:
            wins += 1
        elif score == 0:
            draws += 1
        else:
            losses += 1
        totalNodes.append(nodesExplored)

    print("Victorias:", wins)
    print("Empates:", draws)
    print("Derrotas:", losses)
    print("Nodos explorados promedio por partida:", sum(totalNodes) / n)

runExperiments(n=1000, iterPerMove=100, cParam=1.41, maxDepth=10)
