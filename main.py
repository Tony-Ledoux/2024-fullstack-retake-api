import json

import config
import database
from routes import questions as qr
from routes import pharmacists as pr
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=config.documentation_url)
origins = config.cors_origins.split(",")

app.add_middleware(CORSMiddleware,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(qr.router)
app.include_router(pr.router)

