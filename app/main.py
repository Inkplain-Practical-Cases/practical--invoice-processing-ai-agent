# Why: each feature's HTTP door is assembled centrally without business code.
from fastapi import FastAPI
from app.features.invoice_upload.door import router as upload_router
from app.features.invoice_extraction.door import router as parse_router
from app.features.invoice_persistence.door import router as persistence_router
from app.features.invoice_persistence.door_process import router as process_router

app=FastAPI(title="Northstar Invoice Processing AI Agent")
app.include_router(upload_router)
app.include_router(parse_router)
app.include_router(persistence_router)
app.include_router(process_router)
