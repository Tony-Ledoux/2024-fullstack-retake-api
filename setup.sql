create database hlp;
use hlp;
create table questions (
	id int unsigned not null primary key auto_increment,
    fname varchar(100) not null,
    email varchar(100) not null,
    about varchar(100) not null,
    question varchar(255) not null,
    received_on datetime not null default current_timestamp,
    awnsered bool not null default 0
);

create table pharmacists (
	id int unsigned not null primary key auto_increment,
    pharmacist varchar(100) not null,
    image varchar(255) default "assets/anonimouspharmacists.png",
    explaination text not null,
    start_employment date not null,
    end_employment date null,
    on_holiday boolean default 0,
    availibilty_flag JSON default ('{"availability":{"morning":["monday","tuesday","wednesday","thursday","friday","saturday"],"afternoon":["monday","tuesday","wednesday","thursday","friday"]}}')
);

DELIMITER ;;
CREATE TRIGGER `pharmacists_start_date` BEFORE INSERT ON `pharmacists` FOR EACH ROW
BEGIN
	if isnull(new.start_employment) then
		set new.start_employment = curdate();
    end if;
END;;
DELIMITER ;



create table calendar (
	calendar_date date primary key,
	day_of_year int,
    quarter_value int,
    weeknumber int,
    day_name varchar(10),
    is_weekend Boolean,
    is_holiday Boolean default 0
);

DELIMITER ;;
CREATE PROCEDURE `Calendar_fill`(IN start_date DATE, IN end_date DATE)
BEGIN
	DECLARE cur_date date;
    DECLARE day_of_year int;
    DECLARE quarter_value int;
    DECLARE weeknumber int;
    declare day_name varchar(10);
    declare is_weekend boolean;
    declare is_holiday boolean;
    declare year_value int;
    declare easter date;
    
    set cur_date = start_date;
    set year_value = year(start_date);
    set easter = BerekenPasen(year_value);
    
    while cur_date <= end_date do
		set day_of_year = dayofyear(cur_date);
        set quarter_value = quarter(cur_date);
        set weeknumber =  week(cur_date,1);
        set day_name = dayname(cur_date);
        set is_weekend = if(day_name in('Saturday','Sunday'),1,0);
        set is_holiday = 0;
		if cur_date in (
			concat(year_value,'-01-01'), -- newyear
            concat(year_value,'-05-01'), -- Labourday
            concat(year_value,'-07-21'), -- national holiday
            concat(year_value,'-08-15'), -- motherday
            concat(year_value,'-11-01'), -- Hollowseve
            concat(year_value,'-11-11'), -- end of WW1
            concat(year_value,'-12-25'), -- christmas
			date_add(easter, interval 1 day),
            date_add(easter, interval 39 day),
            date_add(easter, interval 50 day)
        ) then
			set is_holiday = 1;
        end if;
        insert into calendar(calendar_date,day_of_year,quarter_value,weeknumber,day_name,is_weekend,is_holiday)
        values(cur_date,day_of_year,quarter_value,weeknumber,day_name,is_weekend,is_holiday);
        set cur_date = date_add(cur_date,interval 1 day);
    end while;
    
END;;

CREATE FUNCTION `BerekenPasen`(jaar INT) RETURNS date
    DETERMINISTIC
BEGIN
    DECLARE a INT;
    DECLARE b INT;
    DECLARE c INT;
    DECLARE d INT;
    DECLARE e INT;
    DECLARE f INT;
    DECLARE g INT;
    DECLARE h INT;
    DECLARE i INT;
    DECLARE k INT;
    DECLARE l INT;
    DECLARE m INT;
    DECLARE maand INT;
    DECLARE dag INT;
    DECLARE pasen DATE;
    
    SET a = jaar MOD 19;
    SET b = FLOOR(jaar / 100);
    SET c = jaar MOD 100;
    SET d = FLOOR(b / 4);
    SET e = b MOD 4;
    SET f = FLOOR((b + 8) / 25);
    SET g = FLOOR((b - f + 1) / 3);
    SET h = (19 * a + b - d - g + 15) MOD 30;
    SET i = FLOOR(c / 4);
    SET k = c MOD 4;
    SET l = (32 + 2 * e + 2 * i - h - k) MOD 7;
    SET m = FLOOR((a + 11 * h + 22 * l) / 451);
    SET maand = FLOOR((h + l - 7 * m + 114) / 31);
    SET dag = ((h + l - 7 * m + 114) MOD 31) + 1;
    SET pasen = STR_TO_DATE(CONCAT(jaar, '-', maand, '-', dag), '%Y-%m-%d');
    RETURN pasen;
