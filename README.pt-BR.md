# whatevertr-planilha-tidy

*[English version](README.md)*

Uma **skill para Claude** (Anthropic) que entrega **planilhas de dados** em formato **tidy** — navegáveis por **humano e por outra IA** (*machine-readable*). Uma linha por registro, uma coluna por atributo, sem células mescladas, com Excel Table real, tipos consistentes e uma aba **Schema** que outra IA lê sem adivinhar.

Faz parte do **NUD — Constellation Method**, de Thainá Ramos.

> **Três nomes, uma ideia:** *tidy data* (a estrutura), *navegável por IA / machine-readable* (a propriedade), *base de dados limpa* (o uso).

---

## O que faz

- Transforma insumo bruto (planilha bagunçada, dados colados, texto) num `.xlsx` **tidy**: uma linha = um registro, uma coluna = um atributo.
- **Sem merge em dados**, cabeçalho de uma linha (prefixo em vez de multi-nível: `Tempo - carro (anos)`), tipos consistentes, datas em ISO 8601.
- Toda planilha sai com aba **`Premissas`** (prosa: fontes, limitações, métodos) e aba **`Schema`** (tabular: coluna · tipo · unidade · domínio · exemplo) — o contrato legível por máquina.
- Companheiros opcionais (`--export-companheiros`): `.schema.json` (estrutura) + `.csv` (dados) para IA/pipeline que não abre `.xlsx`.
- O significado mora **no dado**, nunca só na cor (um "status" é coluna, não célula vermelha).

Princípio: *se você tirasse toda a formatação e exportasse para CSV, a informação continuaria completa?* Se sim, é navegável por IA.

## Excel e Google Sheets

Os princípios são agnósticos de ferramenta. O builder gera `.xlsx`, que **importa liso no Google Sheets** (estrutura, cores, freeze e header sobrevivem). O único objeto específico do Excel é a *Excel Table* (vira intervalo comum no Sheets). Geração nativa no Google Sheets é uma extensão futura possível.

## Estrutura

```
whatevertr-planilha-tidy/
├── SKILL.md                 # instruções da skill
├── references/
│   ├── builder_patterns.md      # o formato do spec + API do builder.py
│   ├── navegabilidade_ia.md     # por que cada regra torna a planilha legível por máquina
│   ├── anti_patterns.md         # contraexemplos antes/depois
│   └── dicionario_colunas_exemplo.md  # exemplo de Premissas + Schema
├── scripts/
│   └── builder.py           # gerador executável (openpyxl) + check tidy
└── assets/
    ├── exemplo_planetas.spec.json     # insumo de exemplo
    └── Exemplo_Planetas_Tidy.xlsx     # saída de exemplo (+ .csv / .schema.json)
```

## Como instalar

Copie a pasta `whatevertr-planilha-tidy/` para o diretório de skills do seu Claude (`.claude/skills/`). A skill é acionada pelos gatilhos descritos no `SKILL.md`.

## Exemplo

O `assets/` traz um conjunto neutro — **planetas do Sistema Solar** (diâmetro, massa, rotação, gases, distância da Terra, tempo de viagem de carro, avião e à velocidade da luz) — para você ver o padrão tidy + Schema antes de rodar com os seus dados.

```bash
python whatevertr-planilha-tidy/scripts/builder.py \
  --spec whatevertr-planilha-tidy/assets/exemplo_planetas.spec.json \
  --output out/Planetas.xlsx --export-companheiros
```

## Licença

[CC-BY-4.0](LICENSE). Uso livre, com atribuição.

---

*NUD (Constellation Method) — método de Thainá Ramos (Nud by Whatevertr) · Licenciado sob CC-BY-4.0.*
