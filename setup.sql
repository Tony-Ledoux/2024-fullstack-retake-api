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
    start_employment date not null default (curdate()) ,
    end_employment date null
);