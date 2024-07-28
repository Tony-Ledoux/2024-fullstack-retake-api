import json

import config
import database
from queries import questions as queries
from fastapi import FastAPI, HTTPException
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
    query = queries.get_questions
    result = database.execute_sql_query(query)
    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))
    questions_to_return = []
    for question in result:
        q = dict()
        q["id"] = question[0]
        q["name"] = question[1]
        q["email"] = question[2]
        q["subject"] = question[3]
        q["question"] = question[4]
        q["received_at"] = question[5]
        questions_to_return.append(q)
    return {"questions": questions_to_return}
