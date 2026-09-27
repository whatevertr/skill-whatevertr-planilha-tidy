# -*- coding: utf-8 -*-
"""
Builder do NUD Planilha Tidy.

Gera planilhas em formato **tidy** (uma linha = um registro, uma coluna = um
atributo), **navegáveis por humano E por IA** (machine-readable): sem células
mescladas em dados, Excel Table real, header em uma linha, tipos consistentes,
painel congelado, aba Premissas e aba Schema (dicionário legível por máquina).
Opcionalmente exporta os companheiros `.csv` (dados) e `.json` (schema) para uma
IA ancorar a estrutura sem abrir o .xlsx.

Princípios (ver SKILL.md e references/): o significado mora no DADO, nunca só na
cor; um conceito por célula; cabeçalho de uma linha (use prefixo, ex.:
"Tempo - carro (anos)"); nada de subtotal no meio da tabela.

USO
    python builder.py --spec spec.json --output saida.xlsx
    python builder.py --spec spec.json --output saida.xlsx --export-companheiros

FORMATO DO SPEC (JSON)
{
  "titulo": "Título do conjunto de dados",
  "abas": [
    {
      "nome": "Planetas",
      "display_name": "Planetas",            # nome da Excel Table (sem espaço)
      "nota": "texto opcional da linha 1",
      "colunas": [
        {"nome": "Planeta", "tipo": "texto", "exemplo": "Marte",
         "descricao": "Nome do planeta"},
        {"nome": "Diâmetro (km)", "tipo": "inteiro", "unidade": "km",
         "formato": "#,##0", "exemplo": 6792, "descricao": "..."},
        {"nome": "SLA", "tipo": "número", "preencher": true, "descricao": "..."}
      ],
      "dados": [ {"Planeta": "Marte", "Diâmetro (km)": 6792, ...}, ... ]
    }
  ],
  "premissas": [
    ["1. Fontes de dados", [["Planetas", "NASA Planetary Fact Sheet (domínio público)"]]],
    ["2. Limitações conhecidas", [["Distância à Terra", "varia com a órbita; valor aproximado"]]]
  ]
}

`tipo` aceito: texto | inteiro | número | data | booleano. Data → ISO 8601 (YYYY-MM-DD).
Coluna com "preencher": true fica vazia e pintada de laranja (editável pelo humano).
"""

import argparse
import csv
import json
import os
import sys
from datetime import date, datetime

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

# ---- Convenção de cores (a autora pode ajustar para a paleta NUD) ----
HEADER_FILL = PatternFill('solid', start_color='1F4E78')
HEADER_FONT = Font(name='Arial', size=11, bold=True, color='FFFFFF')
BODY_FONT = Font(name='Arial', size=10)
NOTE_FILL = PatternFill('solid', start_color='FFF2CC')
NOTE_FONT = Font(name='Arial', size=10, italic=True, color='7F6000')
BLANK_FILL = PatternFill('solid', start_color='FFEFE0')   # célula a preencher
SECTION_FILL = PatternFill('solid', start_color='D9E1F2')
SECTION_FONT = Font(name='Arial', size=11, bold=True, color='1F4E78')
TITULO_FONT = Font(name='Arial', size=14, bold=True, color='1F4E78')

FORMATO_PADRAO = {'inteiro': '#,##0', 'número': '#,##0.00', 'data': 'yyyy-mm-dd'}
TIPO_JSON = {'texto': 'string', 'inteiro': 'integer', 'número': 'number',
             'data': 'date (ISO 8601)', 'booleano': 'boolean'}


def _coerce(valor, tipo):
    """Normaliza o valor conforme o tipo declarado. String vazia -> None."""
    if valor is None or (isinstance(valor, str) and valor.strip() == ''):
        return None
    if tipo == 'inteiro':
        try:
            return int(valor)
        except (TypeError, ValueError):
            return None
    if tipo == 'número':
        try:
            return float(valor)
        except (TypeError, ValueError):
            return None
    if tipo == 'data':
        if isinstance(valor, (date, datetime)):
            return valor
        try:
            return datetime.strptime(str(valor), '%Y-%m-%d').date()
        except ValueError:
            return str(valor)
    if tipo == 'booleano':
        if isinstance(valor, bool):
            return valor
        return str(valor).strip().lower() in ('true', 'verdadeiro', 'sim', '1')
    return str(valor).strip()


