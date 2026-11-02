# Skill: review-decisions

Process the candidate's Pursue/Discard decisions in `job_search.xlsx`. Read `INSTRUCTIONS.md`, `Context/About_Me.md`, `Context/Target.md`, `Context/Lessons_learned.md` first. If `job_search.xlsx` is open or locked, ask the candidate to close it.

## 0. Date applied column (automatic)
In `job_tracker`, "Date applied" (column M) contains a formula that stamps today's date when Status becomes Applied (iterative calculation is enabled). Never overwrite or clear it; only write a real date when the candidate gives one.

## 1. Pursued jobs → job_tracker
For each `possible_jobs` row with Decision = "Pursue" whose ID isn't in `job_tracker` yet:
- Re-read the posting (if it can't be opened, use what is in `possible_jobs` and say so); research the company briefly.
- Append to `job_tracker` (openpyxl; keep formatting; never change other rows):
  ID | Job title | Company | Location | Link | Short description (2–3 sentences: role + company) | Fit score (re-check with fit-scoring; say if it changes) | Strengths (3–4 concrete points from the candidate's real experience) | Risks (gaps, language, seniority, visa, certs in progress – and how to address them) | Deadline | Status "Not applied" | Documents sent (empty) | Date applied: formula `=IF(OR(K{r}="Applied",K{r}="In interviews",K{r}="Offer"),IF(OR(M{r}="",M{r}=0),TODAY(),M{r}),IF(OR(K{r}="Discarded",K{r}="Rejected"),IF(M{r}=0,"",M{r}),""))` | Date contacted (empty) | Days to reply: `=IF(AND(ISNUMBER(N{r}),ISNUMBER(M{r})),N{r}-M{r},"")` | Next step and date ("Apply") | Contact / referral (empty) | Salary range (if published) | Notes ("Found DD/MM/YYYY.").
- Keep the row in `possible_jobs`.

## 1b. job_tracker newest first
After adding rows, re-sort `job_tracker` by job ID number, highest first. Move whole rows (all 19 columns A–S). The M and O formulas refer to their own row: when a row moves, rewrite both formulas for the new row number (real dates typed in M stay as values). Keep formatting, wrap text and validations, and re-set each Link cell's hyperlink to its own URL text afterwards.

## 2. Add pursued companies to the target list
If the company isn't in "Companies I like" in `Context/Target.md` (check name variants), append a row `| <City> | <Company> (added from <job ID>) |`, find its careers page and add it to `Skills/job-search.md` 3b if it is a small company.

## 3. Learn from discards
**Don't be harsh:** a mild note ("not so much into X") becomes a "Score lower" rule (about −2/−3), NOT an exclusion. Exclude only for clear statements ("no", "don't want", "never") or hard limits. When unsure, use "Score lower".
For each Discard with a note: turn the reason into a short general rule (don't over-generalise from one case) and add it to `Context/Lessons_learned.md` with the job ID(s); update similar rules instead of duplicating. A note like "I like the company but…" means: add the company to Target.md even though the job was discarded. Note clear Pursue patterns too. Discards without notes: no rule, but ask if several share a pattern.

## 4. Save and report
Run `freeze_dates.py` before the first save and `build_analysis.py` after the last save. Report: jobs moved (one line of strengths/risks each), companies added, new or updated rules, score changes, nearest deadlines. Add a short entry to `LOGBOOK.md`.

## Column reference (job_tracker)
A ID · B Job title · C Company · D Location · E Link · F Short description · G Fit score · H Strengths · I Risks · J Deadline · K Status (Not applied, Applied, In interviews, Offer, Rejected, Discarded) · L Documents sent (e.g. which CV version) · M Date applied (formula) · N Date contacted (the candidate fills it in when a company first replies) · O Days to reply (formula) · P Next step and date · Q Contact / referral · R Salary range · S Notes.
"Rejected" = applied and turned down (Next step "—"); "Discarded" = not applying / job closed.
