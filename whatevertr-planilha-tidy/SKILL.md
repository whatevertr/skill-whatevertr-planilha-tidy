---
name: whatevertr-planilha-tidy
description: "Use SEMPRE que o usuário pedir para consolidar, estruturar, organizar ou entregar DADOS em planilha (Excel/.xlsx ou Google Sheets) — 'base de dados', 'base mestre', 'dados consolidados', 'tabela para BI/Power BI/tabela dinâmica/pivot', 'planilha organizada', 'planilha limpa', 'sem células mescladas', 'formato de tabela', ou quando descrever a saída como algo que será filtrado, analisado, cruzado ou lido por outra IA. Também acione quando o usuário pedir uma planilha 'navegável por IA', 'machine-readable', 'legível por máquina' ou 'tidy'. Entrega dados em formato TIDY (uma linha por registro, uma coluna por atributo), sem células mescladas, com Excel Table, tipos consistentes, painel congelado, aba Premissas e aba Schema (dicionário legível por máquina) — pronta para humano E para IA. NÃO acione para planilha de apresentação/impressão, modelo financeiro cheio de fórmulas de cálculo, ou lista trivial; esta skill é para o padrão 'dados navegáveis'."
license: CC-BY-4.0
---

# NUD Planilha Tidy

Skill para entregar planilhas de **dados** em formato **tidy** — navegáveis por **humano e por IA** (*machine-readable*). Uma linha por registro, uma coluna por atributo, sem células mescladas, com Excel Table, tipos consistentes e um **Schema** que outra IA lê sem adivinhar.

Faz parte do **NUD — Constellation Method**, de Thainá Ramos.

> **Três nomes para a mesma ideia:** *tidy data* (a estrutura), *machine-readable / navegável por IA* (a propriedade), *base de dados limpa* (o uso). A skill entrega os três.

## Escopo — quando SIM e quando NÃO

**SIM** — o entregável é **DADO** (vai ser filtrado, ordenado, cruzado, pivotado, alimentar BI, ou ser lido por outra IA).

**NÃO** (a cerca) — não force o padrão tidy quando o entregável é:
- **planilha de apresentação/impressão** (layout desenhado para o olho, não para análise);
- **modelo de cálculo** cheio de fórmulas encadeadas (simulador financeiro, orçamento com cenários);
- **lista trivial** (uma coluna, meia dúzia de itens).

Na dúvida entre "dado" e "apresentação", **pergunte**: *"esta planilha vai ser analisada/lida por máquina, ou é para exibição?"*

## Excel e Google Sheets (tool-neutral)

Os princípios (tidy, sem merge, header único, tipado, machine-readable) valem **igual** para Excel e Google Sheets — é o que torna a planilha navegável em qualquer ferramenta e por qualquer IA. O `scripts/builder.py` gera **`.xlsx`**, que **importa direto no Google Sheets** preservando estrutura, cores, freeze e header. A **única** coisa Excel-específica é o objeto *Excel Table* (Ctrl+T): no Sheets ele vira um intervalo comum (não quebra nada). Geração **nativa** no Google Sheets (via API/Apps Script) é uma extensão futura possível, não requerida pelo núcleo.

## Princípios inegociáveis

1. **Uma linha = um registro.** Nunca repetir cabeçalho em linhas intermediárias; nunca "linha de título" cobrindo colunas no meio da tabela.
2. **Uma coluna = um atributo único.** Nunca empilhar dois conceitos na mesma célula (ex.: "10 min" → separe valor e unidade; sentido de rotação é coluna própria, não o sinal de um número).
3. **Zero células mescladas em áreas de dados.** Tolerável só em nota explicativa na linha 1.
4. **Toda área de dados vira Excel Table** (`displayName` único, `TableStyleMedium2`) — ativa filtro e referência por nome.
5. **Cabeçalho em UMA linha.** Se precisar agrupar, use prefixo no nome (`Tempo - carro (anos)`, `Tempo - avião (anos)`), nunca cabeçalho multi-nível.
6. **Tipos consistentes por coluna.** Número é número, data é **ISO 8601 (YYYY-MM-DD)**, texto é texto. String vazia/`" - "` vira vazio em coluna numérica.
7. **Significado mora no DADO, nunca só na cor.** Se "atrasado"/"retrógrado" é informação, vira **coluna** (`Status`, `Sentido de rotação`). A cor pode realçar, mas o dado sobrevive a CSV/BI/IA.
8. **Aba `Premissas` obrigatória** — fontes, limitações, métodos, dicionário, convenções. É o README da planilha.
9. **Aba `Schema` obrigatória (navegável por IA)** — uma linha por coluna: nome · tipo · unidade · domínio · exemplo · descrição. É o dicionário **legível por máquina**.
10. **Painel congelado + larguras calibradas + formatos numéricos** aplicados.