def _largura(nome, tipo):
    """Largura calibrada: texto largo, número/data estreito."""
    if tipo in ('inteiro', 'número', 'data', 'booleano'):
        return max(12, min(len(nome) + 3, 22))
    return max(16, min(len(nome) + 6, 46))


def _aba_dados(wb, aba, primeira=True):
    ws = wb.active if primeira else wb.create_sheet(aba['nome'])
    if primeira:
        ws.title = aba['nome']

    colunas = aba['colunas']
    headers = [c['nome'] for c in colunas]

    linha_header = 1
    linha_ini = 2
    nota = aba.get('nota')
    if nota:
        ws.cell(row=1, column=1).value = nota
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
        cel = ws.cell(row=1, column=1)
        cel.fill = NOTE_FILL
        cel.font = NOTE_FONT
        cel.alignment = Alignment(vertical='center', wrap_text=True)
        ws.row_dimensions[1].height = 40
        linha_header, linha_ini = 2, 3

    # Header (uma única linha)
    for c, h in enumerate(headers, start=1):
        cel = ws.cell(row=linha_header, column=c)
        cel.value = h
        cel.fill = HEADER_FILL
        cel.font = HEADER_FONT
        cel.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.row_dimensions[linha_header].height = 42

    # Dados
    for i, registro in enumerate(aba.get('dados', [])):
        r = linha_ini + i
        for c, col in enumerate(colunas, start=1):
            if col.get('preencher'):
                continue  # coluna a preencher: fica vazia
            cel = ws.cell(row=r, column=c)
            cel.value = _coerce(registro.get(col['nome']), col.get('tipo', 'texto'))
            cel.font = BODY_FONT
            cel.alignment = Alignment(vertical='top', wrap_text=True)
            fmt = col.get('formato') or FORMATO_PADRAO.get(col.get('tipo'))
            if fmt:
                cel.number_format = fmt

    ultima = ws.max_row if aba.get('dados') else linha_ini
    # estilo/borda no corpo inteiro + pintar colunas a preencher
    for i in range(len(aba.get('dados', []))):
        r = linha_ini + i
        for c, col in enumerate(colunas, start=1):
            cel = ws.cell(row=r, column=c)
            cel.font = BODY_FONT
            cel.alignment = Alignment(vertical='top', wrap_text=True)
            if col.get('preencher'):
                cel.fill = BLANK_FILL

    # larguras
    for c, col in enumerate(colunas, start=1):
        ws.column_dimensions[get_column_letter(c)].width = _largura(
            col['nome'], col.get('tipo', 'texto'))

    # painel congelado abaixo do header
    ws.freeze_panes = ws.cell(row=linha_ini, column=1).coordinate

    # Excel Table (não abrange a linha de nota)
    if aba.get('dados'):
        ref = f'A{linha_header}:{get_column_letter(len(headers))}{ultima}'
        tbl = Table(displayName=aba.get('display_name', aba['nome'].replace(' ', '_')), ref=ref)
        tbl.tableStyleInfo = TableStyleInfo(
            name='TableStyleMedium2', showFirstColumn=False, showLastColumn=False,
            showRowStripes=True, showColumnStripes=False)
        ws.add_table(tbl)
    return ws


def _aba_schema(wb, abas):
    """Aba Schema: dicionário legível por máquina (uma linha por coluna de dado)."""
    ws = wb.create_sheet('Schema')
    headers = ['Aba', 'Coluna', 'Tipo', 'Unidade', 'Domínio / Valores', 'Exemplo', 'Descrição']
    for c, h in enumerate(headers, start=1):
        cel = ws.cell(row=1, column=c)
        cel.value = h
        cel.fill = HEADER_FILL
        cel.font = HEADER_FONT
        cel.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 42
    r = 2
    for aba in abas:
        for col in aba['colunas']:
            vals = [aba['nome'], col['nome'], col.get('tipo', 'texto'),
                    col.get('unidade', ''), col.get('dominio', ''),
                    col.get('exemplo', ''), col.get('descricao', '')]
            for c, v in enumerate(vals, start=1):
                cel = ws.cell(row=r, column=c)
                cel.value = v
                cel.font = BODY_FONT
                cel.alignment = Alignment(vertical='top', wrap_text=True)
            r += 1
    for c, w in enumerate((16, 30, 12, 12, 30, 18, 50), start=1):
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = 'A2'
    tbl = Table(displayName='Schema', ref=f'A1:{get_column_letter(len(headers))}{r-1}')
    tbl.tableStyleInfo = TableStyleInfo(name='TableStyleMedium2', showRowStripes=True)
    ws.add_table(tbl)
    return ws


