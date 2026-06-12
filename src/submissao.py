"""
UVA 10092 - The Problem with the Problem Setter
Arquivo UNIFICADO para submissão no UVA Online Judge.

Este arquivo contém todo o código em um único lugar, pronto para
ser submetido diretamente na plataforma. É a versão agrupada dos
módulos edmonds_karp.py, rede_fluxo.py e main.py.

Modelagem da rede de fluxo:
  - Vértice 0: source (origem)
  - Vértices 1..nk: categorias
  - Vértices nk+1..nk+np: problemas
  - Vértice nk+np+1: sink (sorvedouro)

  Arestas:
    source -> categoria_i  com capacidade = demanda[i]
    categoria_i -> problema_j  com capacidade 1  (se problema j pertence à categoria i)
    problema_j -> sink  com capacidade 1  (cada problema pode ser usado no máximo 1 vez)

  Algoritmo: Edmonds-Karp (BFS) — complexidade O(V · E²)
"""

import sys
from collections import deque

input = sys.stdin.readline


# ============================================================
# MÓDULO 1: Edmonds-Karp (Algoritmo de Fluxo Máximo)
# ============================================================

class EdmondsKarp:
    """Implementação do algoritmo Edmonds-Karp para fluxo máximo.

    Usa BFS para encontrar caminhos aumentantes no grafo residual,
    garantindo complexidade O(V * E^2).
    """

    def __init__(self, n):
        """Inicializa a rede com n vértices."""
        self.n = n
        # Lista de adjacência: cada entrada é [destino, capacidade, indice_da_aresta_reversa]
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        """Adiciona aresta u → v com capacidade cap e aresta reversa v → u com capacidade 0."""
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def bfs(self, s, t, parent):
        """BFS no grafo residual para encontrar caminho aumentante s → t."""
        visited = [False] * self.n
        visited[s] = True
        queue = deque([s])

        while queue:
            u = queue.popleft()
            for i, (v, cap, _) in enumerate(self.graph[u]):
                if not visited[v] and cap > 0:
                    visited[v] = True
                    parent[v] = (u, i)
                    if v == t:
                        return True
                    queue.append(v)
        return False

    def max_flow(self, s, t):
        """Calcula o fluxo máximo de s a t usando Edmonds-Karp."""
        flow = 0
        parent = [(-1, -1)] * self.n

        while self.bfs(s, t, parent):
            # Encontrar o gargalo do caminho aumentante
            bottleneck = float('inf')
            v = t
            while v != s:
                u, idx = parent[v]
                bottleneck = min(bottleneck, self.graph[u][idx][1])
                v = u

            # Atualizar capacidades residuais ao longo do caminho
            v = t
            while v != s:
                u, idx = parent[v]
                self.graph[u][idx][1] -= bottleneck          # aresta direta
                rev_idx = self.graph[u][idx][2]
                self.graph[v][rev_idx][1] += bottleneck       # aresta reversa
                v = u

            flow += bottleneck
            parent = [(-1, -1)] * self.n

        return flow


# ============================================================
# MÓDULO 2: Construção da Rede de Fluxo (Modelagem do Problema)
# ============================================================

def construir_rede(nk, np_, demands, problems_categories):
    """Constrói a rede de fluxo a partir dos dados do problema.

    Vértices:
        0 = source
        1..nk = categorias
        nk+1..nk+np_ = problemas
        nk+np_+1 = sink

    Arestas:
        source → cat_i: capacidade = demands[i]
        cat_i → prob_j: capacidade = 1 (se problema j pertence à categoria i)
        prob_j → sink: capacidade = 1 (uso único de cada problema)
    """
    source = 0
    sink = nk + np_ + 1
    total_vertices = nk + np_ + 2

    ek = EdmondsKarp(total_vertices)

    # Camada 1: Source → Categorias
    for i in range(nk):
        ek.add_edge(source, i + 1, demands[i])

    # Camada 2 e 3: Categorias → Problemas → Sink
    for j in range(np_):
        problem_node = nk + 1 + j
        ek.add_edge(problem_node, sink, 1)
        for cat in problems_categories[j]:
            ek.add_edge(cat, problem_node, 1)

    return ek, source, sink


def extrair_atribuicao(ek, nk, sink):
    """Recupera a atribuição de problemas a categorias a partir do fluxo."""
    resultado = []
    for i in range(1, nk + 1):
        assigned = []
        for edge in ek.graph[i]:
            v, cap, rev_idx = edge
            if v > nk and v != sink:
                if cap == 0:
                    problem_idx = v - nk
                    assigned.append(problem_idx)
        resultado.append(assigned)
    return resultado


# ============================================================
# MÓDULO 3: Leitura de Entrada e Loop Principal
# ============================================================

def solve():
    """Lê casos de teste e resolve cada um até '0 0'."""
    while True:
        line = input().split()
        if not line:
            break
        nk, np_ = int(line[0]), int(line[1])
        if nk == 0 and np_ == 0:
            break

        demands = list(map(int, input().split()))
        total_demand = sum(demands)

        problems_categories = []
        for j in range(np_):
            parts = list(map(int, input().split()))
            categories = parts[1:]
            problems_categories.append(categories)

        ek, source, sink = construir_rede(nk, np_, demands, problems_categories)
        flow = ek.max_flow(source, sink)

        if flow < total_demand:
            print(0)
        else:
            print(1)
            atribuicao = extrair_atribuicao(ek, nk, sink)
            for problemas in atribuicao:
                print(' '.join(map(str, problemas)))


if __name__ == '__main__':
    solve()
