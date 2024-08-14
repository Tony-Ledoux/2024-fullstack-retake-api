from fastapi import APIRouter, Depends, HTTPException
import datetime
import database
import queries.apointments as queries
from models import appointments
import json
from enum import Enum
from collections import defaultdict

from models.appointments import Appointment

router = APIRouter()


class Weekday(Enum):
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7


def is_date(date: str, date_format: str) -> bool:
    try:
        datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False


def get_date(date: str):
    if is_date(date, "%Y-%m-%d"):
        d = datetime.datetime.strptime(date, "%Y-%m-%d")
        return d.date()
    elif is_date(date, "%d/%m/%Y"):
        d = datetime.datetime.strptime(date, "%d/%m/%Y")
        return d.date()
    else:
        return None


def _is_holiday_database_lookup(holiday: str) -> bool:
    q = queries.is_holiday
    result = database.execute_sql_query(q, (holiday,))
    if isinstance(result, Exception):
        return False
    data = False
    for row in result:
        if row[0] == 1:
            data = True
    return data


def _get_timeslots():
    timeslots_to_return = []
    q = queries.get_time_slots
    result = database.execute_sql_query(q)
    if isinstance(result, Exception):
        return []
    for timeslot in result:
        timeslot = {"id": timeslot[0], "timeslot": timeslot[1], "day_part": timeslot[2]}
        timeslots_to_return.append(timeslot)
    return timeslots_to_return


def _get_pharmacists_for_day(weekday: Weekday):
    q = queries.pharmacists_per_day
    fq = q % (weekday.name, weekday.name)
    result = database.execute_sql_query(fq)
    if isinstance(result, Exception):
        return []
    pharmacists_to_return = []
    for pharmacist in result:
        data = {
            "id": pharmacist[0],
            "name": pharmacist[1],
            "morning_availability": json.loads(pharmacist[2]),
            "afternoon_availability": json.loads(pharmacist[3])
        }
        pharmacists_to_return.append(data)

    return pharmacists_to_return


def _get_made_appointments_for_date(d: datetime.date):
    q = queries.get_appointments_per_day
    result = database.execute_sql_query(q, (str(d),))
    appointments_to_return = []
    if isinstance(result, Exception):
        return []
    for appointment in result:
        a = {"pharmacist_id": appointment[1], "slot_id": appointment[2], "client": appointment[3]}
        appointments_to_return.append(a)
    return appointments_to_return


@router.get("/")
async def get_availability(date: str):
    d = get_date(date)
    if d is None:
        raise HTTPException(status_code=400, detail='{"error": "Invalid date format"}')
    if d.isoweekday() == 7 or _is_holiday_database_lookup(str(d)):
        raise HTTPException(status_code=404, detail='{"error": "We are closed"}')
    params = {"day": Weekday(d.isoweekday()).name, "date": str(d)}
    q = queries.get_available_slots
    # format query with params
    q = q % params
    # this query is to big for the execute method in database doing it manualy
    con = database.connect_to_database()
    pharmacists_dict = defaultdict(lambda: {"pharmacist_id": None, "pharmacist": None, "timeslots": []})
    try:
        with con.cursor(dictionary=True) as cursor:
            cursor.execute(q)
            result = cursor.fetchall()
            for row in result:
                pharmacist_id = row["pharmacist_id"]
                pharmacists_dict[pharmacist_id]["pharmacist_id"] = pharmacist_id
                pharmacists_dict[pharmacist_id]["pharmacist"] = row["pharmacist"]
                timeslot_info = {
                    "slot_id": row["slot_id"],
                    "timeslot": row["timeslot"],
                    "day_part": row["day_part"]
                }
                pharmacists_dict[pharmacist_id]["timeslots"].append(timeslot_info)
        return_list = list(pharmacists_dict.values())
        return return_list
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    finally:
        con.close()


@router.post("/")
def create_appointment(model: Appointment):
    q = queries.post_appointment
    success = database.execute_sql_query(q, (
        model.date_value,
        model.pharmacist_id,
        model.time_slot,
        model.customer
    ))
    if isinstance(success, Exception):
        return HTTPException(status_code=500, detail="Entry could not be added to database")
    return {"message": "Successfully added appointment"}
