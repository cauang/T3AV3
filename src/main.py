"""
UVA 10092 - The Problem with the Problem Setter
Versão modularizada — ponto de entrada principal.

Este arquivo orquestra a solução:
    1. Lê a entrada do problema (múltiplos casos de teste)
    2. Constrói a rede de fluxo via módulo rede_fluxo
    3. Executa Edmonds-Karp para obter o fluxo máximo
    4. Verifica se o fluxo atende à demanda total
    5. Reconstrói e imprime a atribuição

Uso:
    python src/main.py < dados/entrada_exemplo.txt
"""

import sys
from rede_fluxo import construir_rede, extrair_atribuicao

input = sys.stdin.readline


def solve():
    """Loop principal: lê e resolve cada caso de teste até '0 0'."""
    while True:
        line = input().split()
        if not line:
            break

        nk, np_ = int(line[0]), int(line[1])

        # Condição de parada: nk = 0 e np = 0
        if nk == 0 and np_ == 0:
            break

        # Leitura das demandas de cada categoria
        demands = list(map(int, input().split()))
        total_demand = sum(demands)

        # Leitura dos problemas: quais categorias cada um pertence
        problems_categories = []
        for j in range(np_):
            parts = list(map(int, input().split()))
            # parts[0] = quantidade de categorias, parts[1:] = categorias
            categories = parts[1:]
            problems_categories.append(categories)

        # Construir a rede de fluxo
        ek, source, sink, nk = construir_rede(nk, np_, demands, problems_categories)

        # Calcular fluxo máximo com Edmonds-Karp
        flow = ek.max_flow(source, sink)

        # Verificar se é possível atender todas as categorias
        if flow < total_demand:
            print(0)
        else:
            print(1)
            # Extrair e imprimir a atribuição
            atribuicao = extrair_atribuicao(ek, nk, sink)
            for problemas in atribuicao:
                print(' '.join(map(str, problemas)))


if __name__ == '__main__':
    solve()
