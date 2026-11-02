"""(Re)build the 'analysis' sheet of job_search.xlsx with live formulas + charts.

Run after every update (the daily search runs it at the end). It first freezes the cached 'Date applied'
values (see freeze_dates.py), so it is safe to run at any time.
Usage: python3 Skills/build_analysis.py [path]

Optional settings below: leave them as None to detect them from the data.
"""
import sys, re, datetime, collections, openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.workbook.properties import CalcProperties

# ---- settings
WEEKLY_START = None   # e.g. datetime.date(2026, 9, 28): first Monday of the "applications per week" chart
MAX_COUNTRIES = 8     # countries shown in "Where the jobs are" (detected from the Location column)

path = sys.argv[1] if len(sys.argv) > 1 else 'job_search.xlsx'
wb = openpyxl.load_workbook(path)
wv = openpyxl.load_workbook(path, data_only=True)

# 1) freeze cached Date applied values
t, tv = wb['job_tracker'], wv['job_tracker']
for r in range(2, t.max_row + 1):
    m = t.cell(r, 13).value
    if isinstance(m, str) and m.startswith('='):
        v = tv.cell(r, 13).value
        if isinstance(v, (datetime.datetime, datetime.date)):
            t.cell(r, 13).value = v; t.cell(r, 13).number_format = 'DD/MM/YYYY'

# 2) data needed for labels / ranges (labels only; all numbers are formulas)
pj = wb['possible_jobs']
rows = [r for r in pj.iter_rows(min_row=2, values_only=True) if r[0]]
dates = [r[1].date() if isinstance(r[1], datetime.datetime) else r[1] for r in rows
         if isinstance(r[1], (datetime.datetime, datetime.date))]
today = datetime.date.today()
first_day = min(dates) if dates else today
role_list = [k for k, _ in collections.Counter(r[5] for r in rows if r[5]).most_common()] or ['(no jobs yet)']


def country_of(loc):
    """'Hamburg, Germany (hybrid)' -> 'Germany'."""
    s = re.sub(r'\(.*?\)', '', str(loc or '')).strip(' ,;–-')
    part = s.split(',')[-1].strip() if s else ''
    part = re.split(r'\s[–-]\s', part)[0].strip()
    return part if 2 <= len(part) <= 30 else ''


countries = [c for c, _ in collections.Counter(country_of(r[4]) for r in rows if country_of(r[4])).most_common(MAX_COUNTRIES)]
countries = countries or ['(no jobs yet)']

if 'analysis' in wb.sheetnames:
    del wb['analysis']
ws = wb.create_sheet('analysis', index=wb.sheetnames.index('job_tracker') + 1)

PJ, JT, HI = 'possible_jobs', 'job_tracker', 'history'
P = lambda col: f"{PJ}!${col}$2:${col}$2000"
T = lambda col: f"{JT}!${col}$2:${col}$1000"
H = lambda col: f"{HI}!${col}$2:${col}$2000"

HDR_FILL = PatternFill('solid', fgColor='1F4E79'); HDR_FONT = Font(name='Calibri', bold=True, color='FFFFFF')
SEC_FONT = Font(name='Calibri', bold=True, size=13, color='1F4E79')
NOTE_FONT = Font(name='Calibri', italic=True, color='595959')
for col, w in zip('ABCDEFG', (40, 13, 13, 22, 14, 14, 3)):
    ws.column_dimensions[col].width = w


def header(row, labels, col=1):
    for i, l in enumerate(labels):
        c = ws.cell(row, col + i, l); c.fill = HDR_FILL; c.font = HDR_FONT
        c.alignment = Alignment(horizontal='center', wrap_text=True)


def section(row, text):
    ws.cell(row, 1, text).font = SEC_FONT


def axes_on(chart):
    # recent Excel versions hide openpyxl axes by default: force axis labels visible
    for ax in (chart.x_axis, chart.y_axis):
        ax.delete = False
        ax.tickLblPos = 'nextTo'
        ax.majorTickMark = 'out'


