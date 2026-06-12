# Roteiro de Acompanhamento — UVA 10092: The Problem with the Problem Setter

## 1. Resumo do Problema

Um elaborador de provas precisa selecionar problemas para um teste. Existem **nk** categorias e **np** problemas disponíveis. Cada categoria exige uma quantidade específica de problemas e cada problema pode pertencer a várias categorias, mas **só pode ser usado uma vez**. O objetivo é verificar se é possível atender a demanda de todas as categorias e, em caso positivo, apresentar uma atribuição válida.

## 2. Interpretação da Entrada e Saída

### Entrada
- Primeira linha: `nk` (categorias) e `np` (problemas)
- Segunda linha: `nk` inteiros com a demanda de cada categoria
- Próximas `np` linhas: para cada problema, o número de categorias a que pertence seguido dos índices dessas categorias
- Entrada termina com `0 0`

### Saída
- Se possível: `1` seguido de `nk` linhas com os índices dos problemas atribuídos a cada categoria
- Se impossível: `0`

## 3. Modelagem da Rede de Fluxo

### Vértices

| Vértice | Representa |
|---|---|
| **Source** (0) | Origem — distribui fluxo para as categorias |
| **Categorias** (1 a nk) | Cada categoria que precisa de problemas |
| **Problemas** (nk+1 a nk+np) | Cada problema disponível |
| **Sink** (nk+np+1) | Sorvedouro — coleta os problemas selecionados |

### Arestas

| De | Para | Capacidade | Justificativa |
|---|---|---|---|
| Source | Categoria i | demanda[i] | Limita a quantidade de problemas que a categoria recebe |
| Categoria i | Problema j | 1 | O problema j pode ser atribuído à categoria i (se compatível) |
| Problema j | Sink | 1 | Cada problema é usado no máximo uma vez |

### Verificação

O fluxo máximo é calculado. Se `fluxo == soma_das_demandas`, a atribuição é possível. Caso contrário, é impossível.

## 4. Justificativa: Ford-Fulkerson vs Edmonds-Karp

Escolhemos **Edmonds-Karp** (BFS) porque:

- O Ford-Fulkerson puro (DFS) pode ter complexidade proporcional ao **valor do fluxo**, que no pior caso pode ser grande (soma das demandas até 100)
- O Edmonds-Karp garante **O(V · E²)**, independente do valor do fluxo
- Com nk ≤ 20 e np ≤ 1000, o Edmonds-Karp é eficiente e previsível
- A BFS encontra automaticamente o **caminho mais curto** em número de arestas, o que melhora a convergência

## 5. Instância Pequena

Usando o exemplo do enunciado:

```
3 5
2 2 1
1 1
1 2
1 3
2 1 2
2 2 3
```

- **3 categorias**, **5 problemas**
- Demandas: Cat 1 = 2, Cat 2 = 2, Cat 3 = 1 → Total = 5
- Problema 1: pertence à Cat 1
- Problema 2: pertence à Cat 2
- Problema 3: pertence à Cat 3
- Problema 4: pertence às Cat 1 e 2
- Problema 5: pertence às Cat 2 e 3

### Rede construída

```
Vértices: 0(Source), 1(Cat1), 2(Cat2), 3(Cat3), 4(P1), 5(P2), 6(P3), 7(P4), 8(P5), 9(Sink)

Arestas:
  Source → Cat1: cap=2     Cat1 → P1: cap=1     P1 → Sink: cap=1
  Source → Cat2: cap=2     Cat1 → P4: cap=1     P2 → Sink: cap=1
  Source → Cat3: cap=1     Cat2 → P2: cap=1     P3 → Sink: cap=1
                           Cat2 → P4: cap=1     P4 → Sink: cap=1
                           Cat2 → P5: cap=1     P5 → Sink: cap=1
                           Cat3 → P3: cap=1
                           Cat3 → P5: cap=1
```

## 6. Execução Manual Passo a Passo (Edmonds-Karp)

### Iteração 1 — BFS encontra: Source → Cat1 → P1 → Sink
- Gargalo: min(2, 1, 1) = **1**
- Atualiza: Source→Cat1: 2→1, Cat1→P1: 1→0, P1→Sink: 1→0
- Fluxo acumulado: **1**

### Iteração 2 — BFS encontra: Source → Cat1 → P4 → Sink
- Gargalo: min(1, 1, 1) = **1**
- Atualiza: Source→Cat1: 1→0, Cat1→P4: 1→0, P4→Sink: 1→0
- Fluxo acumulado: **2**

### Iteração 3 — BFS encontra: Source → Cat2 → P2 → Sink
- Gargalo: min(2, 1, 1) = **1**
- Atualiza: Source→Cat2: 2→1, Cat2→P2: 1→0, P2→Sink: 1→0
- Fluxo acumulado: **3**

### Iteração 4 — BFS encontra: Source → Cat2 → P5 → Sink
- Gargalo: min(1, 1, 1) = **1**
- Atualiza: Source→Cat2: 1→0, Cat2→P5: 1→0, P5→Sink: 1→0
- Fluxo acumulado: **4**

### Iteração 5 — BFS encontra: Source → Cat3 → P3 → Sink
- Gargalo: min(1, 1, 1) = **1**
- Atualiza: Source→Cat3: 1→0, Cat3→P3: 1→0, P3→Sink: 1→0
- Fluxo acumulado: **5**

### Iteração 6 — BFS não encontra caminho → **PARADA**

**Fluxo máximo = 5 = soma das demandas (2+2+1) → Solução existe!**

## 7. Verificação da Resposta Final

Arestas saturadas (capacidade residual = 0):
- Cat1 → P1 ✔ → Problema 1 atribuído à Categoria 1
- Cat1 → P4 ✔ → Problema 4 atribuído à Categoria 1
- Cat2 → P2 ✔ → Problema 2 atribuído à Categoria 2
- Cat2 → P5 ✔ → Problema 5 atribuído à Categoria 2
- Cat3 → P3 ✔ → Problema 3 atribuído à Categoria 3

**Saída:**
```
1
1 4
2 5
3
```

✅ Cada categoria recebeu o número exato de problemas exigido.  
✅ Nenhum problema foi usado mais de uma vez.  
✅ Resposta válida e verificada.
