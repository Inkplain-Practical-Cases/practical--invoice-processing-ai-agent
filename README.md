# Invoice Processing AI Agent

Starter Forward Deployed Engineering practical case: ingest synthetic supplier invoice PDFs via FastAPI, extract text deterministically, parse typed invoice header and line items, validate decimal subtotal/tax/total math, store validated invoices transactionally in PostgreSQL, prevent vendor/invoice-number duplicates, and test malformed files and database error handling. Six cumulative teaching steps with no paid model or real accounting API required.

An Inkplain practical case: a real project built step by step.

## How this repository works

Every step of the lesson has its own branch, and each one contains all steps up to it:

```bash
git clone https://github.com/Inkplain-Practical-Cases/practical--invoice-processing-ai-agent.git
cd practical--invoice-processing-ai-agent
git branch -r            # list the step branches
git checkout step-01-…   # code after step 1
```

`main` holds the final, complete version.
