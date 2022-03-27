DROP SCHEMA IF EXISTS device_management;
CREATE DATABASE device_management;
use device_management;

CREATE TABLE IF NOT EXISTS user (
  id int NOT NULL auto_increment,
  full_name varchar(30) NOT NULL,
  office varchar(30) NOT NULL,
  contact varchar(20) NOT NUll,
  admin_access int NOT NULL DEFAULT 0,
  user_status varchar(20) NOT NULL,
  PRIMARY KEY (id)
);



CREATE TABLE IF NOT EXISTS device(
  id int NOT NULL auto_increment,
  device_name varchar(20) NOT NULL,
  device_type varchar(20) NOT NULL,
  model varchar(30) NOT NUll,
  os_type varchar(30) NOT NULL,
  os_version varchar(255),
  ram varchar(20),
  cpu varchar(20),
  bit int,
  screen_resolution varchar(30),
  grade varchar(20),
  uuid varchar(255),
  device_status varchar(20) NOT NULL,
  PRIMARY KEY (id)
 );




CREATE TABLE IF NOT EXISTS assignment (
  id int NOT NULL auto_increment,
  device_id int NOT NULL,
  user_id int NOT NULL,
  borrow_date date NOT NULL,
  due_date date NOT NULL,
  return_date date,
  primary key(id),
  foreign key(device_id) references device(id),
  foreign key(user_id) references user(id)
);


CREATE TABLE IF NOT EXISTS broken_device(
id int NOT NULL auto_increment,
device_id int NOT NULL,
user_id int NOT NULL,
report_date date NOT NULL,
comments varchar(255),
primary key(id),
foreign key(device_id) references device(id),
foreign key(user_id) references user(id)
);

