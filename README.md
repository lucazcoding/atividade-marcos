# Atividade de Grafos

Projeto dividido em duas partes: solução do LeetCode 200 e uma aplicação real usando a API do Spotify.

---

## Fase 1 — LeetCode 200: Number of Islands

**Arquivo:** `ATV.200/number_of_island.py`

Dado uma matriz de `"1"` (terra) e `"0"` (água), contar quantas ilhas existem. Uma ilha é formada por terras adjacentes horizontalmente ou verticalmente.

**Algoritmo:** DFS — a cada célula `"1"` encontrada, percorre recursivamente todas as células vizinhas marcando-as como visitadas, até delimitar toda a ilha.

```
Entrada:                Saída:
1 1 0 0 0
1 1 0 0 0   →   3 ilhas
0 0 1 0 0
0 0 0 1 1
```

### Análise de Complexidade — Big O

| Abordagem | Tempo | Espaço | Motivo |
|-----------|-------|--------|--------|
| **Ingênua** — para cada `"1"`, varre a grade inteira procurando vizinhos | O(m² × n²) | O(1) | Loop aninhado para cada célula terra |
| **DFS (nossa solução)** | O(m × n) | O(m × n) | Cada célula é visitada no máximo uma vez |

A solução DFS é significativamente mais eficiente: em uma grade 100×100, a abordagem ingênua faria até 100.000.000 operações, enquanto o DFS faz no máximo 10.000.

---

## Fase 1 — LeetCode 994
# 🍊 Rotting Oranges (BFS)

## 📌 Descrição

Dada uma matriz m x n onde:

* 0 → célula vazia
* 1 → laranja fresca
* 2 → laranja podre

A cada *minuto, uma laranja podre infecta qualquer laranja fresca **adjacente* (cima, baixo, esquerda ou direita).

O objetivo é calcular *quantos minutos são necessários para que todas as laranjas fiquem podres*.

Caso exista alguma laranja fresca que *não possa ser infectada*, o algoritmo retorna:


-1


---

## 🧠 Estratégia do Algoritmo

A solução utiliza *Breadth-First Search (BFS)* para simular a propagação da podridão.

Passos da solução:

1. Percorrer a matriz para localizar:

   * laranjas podres
   * laranjas frescas
2. Inserir todas as laranjas podres em uma *fila*
3. Executar *BFS* para espalhar a podridão
4. Cada *nível da BFS representa 1 minuto*
5. Parar quando não existirem mais laranjas frescas

Esse método é chamado de:


Multi-Source BFS


pois várias laranjas podres iniciam a propagação simultaneamente.

---

## 📊 Análise de Complexidade

A análise utiliza *notação Big-O*, que descreve como o custo do algoritmo cresce conforme o tamanho da entrada aumenta.

Considere uma matriz de tamanho:


m × n


onde:

* m = número de linhas
* n = número de colunas

### ⏱ Complexidade de Tempo

O algoritmo percorre inicialmente toda a matriz para localizar as laranjas:


O(m × n)


Durante o *BFS, cada célula pode ser visitada **no máximo uma vez*, pois uma laranja fresca só pode virar podre uma única vez.

Portanto, a complexidade total do algoritmo é:


O(m × n)


---

### 💾 Complexidade de Espaço

O algoritmo utiliza uma *fila* para executar o BFS.

No pior caso, todas as posições da matriz podem ser inseridas na fila.


O(m × n)


---

## ▶️ Exemplo de Saída

Para a matriz:


2 1 1
1 1 0
0 1 1


Saída esperada:


Minutos necessários: 4


---

## 📚 Conceitos Utilizados

* Breadth-First Search (BFS)
* Multi-Source BFS
* Simulação em matriz
* Estrutura de dados: deque

## Fase 2 — Grau de Separação entre Artistas (Spotify)

**Arquivos:** `API/app.py` e `API/index.html`

Encontra o menor caminho entre dois artistas com base em colaborações reais, usando BFS sobre um grafo de feats.

### Como funciona

Cada artista é um **vértice**. Cada colaboração entre dois artistas é uma **aresta**. O BFS percorre o grafo nível por nível garantindo que o primeiro caminho encontrado seja sempre o menor.

### Análise de Complexidade — Big O

| Abordagem | Tempo | Espaço | Motivo |
|-----------|-------|--------|--------|
| **Ingênua** — verifica todos os pares possíveis de artistas | O(V²) | O(V²) | Compara cada artista com todos os outros |
| **BFS (nossa solução)** | O(V + E) | O(V) | Cada vértice e aresta visitados uma vez |

Com 70 artistas e ~200 colaborações, a abordagem ingênua faria 4.900 comparações, enquanto o BFS percorre apenas os 270 vértices e arestas existentes.

### Pré-requisitos

```
pip install flask flask-cors
```

Conta no [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) para obter `CLIENT_ID` e `CLIENT_SECRET`.

### Configuração

No arquivo `API/app.py`, substitua nas linhas 14-15:

```python
CLIENT_ID     = "seu_client_id"
CLIENT_SECRET = "seu_client_secret"
```

### Como rodar

```bash
cd API
python app.py
```

Acesse `http://localhost:5000` no navegador.

### Rotas disponíveis

| Rota | Descrição |
|------|-----------|
| `GET /` | Interface visual |
| `GET /buscar?origem=X&destino=Y` | Executa o BFS e retorna o caminho |
| `GET /vizinhos?artista=X` | Retorna os artistas com quem X colaborou |
| `GET /artistas` | Lista todos os artistas no grafo |

### Exemplos

| Origem | Destino | Saltos |
|--------|---------|--------|
| Metallica | Drake | 4 |
| Romeo Santos | Kendrick Lamar | 4 |
| Harry Styles | Bad Bunny | 4 |
| Louis Tomlinson | Eminem | 4 |

---

## Conexão entre as fases

| Conceito | LeetCode 200 | Spotify |
|----------|-------------|---------|
| Estrutura | Matriz 2D | Lista de adjacência |
| Vértice | Célula | Artista |
| Aresta | Célula adjacente | Colaboração |
| Algoritmo | DFS | BFS |
| Objetivo | Contar ilhas | Menor caminho |
| Visitados | `grid[r][c] = "0"` | conjunto `visited` |

O raciocínio é o mesmo — explorar um grafo evitando revisitar nós. A diferença é que BFS garante o menor caminho, DFS não.

