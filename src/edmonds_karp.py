"""
Módulo: edmonds_karp.py
Implementação do algoritmo Edmonds-Karp para fluxo máximo.

O Edmonds-Karp é uma especialização do método Ford-Fulkerson que utiliza
BFS (Busca em Largura) para encontrar caminhos aumentantes, garantindo
complexidade O(V · E²) independente do valor do fluxo.

Estrutura de dados:
    Cada aresta é representada como [destino, capacidade_residual, indice_reversa].
    A aresta reversa (residual) é criada automaticamente com capacidade 0.
    As duas arestas se referenciam mutuamente pelo índice, permitindo
    atualização eficiente do grafo residual.
"""

from collections import deque


class EdmondsKarp:
    """Algoritmo Edmonds-Karp para cálculo de fluxo máximo em redes.

    Atributos:
        n (int): número de vértices da rede.
        graph (list[list]): lista de adjacência com arestas residuais.
    """

    def __init__(self, n):
        """Inicializa a rede de fluxo com n vértices e sem arestas.

        Args:
            n: número total de vértices na rede (incluindo source e sink).
        """
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        """Adiciona uma aresta direcionada u → v com capacidade cap.

        Cria simultaneamente a aresta reversa v → u com capacidade 0.
        As arestas são indexadas de forma cruzada para permitir
        atualização do grafo residual em O(1).

        Args:
            u: vértice de origem.
            v: vértice de destino.
            cap: capacidade da aresta.

        Exemplo:
            Se graph[u] tem k arestas antes da chamada:
            - graph[u][k] = [v, cap, len(graph[v])]     (aresta direta)
            - graph[v][-1] = [u, 0, k]                   (aresta reversa)
        """
        self.graph[u].append([v, cap, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def _bfs(self, source, sink, parent):
        """Busca em largura no grafo residual para encontrar caminho aumentante.

        Percorre apenas arestas com capacidade residual > 0.
        Registra em parent[v] = (u, idx) o nó anterior e o índice da aresta
        usada para chegar a v, permitindo reconstrução do caminho.

        Args:
            source: vértice origem da busca.
            sink: vértice destino (sorvedouro).
            parent: lista para armazenar o caminho encontrado.

        Returns:
            True se existe caminho aumentante, False caso contrário.
        """
        visited = [False] * self.n
        visited[source] = True
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for i, (v, cap, _) in enumerate(self.graph[u]):
                if not visited[v] and cap > 0:
                    visited[v] = True
                    parent[v] = (u, i)
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def max_flow(self, source, sink):
        """Calcula o fluxo máximo de source a sink.

        Funcionamento:
            1. Encontra caminho aumentante via BFS no grafo residual
            2. Calcula o gargalo (menor capacidade residual no caminho)
            3. Atualiza capacidades: subtrai na direta, soma na reversa
            4. Acumula fluxo e repete até não haver mais caminho

        Args:
            source: vértice origem.
            sink: vértice sorvedouro.

        Returns:
            Valor inteiro do fluxo máximo.
        """
        flow = 0
        parent = [(-1, -1)] * self.n

        while self._bfs(source, sink, parent):
            # Passo 1: encontrar gargalo percorrendo o caminho de trás pra frente
            bottleneck = float('inf')
            v = sink
            while v != source:
                u, idx = parent[v]
                bottleneck = min(bottleneck, self.graph[u][idx][1])
                v = u

            # Passo 2: atualizar capacidades residuais
            v = sink
            while v != source:
                u, idx = parent[v]
                self.graph[u][idx][1] -= bottleneck       # aresta direta: diminui
                rev_idx = self.graph[u][idx][2]
                self.graph[v][rev_idx][1] += bottleneck    # aresta reversa: aumenta
                v = u

            flow += bottleneck
            parent = [(-1, -1)] * self.n

        return flow

    def get_flow_on_edge(self, u, edge_index):
        """Retorna o fluxo que passou por uma aresta específica.

        O fluxo é calculado pela capacidade da aresta reversa correspondente
        (que acumula exatamente o fluxo que passou pela aresta direta).

        Args:
            u: vértice de origem da aresta.
            edge_index: índice da aresta na lista de adjacência de u.

        Returns:
            Quantidade de fluxo que passou pela aresta.
        """
        edge = self.graph[u][edge_index]
        v, cap, rev_idx = edge
        # Fluxo = capacidade da aresta reversa
        return self.graph[v][rev_idx][1]
