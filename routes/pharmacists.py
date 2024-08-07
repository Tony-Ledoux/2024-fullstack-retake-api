from fastapi import APIRouter, Response
import database
import queries.pharmacists as q

router = APIRouter()


@router.get("/pharmacists")
def get_pharmacists():
    result = database.execute_sql_query(q.get_active_pharmacists_query)
    if isinstance(result, Exception):
        return Response(status_code=500, content={"error": "Database error"})
    pharmacists_to_return = []
    for pharmacist in result:
        data = {
            "name": pharmacist[0],
            "image": pharmacist[1],
            "description": pharmacist[2],
            "start_date": pharmacist[3].strftime("%d-%m-%Y")

        }
        pharmacists_to_return.append(data)
    return pharmacists_to_return
