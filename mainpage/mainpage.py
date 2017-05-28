#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, session, request, redirect, flash, g

import mysql.connector
import json
import hashlib
import time

app = Flask(__name__)
app.secret_key = '123456'

dbConnection = mysql.connector.connect(host = 'localhost', port = 3306, password = 'admin1', user = 'root', database = 'tmp')

gradedict = {"A" : 4.0, "A-" : 3.7, "B+" : 3.3, "B" : 3.0, "B-" : 2.7, "C+": 2.3, "C": 2.0, "C-": 1.7, "D": 1.3, "D-": 1.0, "F": 0.0}

def get_model(table_name, attributes, sql_override=None):
    def func(id):
        if (id == None): return None

        cursor = dbConnection.cursor()
        cursor.execute(sql_override if sql_override is not None else 'select ' + ','.join(
            attributes) + ' from ' + table_name + ' where id=%s',
                       [id])
        result = cursor.fetchall()
        if len(result) == 0:
            return None
        else:
            ret = {}
            for i in range(0, len(attributes)):
                ret[attributes[i]] = result[0][i]

            return ret

    return func

get_user = get_model('user', ['id', 'name', 'password', 'user_type'])

def get_authed_user():
    return get_user(session.get('user_id', None))

@app.before_request
def before_request():
    g.authedUser = get_authed_user()
    g.url_path = request.path





@app.route('/')
def page():
	return render_template('mainpage.html')






@app.route('/auth/login')
def page_login():
    return render_template("auth/login.html")

@app.route('/auth/login', methods = ["POST"])
def page_login_post():
	username = request.form['username']
	password = request.form['password']
	cursor = dbConnection.cursor()
	cursor.execute('select id, password from `user` where name = %s', [username])
	result = cursor.fetchall()
	if len(result) == 0:
		flash(u'找不到该用户', 'error')
		return redirect('/auth/login')
	
	if md5Hash(password) != result[0][1]:
		flash(u'密码错误', 'error')
		return redirect('/auth/login')
	
	session['user_id'] = result[0][0]

	flash(u"欢迎： " + username + u"。 登入成功！", 'success')
	return redirect('/')







@app.route('/auth/register')
def page_register():
	return render_template("auth/register.html")

@app.route('/auth/register', methods = ["GET", "POST"])
def page_register_post():
	if len(request.form['username']) <= 3:
		flash(u'用户名长度太短！', 'error')
		return redirect('/auth/register')
	print request.form
	if request.form['password'] != request.form['password-repeat']:
		flash(u'两次密码不一致', 'error')
		return redirect('/auth/register')
	
	if len(request.form['password']) < 6:
		flash(u'密码长度太短！', 'error')
		return redirect('/auth/register')
	
	cursor = dbConnection.cursor()
	
	cursor.execute('select count(*) from `user` where name = %s', [request.form['username']])
	if cursor.fetchall()[0][0] > 0:
		flash(u'用户名已被注册', 'error')
		return redirect('/auth/register')
	
	cursor = dbConnection.cursor()
	print 'here1'
	cursor.execute('insert into `user` (name, password) values (%s, %s)',
					[request.form['username'], md5Hash(request.form['password'])])
	session['user_id'] = cursor.lastrowid
	print 'here2'
	cursor.close()
	dbConnection.commit()
	flash(u"注册成功！", 'success')

	return redirect('/profile')








@app.route('/profile')
def page_profile():
	
	lista = []
	lista.append({"sid": "   ", "sname": "   ", "ssex": "   ", "sage": "   ", "syear": "   "})
	print lista

	if g.authedUser == None:
		return render_template("profile.html", list = lista)

	id = g.authedUser['id']

	listitem = []

	print id
	cursor = dbConnection.cursor()
	cursor.execute("select count(*) from `student` where id = %s"%(id))

	if cursor.fetchall()[0][0] == 0:
		listitem = lista

	cursor.execute("select * from `student` where id = %s"%(id))

	for (iid, sid, sname, ssex, sage, syear, scredit, sgpa) in cursor.fetchall():
		print iid, sid, sname, ssex, sage, syear, scredit, sgpa
		listitem.append({"sid": sid, "sname": sname, "ssex": ssex, "sage": sage, "syear" : syear})
	
	print listitem
	return render_template('profile.html', list = listitem)


@app.route('/profile', methods = ["GET", "POST"])
def page_profile_post():


	id = g.authedUser['id']
	print id

	cursor = dbConnection.cursor()
	cursor.execute("select count(*) from `student` where id = %s"%(id))

	if cursor.fetchall()[0][0] > 0:
		cursor.execute("delete from `student` where id = %s"%(id))
		cursor.execute("insert into `student` (id, sid, sname, ssex, sage, syear) values (%d, %s, '%s', '%s', %s, %s)"%(id, request.form['sid'], request.form['sname'], request.form['ssex'], request.form['sage'], request.form['syear']))
		flash(u'修改信息成功', 'success')
		cursor.close()
		dbConnection.commit()
		return redirect('/')

	cursor.execute("insert into `student` (id, sid, sname, ssex, sage, syear) values (%d, %s, '%s', '%s', %s, %s)"%(id, request.form['sid'], request.form['sname'], request.form['ssex'], request.form['sage'], request.form['syear']))
	flash(u"完善信息成功", 'success')
	cursor.close()
	dbConnection.commit()
	return redirect('/')





@app.route('/auth/logout')
def page_logout():
	flash(u'登出成功', 'success')
	del session['user_id']
	return redirect('/')






@app.route('/coursepage')
def page_course():
	return render_template("course.html")

