# ER Relations#

$Students — Course Selecting — Course — Teaching — Teacher$



$Students ( \underline{Student's ID} ; Student's Name ; Student's Sex ; Student's Age ; Time of enrollment ; Student's GPA )$

$Course Selecting ( \underline{Student's ID ; Course's ID ; Semester's ID} ; Score ; Evaluation )$

$Course ( \underline{Course's ID}  ; Course's Name  ; Course's Credit)$

$Teaching(\underline{Course's ID ;Semester's ID; Teacher's ID})$

$Teacher(\underline{Teacher's ID} ; Teacher's Name; Teacher's Sex; Teacher's Post)$



Score — 学生成绩

Evaluation — 学生评价



#### 查询

课程成绩查询 ：  最高成绩 ／ 最低成绩 ／ 平均成绩 ／ 中位成绩

课程评价查询 ：  学生评价 （不同学生段）

老师授课评价 ：  老师所有课程的总评