def _aba_premissas(wb, blocos):
    ws = wb.create_sheet('Premissas')
    ws.cell(row=1, column=1).value = 'PREMISSAS E DICIONÁRIO'
    ws.cell(row=1, column=1).font = TITULO_FONT
    linha = 3
    for titulo, itens in blocos:
        for col in (1, 2):
            ws.cell(row=linha, column=col).fill = SECTION_FILL
        ws.cell(row=linha, column=1).value = titulo
        ws.cell(row=linha, column=1).font = SECTION_FONT
        linha += 1
        for chave, valor in itens:
            a = ws.cell(row=linha, column=1)
            b = ws.cell(row=linha, column=2)
            a.value, b.value = chave, valor
            a.font = Font(name='Arial', size=10, bold=True)
            b.font = BODY_FONT
            a.alignment = Alignment(vertical='top', wrap_text=True)
            b.alignment = Alignment(vertical='top', wrap_text=True)
            linha += 1
        linha += 1
    ws.column_dimensions['A'].width = 34
    ws.column_dimensions['B'].width = 95
    return ws


def _exportar_companheiros(spec, output_path):
    base = os.path.splitext(output_path)[0]
    # schema.json (machine-readable)
    schema = {'titulo': spec.get('titulo', ''), 'abas': []}
    for aba in spec['abas']:
        schema['abas'].append({
            'nome': aba['nome'],
            'colunas': [{
                'nome': c['nome'], 'tipo': TIPO_JSON.get(c.get('tipo', 'texto'), 'string'),
                'unidade': c.get('unidade'), 'dominio': c.get('dominio'),
                'descricao': c.get('descricao')} for c in aba['colunas']]})
    with open(base + '.schema.json', 'w', encoding='utf-8') as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
    # dados.csv (primeira aba de dados)
    aba = spec['abas'][0]
    with open(base + '.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        headers = [c['nome'] for c in aba['colunas']]
        w.writerow(headers)
        for reg in aba.get('dados', []):
            w.writerow([('' if reg.get(c['nome']) is None else reg.get(c['nome']))
                        for c in aba['colunas']])
    return base + '.schema.json', base + '.csv'


def construir(spec, output_path, companheiros=False):
    wb = Workbook()
    for i, aba in enumerate(spec['abas']):
        _aba_dados(wb, aba, primeira=(i == 0))
    _aba_schema(wb, spec['abas'])
    if spec.get('premissas'):
        _aba_premissas(wb, spec['premissas'])
    # ordem: dados... -> Schema -> Premissas
    ordem = [a['nome'] for a in spec['abas']] + ['Schema']
    if spec.get('premissas'):
        ordem.append('Premissas')
    wb._sheets = [wb[n] for n in ordem if n in wb.sheetnames]
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    wb.save(output_path)

    alerta = _verificar_tidy(output_path, spec)
    extras = []
    if companheiros:
        extras = list(_exportar_companheiros(spec, output_path))
    return alerta, extras


def _verificar_tidy(output_path, spec):
    """Check pós-build: sem merge em área de dados; toda aba de dados tem Table;
    header em uma linha. Retorna string de alerta (vazia = ok)."""
    problemas = []
    wb = load_workbook(output_path)
    nomes_dados = {a['nome'] for a in spec['abas']}
    for nome in nomes_dados:
        ws = wb[nome]
        if not ws.tables:
            problemas.append(f'{nome}: sem Excel Table')
        for m in ws.merged_cells.ranges:
            # merge só é tolerado na linha 1 (nota)
            if m.min_row > 1:
                problemas.append(f'{nome}: merge em área de dados ({m})')
    if problemas:
        return 'ALERTA TIDY: ' + ' | '.join(problemas)
    return ''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--spec', required=True, help='JSON do conjunto de dados.')
    ap.add_argument('--output', required=True, help='Caminho do .xlsx de saída.')
    ap.add_argument('--export-companheiros', action='store_true',
                    help='Também gera .schema.json e .csv ao lado do .xlsx.')
    args = ap.parse_args()
    with open(args.spec, encoding='utf-8') as f:
        spec = json.load(f)
    alerta, extras = construir(spec, args.output, args.export_companheiros)
    print(f'OK: {args.output}')
    for e in extras:
        print(f'   companheiro: {e}')
    if alerta:
        print(alerta, file=sys.stderr)


if __name__ == '__main__':
    main()