## Camada "navegável por IA" (o diferencial)

Além do tidy (que já ajuda máquina), esta skill entrega o que uma IA precisa para **ancorar a estrutura sem adivinhar**:

- **Aba `Schema`**: tipo, unidade e domínio de cada coluna, de forma tabular.
- **Datas em ISO 8601**, tipos declarados, nomes de aba estáveis, um conceito por célula.
- **Companheiros opcionais** (`--export-companheiros`): `nome.schema.json` (estrutura) e `nome.csv` (dados) ao lado do `.xlsx`, para a IA ler sem abrir a planilha.
- Detalhes e o "porquê de cada regra ajudar a máquina" em `references/navegabilidade_ia.md`.

## Fluxo de trabalho

1. **Ler o insumo** (planilha bruta, texto, dados colados). Não confiar que o header está na linha 1 — verificar.
2. **Modelar tidy:** definir as colunas (um conceito cada), tipos, unidades e domínios. Desnormalizar hierarquia (nível vira coluna repetida + coluna de *path*) se houver.
3. **Limpar tipos:** vazio→`None` em coluna numérica; datas→ISO; texto→`strip()`.
4. **Montar o `spec` (JSON)** com `abas` (colunas + dados) e `premissas`. Ver `references/builder_patterns.md` para o formato.
5. **Gerar com o builder:**
   ```bash
   python scripts/builder.py --spec spec.json --output /caminho/saida.xlsx --export-companheiros
   ```
   O builder cria as abas de dados + `Schema` + `Premissas`, aplica estilos/Table/freeze e roda um **check tidy** (sem merge em dados, Table presente). Se aparecer `ALERTA TIDY`, corrija antes de entregar.
6. **Entregar** o `.xlsx` (e, se pedido, os companheiros), com um resumo curto: quantas abas, colunas em branco para preencher (laranja), limitações registradas na Premissas.

## Perguntas ao usuário (no máximo 3-4, enxutas)

1. **Quais abas?** (Detalhado é o mínimo; há Resumo/cruzamento?)
2. **Quais campos ficam em branco para preenchimento futuro?** (Vão em laranja `FFEFE0`.)
3. **Mapeamentos de domínio** a aplicar? (Agrupar X sob Y, traduzir códigos.)
4. **Hierarquia presente?** Se sim, a sequência completa (do mais amplo ao mais granular).

## Anti-padrões (o que NÃO fazer)
Resumo — exemplos com antes/depois em `references/anti_patterns.md`:
- ❌ mesclar célula para "cabeçalho hierárquico" → ✅ prefixo em header de uma linha.
- ❌ subtotal no meio da tabela → ✅ Resumo em outra aba (ou `total_row`).
- ❌ dois conceitos numa coluna → ✅ separar (valor, unidade, e coluna calculada).
- ❌ significado só na cor → ✅ coluna explícita.
- ❌ `pandas.to_excel` cru (sem Table/estilo) → ✅ usar o builder.
- ❌ inventar dado que não existe → ✅ deixar em branco (laranja) + registrar na Premissas.
- ❌ esquecer Premissas/Schema.

## Documentos de referência
- `references/builder_patterns.md` — formato do `spec` e a API do `scripts/builder.py`.
- `references/navegabilidade_ia.md` — por que cada regra torna a planilha legível por máquina/IA.
- `references/anti_patterns.md` — contraexemplos com antes/depois.
- `references/dicionario_colunas_exemplo.md` — exemplo de Premissas/Schema bem feitos (tema: dados astronômicos).
- `scripts/builder.py` — gerador executável (openpyxl), com check tidy e export de companheiros.
- `assets/Exemplo_Planetas_Tidy.xlsx` + `assets/exemplo_planetas.spec.json` — exemplo neutro pronto (planetas do Sistema Solar).

## Exemplo
O `assets/` traz um conjunto neutro — **planetas do Sistema Solar** (diâmetro, massa, rotação, gases, distância à Terra, tempo de viagem a 100 km/h, 900 km/h e à velocidade da luz) — para você ver o padrão tidy + Schema antes de rodar com os seus dados.

---
*NUD (Constellation Method) — método de Thainá Ramos (Nud by Whatevertr) · Licenciado sob CC-BY-4.0.*
