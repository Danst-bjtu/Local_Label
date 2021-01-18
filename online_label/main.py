from flask import render_template, Blueprint
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo
from user import user
from label_items import label_items

app = Flask(__name__)
app.secret_key = "any random key"
graph = Graph('bolt://211.71.75.98:7687', user='neo4j', password='zss1234')
urls = [user, label_items]  # 用路由构建数组
for url in urls:
    app.register_blueprint(url)  # 将路由均实现蓝图注册到主app应用上


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/Labelitem')
def Labelitem():
    label_items = graph.run("match(m: user{username:'" + session['username'] + "'})-[r: 创建项目]->(n:label_items) return ID(n),n").data()
    return render_template('index.html', label_items=label_items)


if __name__ == '__main__':
    app.run()
