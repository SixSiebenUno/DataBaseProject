mysql> create database CSTv1;

mysql> show databases;

mysql> create TABLE Teacher ( Tid char(5) not null, Tname varchar(20) not null, Tsex char(1) not null, Tpost char(2) not null, primary key(Tid));

mysql> create table Course (Cid char(5) not null, Cname varchar(20) not null, Ccredit real not null, primary key(Cid));

