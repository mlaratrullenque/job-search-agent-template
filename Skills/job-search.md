# Skill: job-search

Search for new jobs and add them to the `possible_jobs` sheet of `job_search.xlsx`. Used by the daily scheduled search or when the candidate asks to look for jobs.

## Project folder
Work on the files in the project folder (the folder that contains `INSTRUCTIONS.md`). If the folder can't be reached, stop and say so: never write results anywhere else.

## 0. Run in parts
So that a problem in a later part never loses the earlier one:
- **Part 1 – LinkedIn:** search, filter, read, score, then IMMEDIATELY append those jobs to `possible_jobs`, save the workbook, and add a log line "Part 1 (LinkedIn): N jobs added (Jxxx–Jyyy)" to `Context/Search_log.md`.
- **Part 2 – company careers pages (section 3b):** only after part 1 is saved. Skip anything already added, append new jobs, save again, and log "Part 2 (careers pages): N jobs added, sites not readable: …".
- **Part 3 – re-check (section 4c).**
- If part 2 or 3 fails or times out, part 1 stays saved; note "Part 2 incomplete" in the log so the next run can redo it.
- Update "Last successful search" after part 1 is saved.

## 1. Load context (every time)
- `INSTRUCTIONS.md` (workflow + "Decisions and rules"; these override this skill if they conflict)
- `Context/About_Me.md`, `Context/Target.md` (incl. "Other search criteria" and "Companies I like")
- `Context/Lessons_learned.md` (rules learned from the candidate's discards; apply them)
- `Context/Search_log.md` (last successful search, careers pages that couldn't be read)
- `job_search.xlsx`: collect every Company + Job title + Link already in `possible_jobs`, `job_tracker` AND `history`, so nothing is proposed twice. If a new posting is a repost of a job in `history`, you may add it but flag "seen before (history)".

## 2. Search window
Postings published since "Last successful search" in the log (if none, the last 30 days). This covers days when the computer was off.

## 3. Where to search
- **Job boards:** LinkedIn Jobs, plus the boards that matter in the candidate's countries (e.g. StepStone, Indeed, Welcome to the Jungle, Jobindex, The Hub, IrishJobs…). Decide the list in the first session.
- **Queries:** the candidate's role types × sectors × places (Target.md, in preference order), plus every company in "Companies I like" by country. Include other cities in the same countries when a job looks like an excellent match. Add queries in the posting languages of each country (e.g. German titles for Germany).
- **Efficient LinkedIn method (tested):** in a browser tab where LinkedIn is open (the candidate signed in), run JavaScript `fetch()` calls from that tab, read-only:
  - search: `/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<k>&location=<country or city>&f_TPR=r2592000&start=0` (`f_TPR=r86400` = last 24 h, `r604800` = last week, `r2592000` = 30 days). Parse cards by splitting on `data-entity-urn="urn:li:jobPosting:` and reading the title (`base-search-card__title`), company (`base-search-card__subtitle`), location (`job-search-card__location`) and `datetime`. Pages come in steps of 10 (`start=0,10,20…`).
  - full posting: `/jobs-guest/jobs/api/jobPosting/<id>` (strip HTML; "No longer accepting applications" = closed).
  - Use full location names when a short one returns nothing (e.g. "Amsterdam, North Holland, Netherlands").
  - **Go slowly:** one request at a time with 0.5–1 s pauses, keep each tool call under ~40 s. LinkedIn rate-limits bursts (empty responses or HTTP 429): slow down and retry, never run parallel workers.
  - Use these only to read. Never click Apply/Save or send anything.
- If the browser isn't available, use web search and the companies' own careers pages.
- **All sites: search and read ONLY.** Never apply, message, connect, follow, like, save or change anything.

## 3b. Careers pages to check directly every run
Small companies often don't post on LinkedIn. Every run, check these pages directly (web fetch first; if it fails, open the page in the browser). Add any relevant new role, with the company's own job link.
- <FILL IN: Company – careers page URL>
- …

Not readable (rely on LinkedIn, try again occasionally): <list>.
When a new company is added to Target.md, find its careers page and add it here.

## 4. Filter: be conservative
When unsure, KEEP the job. Only leave a job out when it clearly:
- is closed or past its deadline (4b)
- is far above the candidate's level (Director/VP/Head of, or clearly many more years than they have)
- requires a language they don't speak at the needed level (or keep it flagged with a low score – see fit-scoring)
- breaks a visa rule in INSTRUCTIONS.md
- matches a discard rule in `Lessons_learned.md`
- is outside their places (Target.md) and not an excellent match

## 4a. Title filters
- Don't drop a title just because it contains a word that sounds wrong ("Engineer", "Senior", "Specialist"): read the posting when unsure. "Senior" roles asking for a few years more than the candidate has can stay (with a capped score).
- Only drop titles that are clearly a different profession or clearly far above their level.

## 4b. ONLY OPEN JOBS
The public LinkedIn job page does NOT reliably show when a job is closed. Check the real status from the signed-in LinkedIn tab, read-only:
`fetch('/voyager/api/jobs/jobPostings/<id>', {headers: {'csrf-token': <JSESSIONID cookie value without quotes>, 'accept': 'application/json'}})` → `jobState`.
- Only `LISTED` = open. `SUSPENDED`, `CLOSED` or anything else = not accepting applications → do NOT add the job.
- Also drop jobs whose page says "No longer accepting applications", or that have no way to apply.
- For jobs from company websites, only add them if the page clearly shows an open position with a way to apply.
- If the status can't be checked, don't add the job; note it in the Search log.

## 4c. Re-check open jobs every run (Part 3)
Re-check with 4b every job in `job_tracker` with Status "Not applied" and every job in `possible_jobs` with no Decision. If one is no longer LISTED: in `job_tracker` set Status "Discarded", Next step "—" and add "Not accepting applications on LinkedIn (checked <date>)" to Notes; in `possible_jobs` set Decision "Discard" and write the same text in "Your notes". If the same role was reposted under a new ID that is LISTED, update the link instead and say so in Notes. Report these changes.

## 5. Score and write
Score each job with `Skills/fit-scoring.md`. Append rows to `possible_jobs` with openpyxl (keep formatting/validation; never change existing rows):
ID (next free J###, unique across both sheets) | Date found | Job title | Company | Location (city, country + remote/hybrid if stated) | Role type (use the candidate's role types from Target.md, or "Other") | Sector | Languages required | Experience required | Deadline | Link (direct posting URL) | Fit score (1-10) | Why this score (one line) | Flags | Decision (empty) | Your notes (empty).
If the file is open or locked, do NOT overwrite it or create a copy: tell the candidate and put the results in your message.

## 5b. Newest first and keeping the sheet intact
After adding jobs, re-sort `possible_jobs`: by Date found (newest first), then by Fit score (highest first). Move whole rows (all columns), keep formatting and validations.
openpyxl does NOT move hyperlinks or conditional formatting with the rows. After every insert/re-sort, before saving:
1. Set every Link cell's hyperlink to its own URL text (`cell.hyperlink = cell.value`).
2. Make sure conditional formatting still covers the whole range with the original rules (`A2:P1000`: `$O2="Discard"` → grey font; colour scale on `L2:L1000`). If rules got split, delete them and re-create them; reset `wb._differential_styles = DifferentialStyleList()` first and re-add the `job_tracker` rules too, so old style ids don't get mixed up. Use 8-digit ARGB colours ("FF808080").
3. Check: no Link with a hyperlink target different from its text; one rule range only.
Same for `job_tracker` (Link column E) after sorting.

## Saving job_search.xlsx safely
- Before the FIRST save in any session, run `python3 Skills/freeze_dates.py`. openpyxl drops Excel's cached values; without this, every "Date applied" stamped by the formula would be re-stamped with a new day.
- After the LAST save, run `python3 Skills/build_analysis.py`: it rebuilds the `analysis` sheet (openpyxl deletes charts when it saves) and freezes dates again.

## 6. Log and report
Update `Context/Search_log.md` (last successful search = today, unreadable careers pages, one run-history line per part). Report: number of jobs added, top 3 with scores, deadlines coming up, anything needing the candidate's attention.