END;;
DELIMITER ;

create table time_slots (
	id int unsigned not null primary key auto_increment,
    timeslot varchar(30),
    day_part varchar(45)
);

create table apointments (
	date_value date not null,
    pharmacist_id int unsigned not null,
    slot_id int unsigned not null,
    customer varchar(255),
    primary key (date_value,pharmacist_id,slot_id)
);

-- SEED DATA
call Calendar_fill('2024-01-01','2024-12-31');
call Calendar_fill('2025-01-01','2025-12-31');

INSERT INTO `pharmacists` (`pharmacist`, `image`, `explaination`, `start_employment`) 
VALUES 
('Jack Ryan', 'assets/apo1.jpg', 'Jack Ryan is a licensed pharmacist with over 10 years of experience in the field. He is dedicated to providing exceptional care to all patients and is committed to improving health outcomes through personalized service and expert advice. Jack is passionate about helping patients achieve their health goals and is always available to answer questions and provide guidance on medications and wellness.', '2000-05-15'),
('Jason Bourne', 'assets/apo2.jpg', 'Jason Bourne is a dedicated pharmacist with a passion for patient care. He has a strong background in medication management and is committed to providing personalized service to all patients. Jason is known for his friendly demeanor and expert advice, and he is always available to answer questions and address concerns. Patients appreciate his attention to detail and compassionate approach to healthcare.', '2005-10-05'),
('Ethan Hunt', 'assets/apo3.jpg', 'Ethan Hunt is a skilled pharmacist with a focus on patient-centered care. He is dedicated to helping patients achieve optimal health outcomes through personalized service and expert advice. Ethan is known for his attention to detail and commitment to patient safety. He is always available to answer questions and provide guidance on medications and wellness.', '2010-03-20'),
('James Bond', 'assets/apo6.jpg', 'James Bond is a dedicated pharmacist with a passion for patient care. He has a strong background in medication management and is committed to providing personalized service to all patients. James is known for his friendly demeanor and expert advice, and he is always available to answer questions and address concerns. Patients appreciate his attention to detail and compassionate approach to healthcare.', '2015-08-10'),
('Sidney Bristow', 'assets/apo3.jpg', 'Sidney Bristow is a skilled pharmacist with a focus on patient-centered care. She is dedicated to helping patients achieve optimal health outcomes through personalized service and expert advice. Sidney is known for her attention to detail and commitment to patient safety. She is always available to answer questions and provide guidance on medications and wellness.', '2020-12-05'),
('Lana Kane', 'assets/apo4.jpg', 'Lana Kane is a dedicated pharmacist with a passion for patient care. She has a strong background in medication management and is committed to providing personalized service to all patients. Lana is known for her friendly demeanor and expert advice, and she is always available to answer questions and address concerns. Patients appreciate her attention to detail and compassionate approach to healthcare.', '2021-06-30');

INSERT INTO `time_slots` (`timeslot`,`day_part`) VALUES ('9:00 - 9:25','morning'), ('9:30 - 9:55','morning'),('10:00 - 10:25','morning'),('10:30 - 10:55','morning'),('11:00 - 11:25','morning'),
('14:00 - 14:25','afternoon'),('14:30 - 14:55','afternoon'),('15:00 - 15:25','afternoon'),('15:30 - 15:55','afternoon'),('16:00 - 16:25','afternoon'),('16:30 - 16:55','afternoon'),('17:00 -17:25','afternoon');