@app.route('/coursepage', methods = ['POST'])
def page_course_post():

	cursor = dbConnection.cursor()
	print 'here'
	cursor.execute("select course.cid, cname, ccredit, tname from course, teaching, teacher where course.cid LIKE '%%%s%%' and cname LIKE '%%%s%%' and course.cid = teaching.cid and teaching.tid = teacher.tid"%(request.form['cid'], request.form['cname']))

	listitem = []
	for (cid, cname, ccredit, tname) in cursor.fetchall():
		print cid, cname, ccredit
		listitem.append({"cid": cid, "cname": cname, "ccredit": ccredit, "tname" : tname})
	
	print listitem
	return render_template('course.html', list = listitem)



@app.route('/teacherpage')
def page_teacher():
	return render_template("teacher.html")

@app.route('/teacherpage', methods = ['POST'])
def page_teacher_post():

	cursor = dbConnection.cursor()
	print 'here'
	cursor.execute("select * from teacher where tname LIKE '%%%s%%'"%(request.form['tname']))

	listitem = []
	for (tid, tname, tsex, tpost) in cursor.fetchall():
		print tid, tname, tsex, tpost
		listitem.append({"tid": tid, "tname": tname, "tsex": tsex, "tpost": tpost})
	
	print listitem
	return render_template('teacher.html', list = listitem)






@app.route("/teacheritem/<tid>")
def page_teacher_item(tid):
    
	cursor = dbConnection.cursor()
	post = []
	cursor.execute("select * from teacher where tid = %s"%(tid))
	#print cursor.fetchall()

	for (tid, tname, tsex, tpost) in cursor.fetchall():
		print tid, tname, tsex, tpost
		post.append({"tid": tid, "tname": tname, "tsex": tsex, "tpost": tpost})
	
	print post
	print tid


	cursor.execute("select score, count(*) from courseselecting, teaching where teaching.tid = %s and teaching.cid = courseselecting.cid group by score"%(tid))

	result = []
	for (score, count) in cursor.fetchall():
		print score, count
		result.append({"score": score, "count": count})

	print result

	cursor.execute("select course.cid, cname, ccredit from course, teaching, teacher where course.cid = teaching.cid and teaching.tid = teacher.tid and teacher.tid = %s"%(tid))

	#print cursor.fetchall()
	listitem = []

	for (cid, cname, ccredit) in cursor.fetchall():
		print cid, cname, ccredit, tname, tsex, tpost
		listitem.append({"cid": cid, "cname": cname, "ccredit": ccredit})
	
	print listitem

	return render_template("teacheritem.html", post = post, result = result, list = listitem)


@app.route("/courseitem/<cid>")
def page_course_item(cid):


	cursor = dbConnection.cursor()
	cursor.execute("select * from course where cid = '%s'"%(cid))
	#print cursor.fetchall()

	print 'here'

	post = []

	for (cid, cname, ccredit) in cursor.fetchall():
		print cid, cname, ccredit
		post.append({"cid": cid, "cname": cname, "ccredit": ccredit})
	
	print post

	cursor.execute("select score, count(*) from courseselecting where cid = '%s' group by score"%(cid))
	print cursor.fetchall()

	cursor.execute("select score, count(*) from courseselecting where cid = '%s' group by score"%(cid))

	result = []
	for (score, count) in cursor.fetchall():
		print score, count
		result.append({"score": score, "count": count})
	
	print result

	cursor.execute("select sid, eval, comment from courseselecting where cid = '%s'"%(cid))

	comments = []
	for (sid, score, comment) in cursor.fetchall():
		print sid, score, comment
		comments.append({"sid": sid,"score": score, "comment": comment})
	
	print comments
	
	return render_template("courseitem.html", post = post, result = result, comments = comments)



@app.route("/courseitem/<cid>", methods=["POST"])
def page_course_item_post(cid):
	print 'here'
	print request.form
	if g.authedUser['user_type'] != 1:
		flash(u"没有权限", 'error')
		return redirect('/')
	cursor = dbConnection.cursor()
	cursor.execute("delete from courseselecting where comment = '%s'"%(request.form['delete']))
	print cursor
	cursor.close()
	dbConnection.commit()
	flash(u"删除成功！", 'success')
	return redirect('/courseitem/' + cid)


@app.route('/grade')
def page_grade():
	return render_template("grade.html")

@app.route('/grade', methods = ['POST'])
def page_grade_post():

	cursor = dbConnection.cursor()

	cursor.execute('select count(*) from `student` where id = %s', [g.authedUser['id']])

	if cursor.fetchall()[0][0] == 0:
		print 'here'
		flash(u'您尚未绑定个人信息', 'error')
		return redirect('/profile')

	cursor.execute('select sid from `student` where id = %s', [g.authedUser['id']])
	sid = cursor.fetchall()[0][0]

	cursor = dbConnection.cursor()
	cursor.execute('select count(*) from `course` where cid = %s', [request.form['cid']])
	if cursor.fetchall()[0][0] == 0:
		flash(u'不存在这门课程，请联系管理员添加', 'error')
		return redirect('/grade')

	score = gradedict[request.form['score']]

	cursor.execute('insert into `courseselecting` (sid, cid, score, eval, comment) values (%s, %s, %s, %s, %s)',
				[sid, request.form['cid'], score, request.form['eval'], request.form['comment'] ] )

	flash(u'评价成功', 'success')
	cursor.close()
	dbConnection.commit()
	return redirect('/grade')






def md5Hash(password):
	m = hashlib.md5()
	m.update(password)
	return m.hexdigest()

if __name__ == '__main__':
	app.run(debug = True)
