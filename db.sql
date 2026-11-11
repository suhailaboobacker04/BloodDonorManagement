create database blood_db_aug_26;
use blood_db_aug_26;
create table Donor(id int Primary key auto_increment,
		name varchar(100),
        blood_group varchar(5),
        phone varchar(15) unique,
        city varchar(100),
        last_donation date 
        


		)