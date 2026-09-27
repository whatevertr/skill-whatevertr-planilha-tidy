# Builder — formato do `spec` e API do `scripts/builder.py`

O código real é executável em `scripts/builder.py` (openpyxl). Você **não copia trechos**: monta um `spec` (JSON) e roda o builder. Ele cria as abas de dados, a aba **Schema** (legível por máquina) e a aba **Premissas**, aplica estilos/Excel Table/freeze/formatos e roda um **check tidy** ao final.

## Rodar

```bash
python scripts/builder.py --spec spec.json --output /caminho/saida.xlsx --export-companheiros
```

- `--export-companheiros` (opcional): também gera `saida.schema.json` (estrutura) e `saida.csv` (dados da 1ª aba), para consumo por IA sem abrir o `.xlsx`.
- Sem dependência de `recalc.py` nem de caminhos externos. Só precisa de `openpyxl` (e `pandas` é **opcional**, não exigido).

## Formato do `spec` (JSON)

```json
{
  "titulo": "Dados dos Planetas do Sistema Solar",
  "abas": [
    {
      "nome": "Planetas",
      "display_name": "Planetas",
      "nota": "Texto opcional da linha 1 (fica com merge — não é dado).",
      "colunas": [
        {"nome": "Planeta", "tipo": "texto", "exemplo": "Marte",
         "descricao": "Nome do planeta."},
        {"nome": "Diâmetro equatorial (km)", "tipo": "inteiro", "unidade": "km",
         "formato": "#,##0", "exemplo": 6792, "descricao": "Diâmetro no equador."},
        {"nome": "Tipo", "tipo": "texto",
         "dominio": "rochoso | gigante gasoso | gigante de gelo",
         "exemplo": "rochoso", "descricao": "Classificação."},
        {"nome": "Prioridade de estudo", "tipo": "texto", "preencher": true,
         "descricao": "Em branco — preenchimento do usuário."}
      ],
      "dados": [
        {"Planeta": "Marte", "Diâmetro equatorial (km)": 6792, "Tipo": "rochoso"}
      ]
    }
  ],
  "premissas": [
    ["1. Fontes de dados", [["Fatos planetários", "NASA Planetary Fact Sheet (domínio público)"]]],
    ["2. Limitações conhecidas", [["Distância à Terra", "aproximada; varia com a órbita"]]]
  ]
}
```

### Campos de uma coluna
| Campo | Obrigatório | O que é |
|---|---|---|
| `nome` | sim | Header exato (com unidade entre parênteses quando fizer sentido). |
| `tipo` | sim | `texto` \| `inteiro` \| `número` \| `data` \| `booleano`. Data → ISO 8601 (`YYYY-MM-DD`). |
| `unidade` | recomendado (numérico) | km, horas, anos… Vai para o Schema. |
| `dominio` | quando fechado | Valores possíveis, ex.: `direto | retrógrado`. Vai para o Schema. |
| `formato` | opcional | Formato Excel (`#,##0`, `#,##0.00`). Se ausente, usa padrão por tipo. |
| `exemplo` | recomendado | Um valor real — vai para o Schema. |
| `descricao` | recomendado | O que a coluna significa — vai para o Schema. |
| `preencher` | opcional | `true` = coluna fica vazia e pintada de laranja (editável). |

## O que o builder garante (automático)
- **Aba de dados:** header em uma linha (azul-escuro), corpo Arial 10 com wrap, larguras calibradas, formatos numéricos, freeze abaixo do header, Excel Table (`display_name`). Nota opcional na linha 1 (com merge, fora da Table).
- **Aba `Schema`:** uma linha por coluna (Aba, Coluna, Tipo, Unidade, Domínio, Exemplo, Descrição) — o contrato legível por máquina.
- **Aba `Premissas`:** seções (fundo azul claro) com pares chave/valor, a partir de `spec["premissas"]`.
- **Ordem das abas:** dados… → Schema → Premissas.
- **Check tidy pós-build:** acusa `ALERTA TIDY` se faltar Excel Table ou houver merge fora da linha 1.

## Convenção de cores (constantes no topo do builder)
| Cor | Uso |
|---|---|
| `1F4E78` azul-escuro | cabeçalho das tabelas |
| `FFF2CC` amarelo claro | nota explicativa (linha 1) |
| `FFEFE0` laranja claro | célula em branco para preenchimento |
| `D9E1F2` azul claro | títulos de seção na Premissas |

*(A autora pode ajustar os hex para a paleta NUD — são constantes nomeadas no `builder.py`.)*

## Colunas calculadas / comparações
Quando quiser uma coluna derivada (ex.: tempo de viagem = distância ÷ velocidade), há duas opções:
1. **Calcular no montador do `spec`** (Python), gravando o número pronto — recomendado para valores fixos (é o que o exemplo dos planetas faz). Vantagem: a planilha sai com dado puro, mais navegável por IA que uma fórmula.
2. **Fórmula Excel** (se o usuário precisa editar e ver recalcular) — grave a string `=...` na célula. Nesse caso, teste abrindo no Excel/Sheets; não dependa de recalculadores externos.

Para dados de referência (como os planetários), **prefira a opção 1**: número pronto é mais navegável que fórmula.

## Checklist final antes de entregar
- [ ] Toda aba de dados tem Excel Table (o check tidy confirma).
- [ ] Zero merge em área de dados (só na nota da linha 1).
- [ ] Abas `Premissas` e `Schema` presentes.
- [ ] `freeze_panes` e larguras aplicados; datas em ISO 8601.
- [ ] Colunas em branco pintadas de laranja e explicadas na Premissas.
- [ ] `--export-companheiros` se o consumidor for IA/pipeline.
- [ ] Nenhum dado sensível/privado no conteúdo (usar exemplo neutro para material público).
