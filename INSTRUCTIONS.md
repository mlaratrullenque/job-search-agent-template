# Job search agent – instructions for the AI agent

You are helping **<FILL IN: your name>** with a job search. This file is the entry point: read it at the start of every session, then follow the files it points to.

If any file still contains `<FILL IN: …>` placeholders, start with `FIRST_SESSION.md` before doing anything else.

## Content of the project

1. `Context/` – everything about the candidate
   1. `About_Me.md` – profile, experience, skills, languages, what they like and don't like in a job.
   2. `Target.md` – what they want: roles, sectors, places (in order of preference), other criteria, and the "Companies I like" table.
   3. `CV/` – the CV file(s) (PDF). Same content as About_Me.md.
   4. `Lessons_learned.md` – rules learned from the candidate's Pursue/Discard decisions. **Read before every search and every scoring.**
   5. `Search_log.md` – date of the last successful search and notes on each run.
   6. `LinkedIn_export/` (optional) – the candidate's LinkedIn data export (applications, saved jobs), imported into the `history` sheet.
2. `LOGBOOK.md` – project logbook: what was done each day, decisions, current status and pending items. **Read it at the start of every session and add an entry at the end of each working session.**
3. `Skills/` – the procedures to follow for each task. Always read the relevant one before doing that task:
   - `job-search.md` – find new jobs and add them to `possible_jobs`
   - `fit-scoring.md` – score how well a job fits (1–10)
   - `review-decisions.md` – process the candidate's Pursue/Discard decisions and learn from them
   - `interview-prep.md` – prepare an interview
   - `daily-search-prompt.md` – the prompt for the daily scheduled search
   - Python helpers: `create_workbook.py`, `freeze_dates.py`, `build_analysis.py`, `import_linkedin_history.py`
4. `job_search.xlsx` – one Excel workbook with these sheets:
   1. `possible_jobs` – jobs the agent finds. The candidate reviews them and sets **Decision** to Pursue or Discard, with a note in **Your notes** when discarding (so the agent can learn).
   2. `job_tracker` – jobs marked Pursue, analysed in more depth (description, strengths, risks) with the application status (Not applied, Applied, In interviews, Offer, Rejected, Discarded), date applied, date contacted and days to reply.
   3. `analysis` – statistics and charts with live formulas (funnel, applications per week, fit score vs decisions, countries, role types, jobs found per day, response rate and time). Rebuilt by `Skills/build_analysis.py` after every update.
   4. `networking` – people worth talking to (ID P001…, status, next step).
   5. `headhunters` – recruitment agencies and recruiters (ID H001…).
   6. `history` – LinkedIn applications and saved jobs from the export. Not for review: used so the agent never proposes a job the candidate already saw, and to understand what kind of jobs they are drawn to.

## Methodology

1. The agent searches for interesting jobs (LinkedIn, company careers pages, job boards).
2. The ones that fit the candidate's criteria and experience go into `possible_jobs`, with a fit score.
3. The candidate reviews `possible_jobs` and selects Pursue or Discard, with a short reason when discarding.
4. The agent copies Pursue jobs to `job_tracker`, analyses them in more depth, and turns discard reasons into rules in `Lessons_learned.md`.
5. The candidate applies (always themselves) and keeps Status and "Date contacted" up to date.

## General guidelines

- Be conservative: don't discard a job when unsure – the candidate prefers to see it and discard it themselves.
- Be open-minded but realistic.
- Ask questions whenever information is missing.
- Pay attention to language requirements and the languages the candidate speaks.
- Write the logbook entry at the end of every working session.

## Decisions and rules

These rules override anything in the skills if they conflict. Edit them to your taste in the first session.

- **Search frequency:** a scheduled search runs every day (see `Skills/daily-search-prompt.md`). If a run is missed (e.g. the computer was off), the next run searches everything published since the last successful run, so nothing is lost.
- **Already-seen jobs:** never propose the same job twice, including jobs already discarded, applied to or in `history`. Compare company + title, not only the link (reposts get new IDs).
- **LinkedIn and every other site: search and read ONLY.** Never apply, message, connect, follow, like, save or change anything. Never submit an application anywhere: applying is always done by the candidate.
- **Only open jobs:** never list a job that isn't accepting applications (see `Skills/job-search.md`, section 4b). Re-check undecided and "Not applied" jobs every run.
- **Visa / work permit:** <FILL IN: e.g. "I am an EU citizen; for UK jobs only discard those that explicitly say they do NOT sponsor visas, otherwise flag 'visa sponsorship not specified'">.
- **Excel file:** the workbook may live in a synced folder (OneDrive, Dropbox…). If `job_search.xlsx` is open or locked when the agent needs to write to it, do not overwrite it and do not create a copy: tell the candidate instead.
- **Workbook conventions:** each job gets an ID (J001, J002…) in `possible_jobs` and keeps it in `job_tracker`. When a job is marked Pursue, copy it to `job_tracker` (Status "Not applied") and fill in description, strengths and risks. Dates in DD/MM/YYYY.
- **Newest first:** in `possible_jobs` and `job_tracker` the newest jobs go at the top (`possible_jobs` by Date found, `job_tracker` by job ID, highest first).
- **Date applied (job_tracker, column M):** holds a formula that stamps today's date when Status becomes Applied (iterative calculation is on). Never overwrite or clear that formula; only type a real date when the candidate gives one.
- **Next step (job_tracker):** "Apply" for Not applied jobs; "Wait for answer (follow up if no reply after ~2 weeks)" for Applied jobs.
- **Excel safety:** run `python3 Skills/freeze_dates.py` before the first save of a session and `python3 Skills/build_analysis.py` after the last save (openpyxl drops cached formula results and charts).
- **Messages to recruiters and contacts:** only draft one when the candidate asks for a specific message. Don't draft outreach on your own.
- **Internships and graduate programmes:** <FILL IN: included / not included>.
- <FILL IN: add any other rule you want the agent to follow, one per line>
