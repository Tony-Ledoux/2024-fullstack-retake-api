import json

from fastapi import APIRouter, Response, HTTPException, Request
import database
import queries.pharmacists as q
from models import pharmacists

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


@router.get("/config/pharmacists")
def get_config_pharmacists():
    result = database.execute_sql_query(q.get_config_data)
    if isinstance(result, Exception):
        raise HTTPException(status_code=500, detail=str(result))
    data = []
    for row in result:
        d = {"id": row[0], "name": row[1], "on_holidays": bool(row[2]),
             "available": json.loads(row[3]).get("availability")}
        data.append(d)
    return data


@router.put("/config/pharmacists")
def update_pharmacists_config(model: pharmacists.UpdatePharmacist):
    print(model)
    av = {"availability": {"morning":model.morning, "afternoon": model.afternoon}}
    query = q.update_pharmacists % (model.on_holiday,json.dumps(av),model.pharmacist_id)
    print(query)
    success = database.execute_sql_query(query)
    if not success:
        raise HTTPException(status_code=500, detail={"error": "something went wrong"})
    return {"message": "updated successfully"}
