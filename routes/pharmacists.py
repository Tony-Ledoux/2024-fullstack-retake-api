from fastapi import APIRouter
import database
import queries.pharmacists as q

router = APIRouter()


@router.get("/pharmacists")
def get_pharmacists():
    result = database.execute_sql_query(q)
    return result
