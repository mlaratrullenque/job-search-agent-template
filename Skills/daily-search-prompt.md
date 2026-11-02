# Daily scheduled search – prompt

Create a scheduled task (once a day, e.g. early morning) that starts your AI agent on the computer where the project folder lives, with access to the project folder, and give it this prompt. Use the scheduling feature of your AI tool if it has one, or a scheduler on your computer (Task Scheduler on Windows, cron/launchd on Mac/Linux) that launches the agent from the command line. Each run starts a fresh session, so the prompt must be self-contained.

---

Run my daily job search. The project folder is <FILL IN: full path to the project folder>.

1. Read INSTRUCTIONS.md, LOGBOOK.md (current status), Skills/job-search.md, Skills/fit-scoring.md, Context/About_Me.md, Context/Target.md, Context/Lessons_learned.md and Context/Search_log.md.
2. Follow Skills/job-search.md exactly, in three parts:
   - Part 1 – LinkedIn: search everything published since "Last successful search" in Context/Search_log.md, read the promising postings, check each one is LISTED, score them, add them to the possible_jobs sheet, save, and log the part.
   - Part 2 – the careers pages listed in Skills/job-search.md section 3b: add new relevant jobs, save, log.
   - Part 3 – re-check that every "Not applied" job in job_tracker and every undecided job in possible_jobs is still open; update the closed ones as the skill says.
3. Run python3 Skills/freeze_dates.py before the first save and python3 Skills/build_analysis.py after the last save.
4. If job_search.xlsx is open or locked, do not overwrite it and do not make a copy: put the results in your final message instead.
5. LinkedIn and every other site: search and read only. Never apply, message, connect, follow, like, save or change anything.
6. Add a short entry for today to LOGBOOK.md and finish with a summary: jobs added (top 3 with scores), jobs closed, deadlines in the next 7 days, anything that needs my attention.
