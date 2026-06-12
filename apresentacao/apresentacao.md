# Apresentação — UVA 10092: The Problem with the Problem Setter

## Grupo I

**Integrantes:** *(preencher)*  
**Linguagem:** Python 3  
**Algoritmo:** Edmonds-Karp (Fluxo Máximo via BFS)

---

## 1. Contexto do Problema (~1 min)

### O que é o problema?

Um elaborador de provas precisa montar um teste com questões de **diversas categorias**. Ele possui um banco com **np** problemas e precisa atender **nk** categorias, cada uma com uma quantidade mínima de problemas exigida.

### Restrição principal

Cada problema pode pertencer a **várias categorias**, mas só pode ser **usado uma vez** na prova — ou seja, se um problema for atribuído a uma categoria, não pode ser reutilizado em outra.

### Objetivo

Determinar se é possível selecionar problemas que atendam a **todas** as demandas simultaneamente. Se sim, mostrar **qual** problema vai para qual categoria.

### Por que é um problema de fluxo?

A restrição de uso único + múltiplas opções de atribuição = **emparelhamento bipartido com demandas**, que se reduz naturalmente a uma rede de fluxo.

---

## 2. Modelagem da Rede de Fluxo (~1 min)

### Estrutura da Rede

```
    Source ──(demanda[i])──→ Categoria_i ──(1)──→ Problema_j ──(1)──→ Sink
```

### Componentes

| Componente | O que representa | Por quê? |
|---|---|---|
| **Source** | Necessidade total de problemas | Distribui fluxo para as categorias conforme suas demandas |
| **Categorias** | Cada tipo de questão exigido | Recebem exatamente a quantidade necessária via capacidade da aresta |
| **Problemas** | Questões disponíveis no banco | Conectados às categorias compatíveis |
| **Sink** | Conclusão da seleção | Capacidade 1 garante uso único de cada problema |

### Capacidades e seu significado

| Aresta | Capacidade | O que limita |
|---|---|---|
| Source → Cat_i | `demanda[i]` | Quantos problemas a categoria i precisa |
| Cat_i → Prob_j | `1` | Compatibilidade: problema j pode servir à categoria i |
| Prob_j → Sink | `1` | **Cada problema é usado no máximo uma vez** |

### Por que funciona?

- Uma unidade de fluxo passando por `Source → Cat_i → Prob_j → Sink` significa: *"o problema j foi atribuído à categoria i"*
- Se o fluxo máximo iguala a soma das demandas, todas as categorias foram atendidas
- A capacidade unitária no Sink garante que nenhum problema é reutilizado

---

## 3. Algoritmo e Grafo Residual (~1 min)

### Algoritmo: Edmonds-Karp

O Edmonds-Karp é uma implementação do Ford-Fulkerson que usa **BFS** para encontrar caminhos aumentantes.

### Funcionamento

1. **BFS** encontra o caminho mais curto de Source a Sink no grafo residual
2. Calcula o **gargalo** (menor capacidade residual no caminho)
3. **Atualiza** o grafo residual:
   - Subtrai o gargalo nas arestas diretas
   - Soma o gargalo nas **arestas reversas**
4. Repete até **não haver mais caminho**

### Por que Edmonds-Karp e não Ford-Fulkerson puro?

- Ford-Fulkerson (DFS): complexidade O(E × f), onde f = valor do fluxo
- **Edmonds-Karp (BFS): complexidade O(V × E²)**, independente do fluxo
- Para este problema, Edmonds-Karp é mais previsível e seguro

### Papel das arestas reversas

As arestas reversas permitem que o algoritmo **corrija decisões anteriores**. Se um problema foi atribuído a uma categoria "errada" em uma iteração, uma iteração posterior pode reverter essa escolha via aresta reversa, encontrando uma solução global ótima.

### Condição de parada

O algoritmo para quando a BFS **não encontra mais caminho** de Source a Sink no grafo residual. O fluxo acumulado é o fluxo máximo.

---

## 4. Interpretação da Resposta (~1 min)

### Como o fluxo vira resposta?

Após o fluxo máximo:

1. **Se fluxo < soma das demandas** → Impossível → Imprime `0`
2. **Se fluxo = soma das demandas** → Possível → Imprime `1` e a atribuição

### Reconstrução da atribuição

Para cada categoria `i`, percorremos suas arestas `Cat_i → Prob_j`:
- Se a **capacidade residual = 0** → fluxo passou → problema `j` foi atribuído à categoria `i`

### Exemplo (do enunciado)

```
Entrada: 3 categorias, 5 problemas, demandas: 2, 2, 1

Fluxo máximo = 5 = 2+2+1 ✓

Atribuição:
  Categoria 1: Problemas 1, 4
  Categoria 2: Problemas 2, 5
  Categoria 3: Problema 3

Saída:
  1
  1 4
  2 5
  3
```

---

## 5. Complexidade e Casos Especiais (~1 min)

### Complexidade

| Aspecto | Valor |
|---|---|
| **Tempo** | O(V · E²), onde V = nk+np+2 e E = O(nk·np) |
| **Espaço** | O(V + E) — lista de adjacência com arestas residuais |

Para os limites do problema (nk ≤ 20, np ≤ 1000):
- V ≤ 1.022 e E ≤ ~21.000 → execução rápida

### Casos especiais tratados

| Caso | O que acontece |
|---|---|
| Categoria sem problemas compatíveis | Fluxo < demanda → imprime `0` |
| Problema sem categorias | Não recebe aresta de categoria, é ignorado |
| Demanda total > np | Impossível, fluxo máximo ≤ np < demanda |
| Múltiplos casos de teste | Loop lê até `0 0` |
| Problema pertence a várias categorias | Múltiplas arestas Cat→Prob, mas cap=1 no Sink garante uso único |
| Todos os problemas usados | Fluxo = np e np ≥ demanda → funciona |

### Conclusão

O problema de seleção de problemas por categorias se reduz elegantemente a uma rede de fluxo bipartida. O Edmonds-Karp resolve de forma eficiente e correta, e a atribuição é recuperada diretamente das arestas saturadas.
