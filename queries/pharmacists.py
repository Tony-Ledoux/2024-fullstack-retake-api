get_active_pharmacists_query = ("SELECT pharmacist,image,explaination,start_employment "
                                "from hlp.pharmacists WHERE end_employment is NULL;")