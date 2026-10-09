# STEP-6: Harden and verify

The final branch adds metadata-only structured logs and end-to-end upload→parse→validate→PostgreSQL→GET tests. It rejects corrupt/image-only PDFs, wrong totals and duplicates. CI must exercise all six cumulative branches and main; STEP-4 onward needs a PostgreSQL service. Run `docker compose up -d postgres && python -m pip install -r requirements.txt && python -m pytest -q`. Stage 3 will separately create the .inkp Simulator.
