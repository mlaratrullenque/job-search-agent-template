# Skill: fit-scoring

Score how well a job fits the candidate (1–10). Read `Context/About_Me.md`, `Context/Target.md` and `Context/Lessons_learned.md` (Lessons learned overrides this rubric if they conflict). Read the full posting before scoring.

The weights and scales below are a starting point: adapt them with the candidate in the first session (`<FILL IN>` parts).

## Weighted factors (each 0–10, then weighted)
| Factor | Weight | Guide |
|---|---|---|
| Skills & experience match | 40% | How well the candidate's experience, skills and level match what the posting asks. <FILL IN: the candidate's key strengths and years of experience; certifications in progress count as in progress, not obtained> |
| Sector | 20% | <FILL IN: e.g. 10 = first-choice sector, 8 = second, 6 = third…> |
| Role type | 15% | <FILL IN: highest = most wanted role types; low = roles they are moving away from> |
| Location | 15% | <FILL IN: score per place in Target.md order, e.g. 10 / 9 / 8 / 7…; other cities in the same countries 5–6; too far 2; elsewhere 3 unless remote-friendly> |
| Likes vs dislikes | 10% | Up for the things in "What I'm good at and want" (About_Me.md); down for "What I don't like". |

Score = weighted average, rounded (minimum 1). Salary is not scored unless Target.md says so.

## Soft preferences
Apply the "Score lower" section of `Lessons_learned.md` after weighting (subtract the stated points, minimum 1) and say so in "Why this score". These jobs are still added.

## Caps
- Requires a language the candidate doesn't speak at the needed level: cap 3, flag it. "Nice to have": no cap, flag.
- Clear seniority mismatch (many more years than they have, Head of/Director): cap 4. Slight stretch: mention only.
- Requires a certification they don't have yet: no cap, flag "cert in progress (<date>)" if they are doing it.
- Must start much earlier than their availability with no flexibility: cap 5, flag.
- Visa not mentioned where they need one: no cap, flag "visa sponsorship not specified".

## Output
Fit score (integer); Why this score (one line, main driver); Flags ("; "-separated). Be consistent; 9–10 only when role type, sector, location AND experience all match.

## Calibration
- Every few days, look at the `analysis` sheet ("Fit score vs your decision"): if the candidate pursues many 5s and discards many 7s, the rubric is off – discuss it with them and adjust the weights or add Lessons learned.
- Earlier rejections by a company never lower the score (only the exact same role already applied to is skipped as a duplicate).
