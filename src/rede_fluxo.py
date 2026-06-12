"""
Módulo: rede_fluxo.py
Construção e interpretação da rede de fluxo para o problema UVA 10092.

Este módulo é responsável por:
    1. Ler a entrada do problema
    2. Construir a rede de fluxo usando o algoritmo Edmonds-Karp
    3. Interpretar o resultado do fluxo máximo
    4. Reconstruir a atribuição de problemas às categorias

Modelagem da rede:
    ┌──────────────────────────────────────────────────────────┐
    │                                                          │
    │   Source ──(demanda[i])──> Cat_i ──(1)──> Prob_j ──(1)──> Sink   │
    │                                                          │
    └──────────────────────────────────────────────────────────┘

    - Source (vértice 0): origem, distribui fluxo conforme demandas
    - Categorias (vértices 1..nk): cada uma recebe demanda[i] de fluxo
    - Problemas (vértices nk+1..nk+np): cada um permite no máximo 1 uso
    - Sink (vértice nk+np+1): sorvedouro, coleta os problemas selecionados
"""

from edmonds_karp import EdmondsKarp


def construir_rede(nk, np_, demands, problems_categories):
    """Constrói a rede de fluxo a partir dos dados do problema.

    Mapeia o problema de seleção de problemas por categorias em uma
    rede de fluxo bipartida com capacidades.

    Args:
        nk: número de categorias.
        np_: número de problemas disponíveis.
        demands: lista com a demanda de cada categoria (tamanho nk).
        problems_categories: lista de listas, onde problems_categories[j]
                             contém os índices das categorias do problema j+1.

    Returns:
        Tupla (ek, source, sink, nk) onde:
            - ek: instância de EdmondsKarp com a rede construída
            - source: índice do vértice origem
            - sink: índice do vértice sorvedouro
            - nk: número de categorias (para interpretação posterior)
    """
    # Definição dos vértices
    source = 0                  # vértice origem
    sink = nk + np_ + 1         # vértice sorvedouro
    total_vertices = nk + np_ + 2

    ek = EdmondsKarp(total_vertices)

    # Camada 1: Source → Categorias
    # Capacidade = demanda de cada categoria
    # Significado: a categoria i precisa de exatamente demands[i] problemas
    for i in range(nk):
        ek.add_edge(source, i + 1, demands[i])

    # Camada 2 e 3: Categorias → Problemas → Sink
    for j in range(np_):
        problem_node = nk + 1 + j   # vértice do problema j+1

        # Aresta Problema → Sink com capacidade 1
        # Significado: cada problema pode ser usado no máximo UMA vez
        ek.add_edge(problem_node, sink, 1)

        # Arestas Categoria → Problema com capacidade 1
        # Significado: o problema j+1 pode ser atribuído à categoria cat
        for cat in problems_categories[j]:
            ek.add_edge(cat, problem_node, 1)

    return ek, source, sink, nk


def extrair_atribuicao(ek, nk, sink):
    """Recupera a atribuição de problemas às categorias a partir do fluxo.

    Após o cálculo do fluxo máximo, percorre as arestas de cada categoria
    e identifica quais foram saturadas (capacidade residual = 0), indicando
    que o fluxo passou por elas — ou seja, o problema foi atribuído àquela
    categoria.

    Args:
        ek: instância de EdmondsKarp após execução do fluxo máximo.
        nk: número de categorias.
        sink: índice do vértice sorvedouro.

    Returns:
        Lista de listas, onde resultado[i] contém os índices (1-based)
        dos problemas atribuídos à categoria i+1.
    """
    resultado = []

    for i in range(1, nk + 1):
        assigned = []
        for edge in ek.graph[i]:
            v, cap, rev_idx = edge
            # Verifica se o vértice é um problema (não é source nem sink)
            if v > nk and v != sink:
                # Capacidade residual = 0 significa que 1 unidade de fluxo
                # passou por esta aresta (aresta original tinha cap = 1)
                if cap == 0:
                    problem_idx = v - nk   # converte para índice 1-based
                    assigned.append(problem_idx)
        resultado.append(assigned)

    return resultado
