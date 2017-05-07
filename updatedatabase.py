#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector

dbConnection = mysql.connector.connect(host = 'localhost', port = 3306, password = 'admin1', user = 'root', database = 'CSH')

cursor = dbConnection.cursor()
cursor.execute("insert into `teacher` (tid, tname, tsex, tpost) values (%s, %s, %s, %s)",
                (u'102401', u'张建国', u'男', u'副教授'))
cursor.execute("insert into `teacher` (tid, tname, tsex, tpost) values (%s, %s, %s, %s)",
                (u'102405', u'王勇', u'男', u'讲师'))
cursor.execute("insert into `teacher` (tid, tname, tsex, tpost) values (%s, %s, %s, %s)",
                (u'102402', u'郭跃飞', u'男', u'副教授'))
cursor.execute("insert into `teacher` (tid, tname, tsex, tpost) values (%s, %s, %s, %s)",
                (u'102403', u'张守志', u'男', u'副教授'))
cursor.execute("insert into `teacher` (tid, tname, tsex, tpost) values (%s, %s, %s, %s)",
                (u'102404', u'谢锡麟', u'男', u'副教授'))

print 1

cursor.execute("insert into `course` (cid, cname, ccredit) values (%s, %s, %s)", (u'MATH120017.01', u'数学分析BII', u'5.0'))
cursor.execute("insert into `course` (cid, cname, ccredit) values (%s, %s, %s)", (u'MATH120017.02', u'数学分析BII', u'5.0'))
cursor.execute("insert into `course` (cid, cname, ccredit) values (%s, %s, %s)", (u'MATH120017.04', u'数学分析BII', u'5.0'))
cursor.execute("insert into `course` (cid, cname, ccredit) values (%s, %s, %s)", (u'MATH120017.05', u'数学分析BII', u'5.0'))
cursor.execute("insert into `course` (cid, cname, ccredit) values (%s, %s, %s)", (u'MATH120017.08', u'数学分析BII', u'5.0'))

print 2

cursor.execute("insert into `teaching` (tid, cid, year) values (%s, %s, %s)", (u'102405', u'MATH120017.01', u'2015'))
cursor.execute("insert into `teaching` (tid, cid, year) values (%s, %s, %s)", (u'102401', u'MATH120017.02', u'2015'))
cursor.execute("insert into `teaching` (tid, cid, year) values (%s, %s, %s)", (u'102402', u'MATH120017.04', u'2015'))
cursor.execute("insert into `teaching` (tid, cid, year) values (%s, %s, %s)", (u'102403', u'MATH120017.05', u'2015'))
cursor.execute("insert into `teaching` (tid, cid, year) values (%s, %s, %s)", (u'102404', u'MATH120017.08', u'2015'))

cursor.close()
dbConnection.commit()