def place(chart, row, title, anchor_col='H', w=17, h=7.5):
    axes_on(chart)
    chart.title = title; chart.width = w; chart.height = h
    ws.add_chart(chart, f'{anchor_col}{row}')


ws['A1'] = 'Job search analysis'; ws['A1'].font = Font(name='Calibri', bold=True, size=16, color='1F4E79')
ws['A2'] = ('Live formulas from possible_jobs, job_tracker and history, rebuilt by Skills/build_analysis.py. '
            'Set Status (Rejected / In interviews / Offer) and fill in "Date contacted" in job_tracker to see response stats.')
ws['A2'].font = NOTE_FONT

# ---- KPIs
section(4, 'Overview')
fd = f'DATE({first_day.year},{first_day.month},{first_day.day})'
kpis = [
    ('Jobs found', f'=COUNTA({P("A")})', '0'),
    ('Pursued', f'=COUNTIF({P("O")},"Pursue")', '0'),
    ('Discarded', f'=COUNTIF({P("O")},"Discard")', '0'),
    ('Waiting for your decision', '=B5-B6-B7', '0'),
    ('Pursue rate (of decided jobs)', '=IFERROR(B6/(B6+B7),0)', '0%'),
    ('Average fit score – pursued', f'=IFERROR(AVERAGEIF({P("O")},"Pursue",{P("L")}),0)', '0.0'),
    ('Average fit score – discarded', f'=IFERROR(AVERAGEIF({P("O")},"Discard",{P("L")}),0)', '0.0'),
    ('Applications in tracker (Applied / Interview / Offer / Rejected)', f'=COUNTIF({T("K")},"Applied")+COUNTIF({T("K")},"In interviews")+COUNTIF({T("K")},"Offer")+COUNTIF({T("K")},"Rejected")', '0'),
    (f'Applications since the agent started ({first_day:%d/%m/%Y})', f'=COUNTIFS({T("M")},">="&{fd})', '0'),
    ('Pursued, still to apply', f'=COUNTIF({T("K")},"Not applied")', '0'),
    ('Responses received (Rejected / Interview / Offer)', f'=COUNTIF({T("K")},"Rejected")+COUNTIF({T("K")},"In interviews")+COUNTIF({T("K")},"Offer")', '0'),
    ('  – rejections', f'=COUNTIF({T("K")},"Rejected")', '0'),
    ('  – interviews', f'=COUNTIF({T("K")},"In interviews")', '0'),
    ('  – offers', f'=COUNTIF({T("K")},"Offer")', '0'),
    ('Response rate (responses / applications)', '=IFERROR(B15/B12,0)', '0%'),
    ('Average days from applying to being contacted', f'=IFERROR(AVERAGE({T("O")}),"no data yet")', '0.0'),
    ('Applied 14+ days ago, not contacted yet (follow up)', f'=COUNTIFS({T("K")},"Applied",{T("M")},"<="&(TODAY()-14),{T("N")},"")', '0'),
]
for i, (lab, f, fmt) in enumerate(kpis):
    r = 5 + i
    ws.cell(r, 1, lab).font = Font(name='Calibri')
    c = ws.cell(r, 2, f); c.number_format = fmt; c.font = Font(name='Calibri', bold=True)
    c.alignment = Alignment(horizontal='right')
last_kpi = 5 + len(kpis) - 1

# funnel table D4:E10
header(4, ['Stage', 'Jobs'], col=4)
for i, (lab, ref) in enumerate([('Found', '=B5'), ('Pursued', '=B6'), ('Applied', '=B12'),
                                ('Responses', '=B15'), ('Interviews', '=B17'), ('Offers', '=B18')]):
    ws.cell(5 + i, 4, lab); ws.cell(5 + i, 5, ref).number_format = '0'
ch = BarChart(); ch.type = 'bar'; ch.style = 10; ch.legend = None
ch.add_data(Reference(ws, min_col=5, min_row=4, max_row=10), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=4, min_row=5, max_row=10)); ch.y_axis.title = 'Jobs'
ch.x_axis.scaling.orientation = 'maxMin'
place(ch, 4, 'Funnel: from found to offer')

