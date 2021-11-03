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
    #print('정보입력 완료' 'email', 'paaswd', 'nickname') "Regist [get] 부분으로 넘어가짐. post??"

    if passwd != passwd2:
        flash("암호를 정확히 입력하세요!!")
        return render_template("regist.html", email=email, nickname=nickname)
    else:
        u = User(email, passwd, nickname, True)
        try:
            db_session.add(u)
            db_session.commit() 

        except:
            db_session.rollback();

        flash("%s 님, 가입을 환영합니다!" % nickname)
        return redirect("/login")

@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST']) # 에러
def login_post():
    email = request.form.get('email')
    passwd = request.form.get('passwd')
    u = User.query.filter('email = :email and passwd = sha2(:passwd, 256)').params(email=email, passwd=passwd).first()
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