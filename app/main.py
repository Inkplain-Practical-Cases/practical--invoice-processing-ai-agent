# Why: ASGI composition is the door into the application; business logic belongs in services.
from fastapi import FastAPI
from app.features.invoice_upload.door import router

app = FastAPI(title="Northstar Invoice Processing AI Agent")
app.include_router(router)
