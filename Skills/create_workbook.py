"""Create an empty job_search.xlsx with all sheets, columns, dropdowns and colours.

Usage: python3 Skills/create_workbook.py [path]      (default: job_search.xlsx in the current folder)
Refuses to overwrite an existing workbook. Run it once, from the project folder, in the first session.
Afterwards run Skills/build_analysis.py to add the 'analysis' sheet.
"""
import os, sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule, ColorScaleRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.properties import CalcProperties

path = sys.argv[1] if len(sys.argv) > 1 else 'job_search.xlsx'
if os.path.exists(path):
    raise SystemExit(f'{path} already exists – not overwriting it.')

wb = openpyxl.Workbook()
wb.remove(wb.active)
WRAP = Alignment(wrap_text=True, vertical='top')


def sheet(name, columns, colour, rows, freeze):
    """columns = list of (header, width)."""
    ws = wb.create_sheet(name)
    for i, (h, w) in enumerate(columns, 1):
        c = ws.cell(1, i, h)
        c.font = Font(name='Calibri', bold=True, color='FFFFFFFF')
        c.fill = PatternFill('solid', fgColor=colour)
        c.alignment = Alignment(wrap_text=True, vertical='center')
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w
        for r in range(2, rows + 1):
            ws.cell(r, i).alignment = WRAP
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = freeze
    last = openpyxl.utils.get_column_letter(len(columns))
    ws.auto_filter.ref = f'A1:{last}{rows}'
    return ws


def dropdown(ws, rng, values):
    dv = DataValidation(type='list', formula1='"' + ','.join(values) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)


def score_colours(ws, rng):
    ws.conditional_formatting.add(rng, ColorScaleRule(start_type='num', start_value=1, start_color='FFF8696B',
                                                      mid_type='num', mid_value=5, mid_color='FFFFEB84',
                                                      end_type='num', end_value=10, end_color='FF63BE7B'))


def row_rule(ws, rng, formula, font=None, fill=None):
    dxf = DifferentialStyle(font=Font(color=font) if font else None,
                            fill=PatternFill(bgColor=fill, fill_type='solid') if fill else None)
    ws.conditional_formatting.add(rng, Rule(type='expression', dxf=dxf, formula=[formula]))


# ---- possible_jobs
pj = sheet('possible_jobs', [
    ('ID', 7), ('Date found', 12), ('Job title', 30), ('Company', 20), ('Location', 18), ('Role type', 15),
    ('Sector', 17), ('Languages required', 20), ('Experience required', 36), ('Deadline', 16), ('Link', 30),
    ('Fit score (1-10)', 9), ('Why this score', 40), ('Flags', 39), ('Decision', 12), ('Your notes', 40)],
    'FF1F4E79', 1000, 'C2')
for r in range(2, 1001):
    pj.cell(r, 2).number_format = 'DD/MM/YYYY'
dv = DataValidation(type='whole', operator='between', formula1='1', formula2='10', allow_blank=True)
pj.add_data_validation(dv); dv.add('L2:L1000')
dropdown(pj, 'O2:O1000', ['Pursue', 'Discard'])
row_rule(pj, 'A2:P1000', '$O2="Discard"', font='FF808080')
score_colours(pj, 'L2:L1000')

# ---- job_tracker
jt = sheet('job_tracker', [
    ('ID', 7), ('Job title', 30), ('Company', 20), ('Location', 18), ('Link', 30), ('Short description', 45),
    ('Fit score (1-10)', 9), ('Strengths', 40), ('Risks', 40), ('Deadline', 15), ('Status', 15),
    ('Documents sent', 22), ('Date applied', 13), ('Date contacted', 13), ('Days to reply', 11),
    ('Next step and date', 28), ('Contact / referral', 20), ('Salary range', 15), ('Notes', 40)],
    'FF375623', 999, 'C2')
for r in range(2, 1000):
    jt.cell(r, 13).number_format = 'DD/MM/YYYY'
    jt.cell(r, 14).number_format = 'DD/MM/YYYY'
dropdown(jt, 'K2:K999', ['Not applied', 'Applied', 'In interviews', 'Offer', 'Rejected', 'Discarded'])
row_rule(jt, 'A2:Q999', '$K2="Applied"', fill='FFDDEBF7')
row_rule(jt, 'A2:Q999', '$K2="In interviews"', fill='FFFFF2CC')
row_rule(jt, 'A2:Q999', '$K2="Offer"', fill='FFC6EFCE')
row_rule(jt, 'A2:Q999', '$K2="Discarded"', font='FF808080', fill='FFF2F2F2')
row_rule(jt, 'A2:Q999', '$K2="Rejected"', font='FF808080')
score_colours(jt, 'G2:G999')

# ---- networking
nw = sheet('networking', [
    ('ID', 7), ('Name', 24), ('Current role', 30), ('Company', 24), ('Location', 20), ('LinkedIn / contact', 34),
    ('Why interesting', 40), ('Link to my search (company / J###)', 24), ('Connection', 13), ('Language to use', 13),
    ('Priority', 9), ('Status', 18), ('Date contacted', 13), ('Last interaction', 13), ('Next step and date', 30),
    ('Notes', 45)], 'FF1F4E78', 500, 'C2')
dropdown(nw, 'I2:I500', ['1st', '2nd', '3rd', 'Not connected'])
dropdown(nw, 'K2:K500', ['1', '2', '3'])
dropdown(nw, 'L2:L500', ['To contact', 'Request sent', 'Connected', 'Messaged', 'In conversation',
                         'Call scheduled', 'Call done', 'No reply', 'Not useful'])

# ---- headhunters
hh = sheet('headhunters', [
    ('ID', 7), ('Agency', 30), ('Type', 22), ('Specialisation', 34), ('Cities covered', 28), ('Best for (your roles)', 24),
    ('Level they place', 14), ('Priority', 9), ('Website', 40), ('How to engage', 36),
    ('Contact person(s) (name – focus – LinkedIn)', 50), ('Email / phone', 30), ('Status', 16), ('Date contacted', 14),
    ('Next step', 22), ('Notes', 48)], 'FF1F4E78', 500, 'C2')
dropdown(hh, 'H2:H500', ['1', '2', '3'])
dropdown(hh, 'M2:M500', ['Not contacted', 'Contacted', 'Call scheduled', 'Working with', 'Not useful'])

# ---- history (filled by import_linkedin_history.py)
hi = sheet('history', [('Type', 10), ('Date', 11), ('Company', 25), ('Job title', 55), ('Link', 45),
                       ('In workbook as', 14)], 'FF7F7F7F', 2000, 'A2')

wb.calculation = CalcProperties(calcMode='auto', fullCalcOnLoad=True, iterate=True, iterateCount=1, iterateDelta=0.001)
wb.save(path)
print(f'created {path} – now run: python3 Skills/build_analysis.py')
