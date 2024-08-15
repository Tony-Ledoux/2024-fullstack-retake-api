get_active_pharmacists_query = ("SELECT pharmacist,image,explaination,start_employment "
                                "from hlp.pharmacists WHERE end_employment is NULL;")

get_config_data = ("SELECT id,pharmacist,on_holiday, availibilty_flag from hlp.pharmacists "
                   "where end_employment is NULL or end_employment > now() order by id;")

update_pharmacists = ("UPDATE `hlp`.`pharmacists` SET `on_holiday` = %s, `availibilty_flag` = '%s' WHERE `id` =%s")