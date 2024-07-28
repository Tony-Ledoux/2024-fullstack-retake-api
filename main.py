import config
import database
from fastapi import FastAPI

app = FastAPI(docs_url=config.documentation_url)


@app.get("/")
def root():
    return {"message": "hello world"}

@app.get("/test")
def test():
    return {"message": "All is working"}
