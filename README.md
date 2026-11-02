# Job Search Agent – template

A ready-to-use folder that turns an AI agent into your personal job-search assistant. It is written in plain Markdown and Python, so it works with any AI assistant that can read and write files on your computer (for example Claude, ChatGPT, Gemini or Copilot agents, Cursor, or similar tools). Every day it searches for jobs that match your profile, scores how well each one fits, and adds them to an Excel workbook. You only decide **Pursue** or **Discard**. The agent moves the jobs you pursue to a tracker, analyses them, and learns from your discards so that each search gets more accurate.

This template was built and tested during a real job search over several weeks. All personal data has been removed: you fill in your own.

> **The agent never applies, messages or changes anything for you.** On LinkedIn and every other site it only searches and reads. Applying is always your job.

---

## How it works

```
 daily search ──► possible_jobs ──► you: Pursue / Discard (+ a short reason)
 (LinkedIn,          (scored 1–10)          │                    │
  careers pages,                            ▼                    ▼
  job boards)                         job_tracker          Lessons_learned.md
                                (strengths, risks,      (rules that make the
                                 status, dates)          next searches better)
                                            │
                                            ▼
                                   analysis sheet (funnel, response
                                   rate, fit score vs your decisions…)
```

1. **Search.** Once a day, the agent searches LinkedIn (read-only, in a browser where you are signed in), the careers pages of the companies you like, and job boards. It only looks at jobs published since the last successful run, so a missed day loses nothing.
2. **Filter and score.** Each job is checked to make sure it is still open. The agent then gives it a fit score from 1 to 10 based on your skills, sector, role type, location and likes/dislikes, with a one-line reason and flags (language, seniority, visa…).
3. **You decide.** In the `possible_jobs` sheet you mark each job Pursue or Discard. When you discard, write a short reason ("too far", "not into sales"…).
4. **The agent learns.** Your reasons become rules in `Lessons_learned.md`. A mild reason lowers the score of similar jobs; a clear "no" excludes them.
5. **Track.** Pursued jobs go to `job_tracker`, with a description, your strengths, the risks and a status (Not applied → Applied → In interviews → Offer / Rejected). The date you applied is filled in automatically when you set the status to Applied.
6. **Analyse.** The `analysis` sheet shows your funnel, applications per week, response rate and time, and whether the fit scores match your decisions.

You can also ask the agent to prepare an interview (`Skills/interview-prep.md`) and keep track of people you contact (`networking` sheet) and recruitment agencies (`headhunters` sheet).

---

## What you need

- **An AI agent with access to a folder on your computer**, so it can read and write the files in this folder and run small Python scripts. Any agent tool that works with local files will do.
- **A browser the agent can use, signed in to LinkedIn** (optional but strongly recommended, because LinkedIn is where most jobs are). Without it, the agent uses web search and careers pages.
- **A way to run the daily search automatically** (optional): the scheduled-task feature of your AI tool, or a scheduler on your computer that starts the agent with the prompt in `Skills/daily-search-prompt.md`. The computer must be on at that time. If a day is missed, the next run catches up. Without automation, just ask the agent to "run the daily search" when you want.
- **Python 3 with `openpyxl`** (`pip install openpyxl`) on the machine where the agent runs the scripts. The agent can install it for you.
- **Excel** (or LibreOffice) to review the workbook.

---

## Folder structure

```
Job-Search-Agent-Template/
├── README.md                  ← this file
├── INSTRUCTIONS.md            ← entry point for the agent: workflow + your rules
├── FIRST_SESSION.md           ← guided setup the agent follows the first time
├── LOGBOOK.md                 ← what happened each day (the agent keeps it)
├── Context/
│   ├── About_Me.md            ← your profile          (fill in)
│   ├── Target.md              ← what/where you want   (fill in)
│   ├── Lessons_learned.md     ← rules learned from your decisions (the agent fills it)
│   ├── Search_log.md          ← last search date + run history   (the agent fills it)
│   ├── CV/                    ← put your CV here (PDF)
│   └── LinkedIn_export/       ← optional: earlier LinkedIn applications (CSV export)
└── Skills/
    ├── job-search.md          ← how to search, filter and add jobs
    ├── fit-scoring.md         ← the 1–10 scoring rubric  (adapt the weights)
    ├── review-decisions.md    ← how to process your Pursue/Discard decisions
    ├── interview-prep.md      ← how to prepare an interview
    ├── daily-search-prompt.md ← prompt to paste into the daily scheduled task
    ├── create_workbook.py     ← creates the empty job_search.xlsx
    ├── build_analysis.py      ← rebuilds the analysis sheet (charts)
    ├── freeze_dates.py        ← protects the automatic "Date applied" dates
    └── import_linkedin_history.py ← optional: imports earlier LinkedIn applications/saved jobs
```

