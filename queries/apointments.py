is_holiday = ("SELECT is_holiday FROM hlp.calendar WHERE calendar_date = %s LIMIT 1;")
pharmacists_per_day = ("SELECT id, pharmacist, JSON_UNQUOTE(JSON_EXTRACT(availibilty_flag,'$.availability.morning')) AS morning_availability, "
                       "JSON_UNQUOTE(JSON_EXTRACT(availibilty_flag,'$.availability.afternoon')) AS afternoon_availability from hlp.pharmacists where ("
                       "JSON_CONTAINS(JSON_EXTRACT(availibilty_flag,'$.availability.morning')," + """'"%s"')""" + " OR "
                       "JSON_CONTAINS(JSON_EXTRACT(availibilty_flag,'$.availability.afternoon')," + """'"%s"')""" +
                       ") AND on_holiday = 0;")

get_appointments_from_date = ("SELECT date_value,(SELECT pharmacist from hlp.pharmacists WHERE pharmacist_id = hlp.pharmacists.id) AS pharmacist,"
                            "timeslot,day_part,customer "
                            "FROM hlp.apointments "
                            "JOIN hlp.time_slots on slot_id = hlp.time_slots.id "
                            "WHERE date_value >= %s order by date_value,pharmacist_id ASC, day_part DESC")

get_time_slots = "SELECT * FROM hlp.time_slots"

post_appointment = "INSERT INTO hlp.apointments (`date_value`,`pharmacist_id`,`slot_id`,`customer`) VALUES (%s, %s, %s, %s)"

get_available_slots ="""
WITH AvailablePharmacists AS (
    SELECT id, pharmacist, JSON_CONTAINS(availibilty_flag, JSON_QUOTE('%(day)s'), CONCAT('$.availability.morning')) as available_morning, 
    JSON_CONTAINS(availibilty_flag, JSON_QUOTE('%(day)s'), CONCAT('$.availability.afternoon')) as available_afternoon
    FROM hlp.pharmacists
    WHERE (start_employment <= '%(date)s' AND (end_employment IS NULL OR end_employment >= '%(date)s'))
      AND on_holiday = 0
), booked_slots as (
	SELECT * from hlp.apointments where date_value = '%(date)s' and pharmacist_id in (select id from AvailablePharmacists))

SELECT
	p.id as pharmacist_id,
    p.pharmacist,
    ts.id as slot_id,
    ts.timeslot,
    ts.day_part
from hlp.time_slots ts join AvailablePharmacists p
	ON (ts.day_part = 'morning' and p.available_morning = 1)
    OR (ts.day_part = 'afternoon' and p.available_afternoon = 1)
left join booked_slots bs on p.id = bs.pharmacist_id and ts.id = bs.slot_id where bs.slot_id is null order by p.id, ts.id
"""