# First session – setting up the agent

Agent: go through these steps in order. Don't start a step before the previous one is done. Ask the candidate for information whenever you need it (a few questions at a time, not a long questionnaire). Tick each step (✅ + date) when it is done, and record decisions in `INSTRUCTIONS.md` ("Decisions and rules") and in `LOGBOOK.md`.

## 1. Read and explain
Read `INSTRUCTIONS.md` and every file it points to. Explain the workflow back to the candidate in a few lines and confirm they agree with it.

## 2. Fill in the profile
- Read the CV(s) in `Context/CV/`.
- Fill in `Context/About_Me.md` from the CV, then ask the candidate for what a CV doesn't say: what they are good at, what they enjoy, what they don't want in a job, career direction, languages with levels.
- Show them the result and correct it until they are happy.

## 3. Fill in the target
Ask for and fill in `Context/Target.md`:
- role types they want (and roles they don't want)
- sectors, in order of preference
- places, in order of preference (cities or regions, remote?), and places that are too far
- availability / start date, contract types (permanent, fixed-term, internships, graduate programmes), working mode, salary rules (filter or not)
- visa / work-permit situation
- companies they like (examples, not a limit) – for small companies, find their careers page URL
- anything that is a hard no (companies, sectors, types of work)

## 4. Calibrate the scoring
Show the candidate the factors and weights in `Skills/fit-scoring.md` and adapt them: what matters most to them (skills match, sector, role type, location, likes/dislikes), and the score for each place and sector. Replace the `<FILL IN>` parts of the rubric.

## 5. Create the workbook
- Run `python3 Skills/create_workbook.py` if `job_search.xlsx` doesn't exist yet.
- Optional, only for people who have already been applying: ask whether they applied to or saved jobs on LinkedIn before starting. If so, and they added their LinkedIn data export to `Context/LinkedIn_export/` (LinkedIn → Settings → Data privacy → Get a copy of your data → "Jobs"), run `python3 Skills/import_linkedin_history.py` to fill the `history` sheet, so those jobs are never proposed again. If they don't have it yet, skip this step; it can be done any time later.
- Optional: ask whether they want to fill the `headhunters` sheet (recruitment agencies specialised in their sector and cities).

## 6. Set up the search
- Decide with the candidate where the agent can search: LinkedIn (read-only, in a browser where they are signed in), job boards for their countries, careers pages of the companies in Target.md. Write the list of careers pages to check into `Skills/job-search.md`, section 3b.
- Run a first search covering the last 30 days and let the candidate review the results.
- Then set up the daily scheduled task with the prompt in `Skills/daily-search-prompt.md`.

## 7. First review
After the candidate marks the first jobs Pursue/Discard, follow `Skills/review-decisions.md`. The first rounds of discards teach the most, so ask about patterns if several discards have no notes.

When all steps are done, replace the line at the top of `INSTRUCTIONS.md` that points here, and write the first full entry in `LOGBOOK.md`.