# ---- fit score vs decision
r0 = last_kpi + 3
section(r0, 'Fit score vs your decision (is the scoring calibrated?)')
header(r0 + 1, ['Fit score', 'Pursued', 'Discarded', 'Pursue rate'])
for s in range(1, 11):
    r = r0 + 1 + s
    ws.cell(r, 1, s)
    ws.cell(r, 2, f'=COUNTIFS({P("L")},$A{r},{P("O")},"Pursue")')
    ws.cell(r, 3, f'=COUNTIFS({P("L")},$A{r},{P("O")},"Discard")')
    ws.cell(r, 4, f'=IFERROR(B{r}/(B{r}+C{r}),0)').number_format = '0%'
ch = BarChart(); ch.type = 'col'; ch.grouping = 'stacked'; ch.overlap = 100; ch.style = 10
ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=r0 + 1, max_row=r0 + 11), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=1, min_row=r0 + 2, max_row=r0 + 11))
ch.x_axis.title = 'Fit score'; ch.y_axis.title = 'Jobs'
place(ch, r0, 'Your decisions by fit score')

# ---- countries (detected from the Location column)
r1 = r0 + 15
section(r1, 'Where the jobs are')
header(r1 + 1, ['Country', 'Found', 'Pursued', 'Pursue rate'])
for i, name in enumerate(countries):
    r = r1 + 2 + i
    ws.cell(r, 1, name)
    ws.cell(r, 2, f'=COUNTIF({P("E")},"*"&$A{r}&"*")')
    ws.cell(r, 3, f'=COUNTIFS({P("E")},"*"&$A{r}&"*",{P("O")},"Pursue")')
    ws.cell(r, 4, f'=IFERROR(C{r}/B{r},0)').number_format = '0%'
rl = r1 + 1 + len(countries)
ch = BarChart(); ch.type = 'col'; ch.style = 10
ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=r1 + 1, max_row=rl), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=1, min_row=r1 + 2, max_row=rl)); ch.y_axis.title = 'Jobs'
place(ch, r1, 'Jobs found and pursued by country')

# ---- role types
r2 = max(r1 + 15, rl + 3)
section(r2, 'Role types')
header(r2 + 1, ['Role type', 'Found', 'Pursued', 'Pursue rate'])
for i, name in enumerate(role_list):
    r = r2 + 2 + i
    ws.cell(r, 1, name)
    ws.cell(r, 2, f'=COUNTIF({P("F")},$A{r})')
    ws.cell(r, 3, f'=COUNTIFS({P("F")},$A{r},{P("O")},"Pursue")')
    ws.cell(r, 4, f'=IFERROR(C{r}/B{r},0)').number_format = '0%'
rl = r2 + 1 + len(role_list)
ch = BarChart(); ch.type = 'col'; ch.style = 10
ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=r2 + 1, max_row=rl), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=1, min_row=r2 + 2, max_row=rl)); ch.y_axis.title = 'Jobs'
place(ch, r2, 'Jobs found and pursued by role type')

# ---- daily search results
r3 = max(r2 + 15, rl + 3)
section(r3, 'Daily search: jobs found and your pursue rate')
header(r3 + 1, ['Date', 'Found', 'Pursued', 'Discarded', 'Pursue rate (day)', 'Pursue rate (cumulative)'])
days = (today - first_day).days + 1
d0 = r3 + 2
for k in range(days):
    r = d0 + k
    d = first_day + datetime.timedelta(days=k)
    ws.cell(r, 1, datetime.datetime(d.year, d.month, d.day)).number_format = 'DD/MM/YYYY'
    ws.cell(r, 2, f'=COUNTIFS({P("B")},$A{r})')
    ws.cell(r, 3, f'=COUNTIFS({P("B")},$A{r},{P("O")},"Pursue")')
    ws.cell(r, 4, f'=COUNTIFS({P("B")},$A{r},{P("O")},"Discard")')
    ws.cell(r, 5, f'=IFERROR(C{r}/(C{r}+D{r}),0)').number_format = '0%'
    ws.cell(r, 6, f'=IFERROR(SUM(C${d0}:C{r})/(SUM(C${d0}:C{r})+SUM(D${d0}:D{r})),0)').number_format = '0%'
