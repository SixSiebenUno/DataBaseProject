
DROP TABLE IF EXISTS `teaching`;
DROP TABLE IF EXISTS `courseselecting`;
DROP TABLE IF EXISTS `course`;
DROP TABLE IF EXISTS `student`;
DROP TABLE IF EXISTS `teacher`;
DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`name` varchar(255) DEFAULT NULL, #username
	`password` text, #user password
	`user_type` int(255) DEFAULT NULL,
	PRIMARY KEY(`id`)
	) AUTO_INCREMENT = 7 DEFAULT CHARSET = utf8;

CREATE TABLE `student` (
	`id` int (11) NOT NULL, # user.id
	`sid` int (22) NOT NULL, # student ID
	`sname` varchar (255) DEFAULT NULL, # student name
	`ssex` varchar (10) NOT NULL, # student sex
	`sage` int NOT NULL, # student age
	`syear` int NOT NULL, # student year of enrollment
	`scredit` int DEFAULT 0,
	`sgpa` real DEFAULT 0.0,
	PRIMARY KEY(`sid`),
	FOREIGN KEY(`id`) REFERENCES `user`(`id`)
	) DEFAULT CHARSET = utf8;

CREATE TABLE `teacher` (
	`tid` int (6) NOT NULL,
	`tname` varchar(255) DEFAULT NULL,
	`tsex` varchar(11) NOT NULL,
	`tpost` varchar(20), # teacher post : Professor / Lecturer / ...
	PRIMARY KEY(`tid`)
	) DEFAULT CHARSET = utf8;

CREATE TABLE `course` (
	`cid` char (13) NOT NULL,
	`cname` varChar(255) NOT NULL,
	`ccredit` int NOT NULL,
	PRIMARY KEY(`cid`)
	) DEFAULT CHARSET = utf8;

CREATE TABLE `courseselecting` (
	`sid` int (22) NOT NULL,
	`cid` char (13) NOT NULL,
	`score` real DEFAULT 0.0,  # student score 0.0 - 4.0
	`eval` real DEFAULT 0.0,  # student evaluation 0.0 - 100.0
	`comment` text,  # student comment
	PRIMARY KEY(`sid`, `cid`),
	FOREIGN KEY(`sid`) REFERENCES `student`(`sid`),
	FOREIGN KEY(`cid`) REFERENCES `course` (`cid`)
	) DEFAULT CHARSET = utf8;

CREATE TABLE `teaching` (
	`cid` char (13) NOT NULL,
	`tid` int (6) NOT NULL, 
	`year` int NOT NULL,
	PRIMARY KEY(`cid`, `tid`, `year`),
	FOREIGN KEY(`tid`) REFERENCES `teacher`(`tid`),
	FOREIGN KEY(`cid`) REFERENCES `course` (`cid`)
	) DEFAULT CHARSET = utf8;