`job_search.xlsx` isn't included; `create_workbook.py` creates it the first time.

---

## Setup (about 30–60 minutes, guided by the agent)

1. **Download this folder** and put it somewhere on your computer (a synced folder like OneDrive or Dropbox is fine).
2. **Put your CV** (PDF) in `Context/CV/`.
3. *Optional – only if you have already been applying:* **import your earlier applications from LinkedIn.** If you applied to or saved jobs on LinkedIn before starting with the agent, download your data (LinkedIn → Settings → Data privacy → *Get a copy of your data* → select *Jobs*; it arrives by email, sometimes after a day). Put `Job Applications.csv` and `Saved Jobs.csv` in `Context/LinkedIn_export/`. The agent imports them into the `history` sheet, so it won't propose jobs you have already applied to or saved. They also give the agent a first idea of what you like, and your earlier applications count in the "applications per week" chart. You can skip this step and do it later at any time.
4. **Open your AI agent, give it access to the folder** and write:

   > Read INSTRUCTIONS.md and let's do the first session (FIRST_SESSION.md).

   The agent will then:
   - read your CV and fill in `About_Me.md`, asking you what the CV doesn't say (what you enjoy, what you don't want, career direction)
   - ask about your targets and fill in `Target.md`: roles, sectors, cities in order of preference, contract types, visa, companies you like
   - adapt the scoring weights in `fit-scoring.md` with you
   - create `job_search.xlsx` (and, if you added it, import your LinkedIn history)
   - run a first search over the last 30 days
5. **Set up the daily search** (optional). Create a scheduled task in your AI tool, or a scheduler on your computer (e.g. every morning), that runs the agent in this folder with the prompt from `Skills/daily-search-prompt.md` (fill in the folder path first).

> **Tip:** many agent tools automatically read an instructions file with a fixed name when they open a folder (for example `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` or `.github/copilot-instructions.md`). If yours does, create that file with one line, "Read INSTRUCTIONS.md and follow it", so every session starts from the right place.

All the places you need to fill in are marked `<FILL IN: …>`. You can also fill them in by hand before the first session.

---

## Daily use

| You | The agent |
|---|---|
| Open `job_search.xlsx`, review the new rows at the top of `possible_jobs`, set **Decision** and write a reason when you discard. **Close the file.** | — |
| Write "*I've reviewed the jobs, process my decisions*" | Moves Pursue jobs to `job_tracker` with description, strengths and risks; adds new rules to `Lessons_learned.md`; adds new companies to `Target.md`. |
| Apply yourself, then set **Status** = Applied (the date fills in automatically). | Next morning: searches again and re-checks that your "Not applied" jobs are still open. |
| When a company replies, set **Status** (Rejected / In interviews / Offer) and **Date contacted**. | Keeps the `analysis` sheet up to date. |
| "*Help me prepare the interview for J012*" | Company brief, likely questions, your best examples, questions to ask. |

Tips:
- **Always close the Excel file** before asking the agent to update it. If it is open, the agent won't overwrite it and will give you the results in the chat instead.
- **Write reasons when you discard.** Even three words help. This is what makes the search better over time.
- **Be specific about how strong a dislike is.** "Not so much into X" lowers the score of similar jobs; "never X" excludes them.
- At the start of each new chat, the agent reads `INSTRUCTIONS.md` and `LOGBOOK.md`, so it knows where you left off.

---

## Customising

- **Your rules:** add them to "Decisions and rules" in `INSTRUCTIONS.md` (e.g. "no consulting firms", "include internships"). They override the skills.
- **Scoring:** change the weights and scales in `Skills/fit-scoring.md`. The "Fit score vs your decision" chart in the `analysis` sheet shows whether the scores match your choices.
- **Careers pages:** list the small companies whose sites the agent should check every day in `Skills/job-search.md`, section 3b.
- **New skills:** add a `.md` file in `Skills/` and mention it in `INSTRUCTIONS.md`.

---

## Good to know


- **Charts disappearing / dates changing:** the Python library that edits the workbook drops charts and cached formula results when it saves. That is why the agent runs `freeze_dates.py` before saving and `build_analysis.py` after saving. If charts are missing, ask the agent to run `build_analysis.py`.
- **Links pointing to the wrong job after sorting:** the skill tells the agent to reset every link after it re-sorts rows. If you see this happen, ask the agent to "re-check the hyperlinks in possible_jobs and job_tracker".
- **Privacy:** `.gitignore` keeps your CV, LinkedIn export, interviews and the workbook out of git. If you keep your own filled-in copy in a repository, make that repository **private**.


