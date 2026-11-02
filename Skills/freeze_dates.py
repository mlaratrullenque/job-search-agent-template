"""Run this BEFORE the first save of job_search.xlsx in any session.

The 'Date applied' formula in job_tracker (column M) stamps TODAY() when Status becomes Applied and keeps
that date only through Excel's cached value. openpyxl drops cached values when it saves, so the date would
be re-stamped with a new day. This script writes every cached date as a real value (the formula stays only
on rows that still have no date), then saves.
Usage: python3 Skills/freeze_dates.py [path]
"""
import sys, datetime, openpyxl
from openpyxl.workbook.properties import CalcProperties

path = sys.argv[1] if len(sys.argv) > 1 else 'job_search.xlsx'
wf = openpyxl.load_workbook(path)
wv = openpyxl.load_workbook(path, data_only=True)
t, tv = wf['job_tracker'], wv['job_tracker']
n = 0
for r in range(2, t.max_row + 1):
    m = t.cell(r, 13).value
    if isinstance(m, str) and m.startswith('='):
        v = tv.cell(r, 13).value
        if isinstance(v, (datetime.datetime, datetime.date)):
            t.cell(r, 13).value = v
            t.cell(r, 13).number_format = 'DD/MM/YYYY'
            n += 1
wf.calculation = CalcProperties(calcMode='auto', fullCalcOnLoad=True, iterate=True, iterateCount=1, iterateDelta=0.001)
wf.save(path)
print(f'froze {n} applied dates')
