CREATE database IF NOT EXISTS python_labs;

USE python_labs;

CREATE TABLE IF NOT EXISTS type_of_robots
	(id int NOT NULL AUTO_INCREMENT,
    type_name varchar(255) NOT NULL,
    PRIMARY KEY(id));
    
CREATE TABLE IF NOT EXISTS robots
	(id int NOT NULL AUTO_INCREMENT,
    robot_name varchar(255) NOT NULL,
    robot_type int NOT NULL,
    PRIMARY KEY(id),
	FOREIGN KEY(robot_type) REFERENCES type_of_robots(id)
    ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS robot_state
  (id int NOT NULL AUTO_INCREMENT,
    robot_id int NOT NULL,
    x int NOT NULL,
    y int NOT NULL,
    step int NOT NULL,
    direction varchar(15),
    PRIMARY KEY(id),
  FOREIGN KEY(robot_id) REFERENCES robots(id)
    ON DELETE CASCADE);