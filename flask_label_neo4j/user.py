from flask import render_template, Blueprint
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo


user = Blueprint('user', __name__)  # 蓝图使用方法，参数里给定文件名，还可以给定url前缀
graph = Graph('http://localhost:7474', user='neo4j', password='123456')
# graph = Graph('bolt://211.71.75.98:7687', user='neo4j', password='zss1234')  #实验室Neo4j数据库连接


@user.route('/loginProcess', methods=['POST'])  # 使用user 的路由配置
def loginProcess():
    error = None
    username = request.form['log_username']
    password = request.form['log_password']
    usernames = graph.run(
        "match (n:user {username:'" + username + "',password:'" + password + "'}) return count(n)").data()
    if usernames[0]['count(n)'] != 0:
        session['username'] = username
        return redirect(url_for('Labelitem'))
    else:
        error = "用户名或密码错误"
        return render_template('login_register.html', error=error)


@user.route('/logout')
def logout():
    session.pop('username', None)
    return render_template("login_register.html")


@user.route('/registerProcess', methods=['POST'])  # 使用user 的路由配置
def registerProcess():
    error = None
    username = request.form['re_username']
    password = request.form['re_password']
    usernames = graph.run("match (n:user {username:'" + username + "'}) return count(n)").data()
    if usernames[0]['count(n)'] == 0:
        graph.run("create (n:user {username:'" + username + "',password:'" + password + "'}) return n")
        return render_template('login_register.html', error='注册成功，请登录')
    else:
        error = "该用户名已被注册"
        return render_template('login_register.html', error=error)
