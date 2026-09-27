# Anti-padrões — O que NÃO fazer

Erros comuns que quebram o padrão tidy / navegável por IA. Aprenda pelos contraexemplos. Tema neutro: dados de planetas.

---

## 1. Mesclar células para "fazer cabeçalho hierárquico"

### ❌ Errado
```
| Tempo de viagem                        |
| Carro (anos) | Avião (anos) | Luz (min) |
| 623          | 69           | 3.0        |
```
A primeira linha tem células mescladas ("Tempo de viagem" cobrindo três colunas).

### ✅ Certo — prefixo no nome, em UMA linha de header
```
| Tempo - carro a 100 km/h (anos) | Tempo - avião a 900 km/h (anos) | Tempo - luz (minutos) |
| 623                             | 69                              | 3.0                   |
```
**Por quê:** merge quebra filtro, tabela dinâmica e leitura por IA (as células "de baixo" ficam vazias para a máquina). Header de uma linha é a única forma que BI e IA consomem bem.

---

## 2. Linhas de "subtotal" no meio da tabela

### ❌ Errado
```
| Tipo            | Planeta   | Número de luas |
| rochoso         | Terra     | 1              |
| rochoso         | Marte     | 2              |
| TOTAL ROCHOSOS  |           | 3              |
| gigante gasoso  | Júpiter   | 95             |
```

### ✅ Certo
- A aba detalhada tem só uma linha por registro (um planeta), sem totais embutidos.
- Subtotais vão em outra aba (Resumo) ou na `total_row` do Excel Table (no rodapé).
- Assim o "Subtotal" do Excel e qualquer agregação de IA funcionam — porque cada linha é um registro puro.

---

## 3. Empilhar dois conceitos na mesma coluna

### ❌ Errado
```
| Rotação          |
| 24,6 horas       |
| 5.832,5 h (retró)|
```

### ✅ Certo
```
| Período de rotação (horas) | Sentido de rotação |
| 24.6                       | direto             |
| 5832.5                     | retrógrado         |
```
O número fica puro (comparável, somável) e o sentido vira coluna de domínio fechado.

---

## 4. Usar formatação para guardar informação

### ❌ Errado
"Os planetas em vermelho giram em sentido retrógrado."

### ✅ Certo
Coluna `Sentido de rotação` com valores explícitos (`direto` / `retrógrado`). A formatação condicional pode pintar a célula com base na coluna, mas a informação está NO DADO.

**Por quê:** dados precisam sobreviver à exportação para CSV, Power BI, banco SQL e leitura por IA — onde cor não existe.

---

## 5. Usar `pandas.to_excel()` sem estilo/estrutura

### ❌ Errado
```python
df.to_excel('planetas.xlsx', index=False)  # pronto?
```
Resultado: área retangular sem Excel Table, sem freeze, sem larguras, sem Schema. Funciona como "dump", não é o padrão da skill.

### ✅ Certo
Use o `scripts/builder.py` (openpyxl): ele cria Table, Schema, Premissas, freeze, formatos e roda o check tidy. Ver `builder_patterns.md`.

---

## 6. Nomes de coluna diferentes entre abas para a mesma coisa

### ❌ Errado
- Aba "Planetas" tem `Diâmetro equatorial (km)`
- Aba "Resumo" tem `Tamanho`
- Aba "Comparação" tem `Diâmetro (km)`

### ✅ Certo
Nome canônico definido no Schema e usado igual em todas as abas: `Diâmetro equatorial (km)`. A IA referencia pela coluna — nome instável obriga adivinhação.

---

## 7. Esquecer a aba Premissas / Schema

Mesmo planilha simples precisa delas. Sem Premissas (prosa) e Schema (tabular), daqui a 2 meses ninguém lembra a fonte, e nenhuma IA sabe o tipo/unidade de cada coluna. **Premissas + Schema são o README e o contrato da planilha.**

---

## 8. Inventar dado para "completar"

### ❌ Errado
Não se sabe o número exato de luas → chuta um valor "para ficar completo".

### ✅ Certo
- Deixe em branco (pintado de laranja `FFEFE0`) ou registre o valor com a limitação.
- A Premissas explica ("nº de luas é aproximado, cresce com novas descobertas").
- Nunca troque "não sei" por um número inventado.

---

## 9. Header de tabela na linha 1 quando há nota explicativa

### ❌ Errado
```
Linha 1: "Dados públicos; distância à Terra é aproximada..."
Linha 2: Header
```
…mas a Excel Table foi definida com `ref='A1:O10'` — e a linha 1 (nota) vira "registro 1".

### ✅ Certo
- Linha 1: nota com merge (NÃO é parte da tabela).
- Linha 2: header. Linha 3+: dados.
- `ref='A2:O{ultima_linha}'` na Table. (O builder já faz isso.)

---

## 10. Abreviações sem documentação

### ❌ Errado
| DiamKm | PerRot | NLua |

### ✅ Certo
| Diâmetro equatorial (km) | Período de rotação (horas) | Número de luas confirmadas |

Se precisar abreviar por largura, documente no Schema. A IA e o humano leem o nome — nome claro é auto-descrição.
