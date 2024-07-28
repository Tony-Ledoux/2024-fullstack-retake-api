import config
import database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=config.documentation_url)
origins = config.cors_origins.split(",")

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/")
def root():
    return {"message": "hello world"}

@app.get("/test")
def test():
    return {"message": "All is working"}
