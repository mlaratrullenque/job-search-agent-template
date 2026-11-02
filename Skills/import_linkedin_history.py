"""Import the LinkedIn data export (applications + saved jobs) into the 'history' sheet of job_search.xlsx.

Put the CSV files from the LinkedIn export in Context/LinkedIn_export/ ("Job Applications.csv",
"Saved Jobs.csv", "Saved Jobs_1.csv"…), then run from the project folder:
    python3 Skills/import_linkedin_history.py [workbook] [export folder]
Rows already in history (same link + type) are skipped, so it is safe to run again with a newer export.
Only date, company, job title and link are imported – no contact details or answers.
Run freeze_dates.py before and build_analysis.py after, like any other save.
"""
import csv, glob, os, re, sys, datetime
import openpyxl

path = sys.argv[1] if len(sys.argv) > 1 else 'job_search.xlsx'
folder = sys.argv[2] if len(sys.argv) > 2 else os.path.join('Context', 'LinkedIn_export')


def parse_date(s):
    """LinkedIn exports dates like '2/10/25, 3:25 AM' (month/day/year)."""
    s = (s or '').strip()
    for fmt in ('%m/%d/%y, %I:%M %p', '%m/%d/%Y, %I:%M %p', '%m/%d/%y', '%Y-%m-%d'):
        try:
            return datetime.datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def job_id(url):
    m = re.search(r'/jobs/view/(\d+)', url or '')
    return m.group(1) if m else (url or '').strip()


wb = openpyxl.load_workbook(path)
hi = wb['history']
seen = {(r[0], job_id(r[4])) for r in hi.iter_rows(min_row=2, values_only=True) if r[0]}

# jobs already in the workbook → fill "In workbook as"
in_wb = {}
for name in ('possible_jobs', 'job_tracker'):
    ws = wb[name]
    link_col = 11 if name == 'possible_jobs' else 5
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] and r[link_col - 1]:
            in_wb[job_id(r[link_col - 1])] = r[0]

new = []
files = [('Applied', f) for f in glob.glob(os.path.join(folder, 'Job Applications*.csv'))] + \
        [('Saved', f) for f in glob.glob(os.path.join(folder, 'Saved Jobs*.csv'))]
if not files:
    raise SystemExit(f'No LinkedIn CSV files found in {folder}')
for kind, f in files:
    with open(f, encoding='utf-8-sig', newline='') as fh:
        for row in csv.DictReader(fh):
            date = parse_date(row.get('Application Date') or row.get('Saved Date'))
            url = (row.get('Job Url') or '').strip()
            key = (kind, job_id(url))
            if not url or key in seen:
                continue
            seen.add(key)
            new.append((kind, date, (row.get('Company Name') or '').strip(), (row.get('Job Title') or '').strip(),
                        url, in_wb.get(job_id(url), '')))

new.sort(key=lambda x: x[1] or datetime.datetime.min, reverse=True)
r = hi.max_row + 1
while r > 2 and not hi.cell(r - 1, 1).value:
    r -= 1
for row in new:
    for c, v in enumerate(row, 1):
        cell = hi.cell(r, c, v)
        if c == 2 and v:
            cell.number_format = 'DD/MM/YYYY'
        if c == 5 and v:
            cell.hyperlink = v
    r += 1
wb.save(path)
print(f'imported {len(new)} rows into history ({sum(1 for x in new if x[0] == "Applied")} applications, '
      f'{sum(1 for x in new if x[0] == "Saved")} saved jobs)')
