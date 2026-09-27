# Exemplo de aba Premissas e aba Schema bem feitas

Use como template. Tema neutro: **dados dos planetas do Sistema Solar** (o mesmo do `assets/Exemplo_Planetas_Tidy.xlsx`). Dados de domínio público (base NASA Planetary Fact Sheet).

## Aba Premissas (prosa — para o humano)

```
PREMISSAS E DICIONÁRIO

1. Fontes de dados
   Fatos planetários   →  NASA Planetary Fact Sheet (domínio público):
                          diâmetro, massa, rotação, período orbital, gases.
   Tempos de viagem    →  Calculados: distância mínima à Terra ÷ velocidade.
                          Luz a 299.792,458 km/s.

2. Limitações conhecidas
   Distância mínima à Terra   →  Aproximada; varia continuamente com as órbitas.
                          A da Terra é 0 (referência).
   Número de luas      →  Confirmadas até a compilação; cresce com novas descobertas.
   Sentido de rotação  →  Vênus e Urano giram em sentido retrógrado; registrado em
                          COLUNA PRÓPRIA, não no sinal do número de rotação.

3. Métodos de cálculo
   Tempo (anos)        →  distância_km ÷ velocidade_km/h ÷ 24 ÷ 365,25.
   Tempo - luz (min)   →  distância_km ÷ 299.792,458 ÷ 60.

4. Convenção de cores
   Azul-escuro (1F4E78)   →  Cabeçalho das tabelas.
   Amarelo claro (FFF2CC) →  Nota explicativa no topo da aba.
   Laranja claro (FFEFE0) →  Célula em branco para preenchimento (ex.: Prioridade de estudo).
   Azul claro (D9E1F2)    →  Títulos de seção na Premissas.

5. Navegável por IA
   Schema        →  A aba Schema traz coluna, tipo, unidade, domínio e exemplo.
   Companheiros  →  Opcional: .csv (dados) e .schema.json (estrutura) ao lado do .xlsx.
```

## Aba Schema (tabular — para a máquina/IA)

Uma linha por coluna de dado. É o **contrato** que uma IA lê antes do dado.

| Aba | Coluna | Tipo | Unidade | Domínio / Valores | Exemplo | Descrição |
|---|---|---|---|---|---|---|
| Planetas | Planeta | texto | | | Marte | Nome do planeta. |
| Planetas | Tipo | texto | | rochoso \| gigante gasoso \| gigante de gelo | rochoso | Classificação. |
| Planetas | Diâmetro equatorial (km) | inteiro | km | | 6792 | Diâmetro no equador. |
| Planetas | Massa (10^24 kg) | número | 10^24 kg | | 0.642 | Massa. |
| Planetas | Distância média ao Sol (10^6 km) | número | 10^6 km | | 227.9 | Semieixo maior da órbita. |
| Planetas | Distância mínima à Terra (10^6 km) | número | 10^6 km | | 54.6 | Aproximação mínima (aprox.; varia). |
| Planetas | Período de rotação (horas) | número | horas | | 24.6 | Dia sideral. |
| Planetas | Sentido de rotação | texto | | direto \| retrógrado | direto | Conceito próprio (não no sinal do número). |
| Planetas | Período orbital (dias terrestres) | número | dias | | 687.0 | Duração do ano. |
| Planetas | Número de luas confirmadas | inteiro | luas | | 2 | Satélites confirmados (aprox.). |
| Planetas | Gases atmosféricos principais | texto | | | CO2, N2, Ar | Principais gases observados. |
| Planetas | Tempo - carro a 100 km/h (anos) | número | anos | | 623 | Viagem hipotética a 100 km/h. |
| Planetas | Tempo - avião a 900 km/h (anos) | número | anos | | 69 | Viagem hipotética a 900 km/h. |
| Planetas | Tempo - luz (minutos) | número | minutos | | 3.0 | Tempo que a luz leva no vácuo. |
| Planetas | Prioridade de estudo | texto | | | | Em branco — preenchimento do usuário. |

## O que este exemplo ensina
- **Unidade no nome da coluna** (`(km)`, `(10^6 km)`, `(anos)`) — a máquina lê a unidade sem adivinhar.
- **Domínio fechado declarado** (`direto | retrógrado`) — a IA sabe os valores possíveis.
- **Conceito separado em coluna** — o sentido de rotação é coluna, não o sinal do número de rotação (anti-padrão nº 4).
- **Prefixo em vez de cabeçalho multi-nível** — `Tempo - carro (anos)` / `Tempo - avião (anos)` (anti-padrão nº 1).
- **Limitação registrada** — distância e nº de luas são aproximados; quem consome sabe disso.

## Como gerar
Ver `builder_patterns.md`. A aba Premissas sai de `spec["premissas"]` e a aba Schema sai automaticamente de `spec["abas"][*]["colunas"]` — a mesma definição alimenta o dado e o contrato.
