# Invoice Processing AI Agent — STEP 4
All previous PDF/typed financial validation continues to work. Valid invoices are now written transactionally to real PostgreSQL via SQLAlchemy 2.

```bash
docker compose up -d postgres
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```

POST /invoices/process with a supported synthetic text PDF → HTTP 201 plus database ID. GET /invoices/{id} retrieves it with line items. Test fixtures create tables through SQLAlchemy metadata in a clean disposable database; migration SQL shows equivalent DDL. Do not point this demo at a real finance database.
