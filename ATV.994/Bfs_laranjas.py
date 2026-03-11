"""
LeetCode 994 — Rotting Oranges

Problema:
Dada uma matriz onde:
0 = célula vazia
1 = laranja fresca
2 = laranja podre

A cada minuto, qualquer laranja fresca adjacente (cima, baixo, esquerda, direita)
a uma laranja podre se torna podre.

Objetivo:
Retornar o número mínimo de minutos necessários para que todas as laranjas
se tornem podres.

Se existir alguma laranja que nunca poderá apodrecer, retornar -1.

Estratégia:
Utilizar BFS (Breadth First Search) com múltiplas fontes.
Todas as laranjas podres iniciais começam a infectar simultaneamente.

Complexidade:
Tempo: O(m × n)
Espaço: O(m × n)
"""

from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rows = len(grid)
        cols = len(grid[0])

        queue = deque()
        fresh_oranges = 0

        # Percorre a matriz para encontrar as laranjas podres e quas são frescas
        for r in range(rows):
            for c in range(cols):

                if grid[r][c] == 2:
                    queue.append((r, c))

                elif grid[r][c] == 1:
                    fresh_oranges += 1

        minutes = 0

        # Direções possíveis (cima, baixo, direita, esquerda)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # BFS
        while queue and fresh_oranges > 0:

            # Processa um nível do BFS - 1 min
            for _ in range(len(queue)):

                r, c = queue.popleft()

                for dr, dc in directions:

                    nr = r + dr
                    nc = c + dc

                    # Verifica limites da matriz
                    if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                        continue

                    # Infecta laranja fresca
                    if grid[nr][nc] != 1:
                        continue

                    # Laranja fica podre
                    grid[nr][nc] = 2
                    fresh_oranges -= 1

                    # Nova laranja podre entra na fila
                    queue.append((nr, nc))

            minutes += 1

        return minutes if fresh_oranges == 0 else -1



# Execução od code


if __name__ == "__main__":

    grid = [
        [1, 1, 1],
        [1, 2, 0],
        [0, 1, 1]
    ]

    solver = Solution()

    result = solver.oranges_rotting(grid)

    print("Passos necessários:", result)

