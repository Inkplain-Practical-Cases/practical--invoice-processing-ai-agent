# Why: assemble HTTP routers without document parsing logic.
from fastapi import FastAPI
from app.features.invoice_upload.door import router as upload_router
from app.features.invoice_extraction.door import router as parse_router

app = FastAPI(title="Northstar Invoice Processing AI Agent")
app.include_router(upload_router)
app.include_router(parse_router)
