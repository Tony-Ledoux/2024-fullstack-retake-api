get_questions = "SELECT * from hlp.questions;"
get_questions_by_status = "SELECT * from hlp.questions WHERE awnsered = %s;"
post_questions = "INSERT INTO `hlp`.`questions` (`fname`, `email`, `about`, `question`) VALUES (%s, %s, %s, %s);"