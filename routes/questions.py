from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import database
from queries import questions as q_questions
from models import question as model

router = APIRouter()


@router.post("/questions")
def post_question(dm: model.Question):
    query = q_questions.post_questions
    success = database.execute_sql_query(query,(
        dm.name,
        dm.email,
        dm.subject,
        dm.message
    ))
    if success:
        response = jsonable_encoder(dm)
        return JSONResponse(status_code=201, content=response)
    return Response(status_code=500, content="Something went wrong")


@router.get("/questions")
def get_questions(closed: bool = None):
    param = 0
    if closed:
        param = 1
    if closed is None:
        query = q_questions.get_questions
        result = database.execute_sql_query(query)
    else:
        query = q_questions.get_questions_by_status
        result = database.execute_sql_query(query, (param,))
    if isinstance(result, Exception):
        return Response(status_code=500, content=str(result))
    questions_to_return = []
    for question in result:
        q = dict()
        q["id"] = question[0]
        q["from"] = question[1]
        q["mail"] = question[2]
        q["subject"] = question[3]
        q["question"] = question[4]
        q["received"] = question[5]
        if question[6] == 0:
            q["status"] = "unanswered"
        else:
            q["status"] = "answered"
        questions_to_return.append(q)

    return questions_to_return
