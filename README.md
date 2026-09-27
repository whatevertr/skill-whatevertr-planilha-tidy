# whatevertr-planilha-tidy

*[Versão em português](README.pt-BR.md)*

A **skill for Claude** (Anthropic) that delivers **data spreadsheets** in **tidy** format — navigable by **humans and by other AIs** (*machine-readable*). One row per record, one column per attribute, no merged cells, real Excel Table, consistent types, and a **Schema** sheet another AI can read without guessing.

Part of the **NUD — Constellation Method**, by Thainá Ramos.

> **Three names, one idea:** *tidy data* (the structure), *machine-readable / AI-navigable* (the property), *clean database* (the use).

---

## What it does

- Turns raw input (messy spreadsheet, pasted data, text) into a **tidy** `.xlsx`: one row = one record, one column = one attribute.
- **No merged cells in data**, single-row headers (prefixes instead of multi-level: `Time - car (years)`), consistent types, ISO-8601 dates.
- Ships every workbook with a **`Premissas`** sheet (prose: sources, limits, methods) and a **`Schema`** sheet (tabular: column · type · unit · domain · example) — the machine-readable contract.
- Optional companions (`--export-companheiros`): `.schema.json` (structure) + `.csv` (data) for AI/pipelines that don't open `.xlsx`.
- Meaning always lives **in the data**, never only in color (a "status" is a column, not a red cell).

Principle: *if you stripped all formatting and exported to CSV, would the information still be complete?* If yes, it's AI-navigable.

## Excel and Google Sheets

The principles are tool-neutral. The builder outputs `.xlsx`, which **imports cleanly into Google Sheets** (structure, colors, freeze, header all survive). The only Excel-specific object is the *Excel Table* (becomes a plain range in Sheets). Native Google Sheets generation is a possible future extension.

## Structure

```
whatevertr-planilha-tidy/
├── SKILL.md                 # skill instructions
├── references/
│   ├── builder_patterns.md      # the spec format + builder.py API
│   ├── navegabilidade_ia.md     # why each rule makes it machine-readable
│   ├── anti_patterns.md         # before/after counter-examples
│   └── dicionario_colunas_exemplo.md  # example Premissas + Schema
├── scripts/
│   └── builder.py           # executable generator (openpyxl) + tidy check
└── assets/
    ├── exemplo_planetas.spec.json     # example input
    └── Exemplo_Planetas_Tidy.xlsx     # example output (+ .csv / .schema.json)
```

## Install

Copy the `whatevertr-planilha-tidy/` folder into your Claude skills directory (`.claude/skills/`). The skill triggers on the cues described in `SKILL.md`.

## Example

The `assets/` folder ships a neutral dataset — **Solar System planets** (diameter, mass, rotation, gases, distance from Earth, travel time by car, plane and light) — so you can see the tidy + Schema pattern before running it on your own data.

```bash
python whatevertr-planilha-tidy/scripts/builder.py \
  --spec whatevertr-planilha-tidy/assets/exemplo_planetas.spec.json \
  --output out/Planetas.xlsx --export-companheiros
```

## License

[CC-BY-4.0](LICENSE). Free to use, with attribution.

---

*NUD (Constellation Method) — method by Thainá Ramos (Nud by Whatevertr) · Licensed under CC-BY-4.0.*