dl = d0 + days - 1
ws.cell(dl + 1, 1, 'The first day usually includes the first 30-day search.').font = NOTE_FONT
ch = BarChart(); ch.type = 'col'; ch.style = 10
ch.add_data(Reference(ws, min_col=2, max_col=3, min_row=r3 + 1, max_row=dl), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=1, min_row=d0, max_row=dl)); ch.y_axis.title = 'Jobs'
ch.x_axis.number_format = 'dd/mm'
place(ch, r3, 'Jobs found and pursued per day')
ch = LineChart(); ch.style = 12
ch.add_data(Reference(ws, min_col=5, max_col=6, min_row=r3 + 1, max_row=dl), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=1, min_row=d0, max_row=dl)); ch.y_axis.number_format = '0%'
ch.y_axis.scaling.min = 0; ch.y_axis.scaling.max = 1; ch.x_axis.number_format = 'dd/mm'
for se in ch.series:
    se.smooth = False
place(ch, r3 + 16, 'Pursue rate over time')

# ---- applications per week
r4 = max(dl + 4, r3 + 33)
start = WEEKLY_START or (first_day - datetime.timedelta(weeks=2))
start = start - datetime.timedelta(days=start.weekday())  # Monday
section(r4, f'Applications per week (since {start:%d/%m/%Y})')
header(r4 + 1, ['Week starting (Mon)', 'Applications', 'Cumulative', 'Week'])
this_monday = today - datetime.timedelta(days=today.weekday())
weeks = max(1, (this_monday - start).days // 7 + 1)
w0 = r4 + 2
for k in range(weeks):
    r = w0 + k
    d = start + datetime.timedelta(weeks=k)
    ws.cell(r, 1, datetime.datetime(d.year, d.month, d.day)).number_format = 'DD/MM/YYYY'
    ws.cell(r, 2, f'=COUNTIFS({T("M")},">="&$A{r},{T("M")},"<"&($A{r}+7))'
                  f'+COUNTIFS({H("A")},"Applied",{H("F")},"",{H("B")},">="&$A{r},{H("B")},"<"&($A{r}+7))')
    ws.cell(r, 3, f'=SUM(B${w0}:B{r})')
    ws.cell(r, 4, f"Week {k + 1} ({d:%d/%m}–{(d + datetime.timedelta(days=6)):%d/%m})")
wl = w0 + weeks - 1
ws.cell(wl + 1, 1, 'Applications with a date in job_tracker + LinkedIn applications in history that are not in the tracker. '
                   'Weeks run Monday–Sunday; the chart is at the top of the sheet.').font = NOTE_FONT
ch = LineChart(); ch.style = 12; ch.legend = None
ch.add_data(Reference(ws, min_col=2, min_row=w0, max_row=wl), titles_from_data=False)
ch.set_categories(Reference(ws, min_col=4, min_row=w0, max_row=wl)); ch.y_axis.title = 'Applications'
ch.x_axis.title = 'Week (Monday–Sunday)'; ch.y_axis.scaling.min = 0
for se in ch.series:
    se.smooth = False; se.marker.symbol = 'circle'; se.marker.size = 7
place(ch, 4, 'Applications per week', anchor_col='R')

for row in ws.iter_rows():
    for c in row:
        if c.font is None or c.font.name != 'Calibri':
            f = c.font; c.font = Font(name='Calibri', bold=f.bold, italic=f.italic, size=f.size, color=f.color)
ws.sheet_view.showGridLines = False
wb.calculation = CalcProperties(calcMode='auto', fullCalcOnLoad=True, iterate=True, iterateCount=1, iterateDelta=0.001)
wb.save(path)
print('analysis rebuilt:', days, 'days,', weeks, 'weeks,', len(countries), 'countries')
