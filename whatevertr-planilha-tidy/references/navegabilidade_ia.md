# Navegável por IA (machine-readable) — por que cada regra ajuda a máquina

Uma planilha "navegável por IA" é aquela que **outra IA consegue ler e usar sem adivinhar** a estrutura. É a mesma disciplina do *tidy data*, com uma camada a mais de **auto-descrição**. Este documento explica o porquê de cada regra — para quem executa a skill não tratar as regras como capricho estético.

## O princípio
Uma IA (ou um script, ou o Power BI) **não vê a formatação como um humano vê**. Ela lê células, tipos e nomes. Tudo que estiver só no "visual" (cor, merge, um título solto no meio) **some** quando o dado é exportado, consultado por API, ou lido por um modelo. Logo: **o significado precisa estar no dado e na estrutura declarada, não no desenho.**

## Regra por regra

| Regra | Por que a máquina precisa |
|---|---|
| **Uma linha = um registro** | A IA itera linha a linha esperando um registro por linha. Uma "linha de subtotal" no meio vira um registro falso e contamina qualquer agregação. |
| **Uma coluna = um atributo** | Permite tipar a coluna inteira. "10 min" numa coluna quebra o tipo (texto+número misturados) e a IA não consegue somar/comparar. |
| **Cabeçalho em uma linha** | A IA assume header na primeira linha (ou na declarada). Cabeçalho de dois níveis (merge) faz ela ler nome de coluna errado. Use prefixo: `Tempo - carro (anos)`. |
| **Sem merge em dados** | Célula mesclada tem valor só na primeira célula do bloco; as demais viram vazio. A IA lê buracos onde havia informação. |
| **Tipos consistentes + datas ISO 8601** | `2026-09-25` é inequívoco; `25/09/26` é ambíguo (mês? dia?) e depende de local. ISO é a única forma que toda máquina lê igual. |
| **Significado no dado, não na cor** | "linhas vermelhas = retrógrado" é invisível para a IA. Vira coluna `Sentido de rotação` com valor `retrógrado`. |
| **Nomes de coluna estáveis e sem abreviação obscura** | A IA referencia a coluna pelo nome. `QtdProc` obriga adivinhação; `Quantidade de processos` é auto-explicativo. Mesmo nome em todas as abas. |
| **Aba Schema** | É o **contrato**: tipo, unidade, domínio e exemplo de cada coluna, em formato tabular. A IA lê o Schema primeiro e já sabe o que esperar do dado — não precisa inferir. |
| **Companheiros `.csv` + `.schema.json`** | Uma IA que não abre `.xlsx` (ou que trabalha por API) lê o `.csv` (dados puros) e o `.schema.json` (estrutura) direto. |

## A aba Schema (o coração da navegabilidade)
Uma linha por coluna de dado, com:
- **Coluna** — nome exato (igual ao header).
- **Tipo** — texto / inteiro / número / data (ISO) / booleano.
- **Unidade** — km, horas, 10^6 km, anos… (quando numérico).
- **Domínio / Valores** — o conjunto permitido, quando fechado (ex.: `direto | retrógrado`).
- **Exemplo** — um valor real da coluna.
- **Descrição** — o que a coluna significa.

Com isso, uma IA que recebe a planilha sabe, antes de ler qualquer dado, que "Tipo" só assume três valores, que "Diâmetro" está em km, e que "Distância mínima à Terra" é aproximada (se a descrição disser).

## Companheiros de máquina (opcional, mas recomendado)
O builder gera com `--export-companheiros`:
- **`nome.schema.json`** — a estrutura em JSON (o Schema legível por programa).
- **`nome.csv`** — os dados da primeira aba em CSV puro (sem formatação, sem merge, sem cor — só dado).

Regra de ouro: **se você removesse toda a formatação e exportasse para CSV, a informação continuaria completa?** Se sim, a planilha é navegável por IA. Se não (algo só existia na cor, no merge ou num título solto), ainda não é.
