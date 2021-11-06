from flask import render_template, request, Response, session, jsonify, make_response, redirect, flash, url_for, send_file 
from datetime import datetime, date
from sqlalchemy.orm import subqueryload, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from webapp import app
from webapp import models
from webapp import init_db
from webapp.classes import FormInput
from webapp.init_db import db_session
from webapp.models import User
import os
from sqlalchemy import *
#from werkzeug.utils import secure_filename
from pymysql import *

@app.route('/')
def idx():
    return render_template ("index.html")

@app.route('/mu')
def hellohtml():
    return render_template ("blog-details.html")

@app.route('/chart')
def chart():
    return render_template("blog.html")


@app.route('/method', methods=['GET','POST'])
def method():
    if request.method == 'GET':
        num = request.args["num"]
        name = request.args.get("name")
        return "GET Data({}, {})".format(num, name)
    else:
        num = request.form("num")
        name = request.form["name"]
        return "POST data({},{})".format(num, name)

@app.route('/regist', methods=['GET'])
def regist():
    return render_template("regist.html")

@app.route('/regist', methods=['POST'])
def regist_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    nickname = request.form.get('nickname')
    print(email, passwd, passwd2, nickname)
    

    if passwd != passwd2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("regist.html", email=email, nickname=nickname)
    else:
        #id = 2
        u = User(email, passwd, nickname, True)
        u.passwd = passwd
        u.email = email
        u.nickname = nickname
        print('1')
        try:
            db_session.add(u)
            print('가입됨?')
            db_session.commit()
            print('2')
        except:
            db_session.rollback();
            print('3')
        flash("%s 님, 가입을 환영합니다!" % nickname)
        return redirect("/login")

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')

    u = User.query.filter_by(email=email, passwd=passwd).first()
    if u is not None:
        session['loginUser'] = { 'userid': u.id, 'name': u.nickname }
        if session.get('next'):
            next = session.get('next')
            del session['next']
            return redirect(next)
        return redirect('/')
    else:
        flash("해당 사용자가 없습니다!!")
        return render_template("login.html", email=email)

@app.route('/logout')
def logout():
    if session.get('loginUser'):
        del session['loginUser']

    return redirect('/')
