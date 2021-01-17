from flask import render_template, Blueprint
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo

user = Blueprint('user', __name__)  # 蓝图使用方法，参数里给定文件名，还可以给定url前缀
graph = Graph('http://localhost:7474', user='neo4j', password='123456')


@user.route('/login')  # 使用user的路由配置
def login():
    return render_template("login.html")


@user.route('/loginProcess', methods=['POST', 'GET'])  # 使用user 的路由配置
def loginProcess():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        usernames = graph.run("match (n:user {username:'" + username + "',password:'" + password + "'}) return count(n)").data()
        if usernames[0]['count(n)'] != 0:
            session['username'] = username
            return redirect(url_for('Labelitem'))
        else:
            error = "账号或密码错误"

    return render_template('login.html', error=error)



@user.route('/logout')
def logout():
    session.pop('username', None)
    return render_template("login.html")

@user.route('/register')  # 使用user的路由配置
def register():
    return render_template("register.html")


@user.route('/registerProcess', methods=['POST', 'GET'])  # 使用user 的路由配置
def registerProcess():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']
        usernames = graph.run("match (n:user {username:'" + username + "'}) return count(n)").data()
        if usernames[0]['count(n)'] == 0:
            graph.run("create (n:user {username:'" + username + "',password:'" + password + "'}) return n")
            return redirect(url_for('login'))
        else:
            error = "该账号已被注册"

    return render_template('register.html', error = error)