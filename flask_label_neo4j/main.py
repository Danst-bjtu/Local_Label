from flask import render_template, Blueprint
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo
from user import user
from label_items import label_items
from just_label import just_label

app = Flask(__name__)
app.secret_key = "any random key"
graph = Graph('http://localhost:7474', user='neo4j', password='123456')
urls = [user, label_items, just_label]  # 用路由构建数组
for url in urls:
    app.register_blueprint(url)  # 将路由均实现蓝图注册到主app应用上


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/Labelitem')
def Labelitem():
    label_items = graph.run("match(m: user{username:'" + session['username'] + "'})-[r: 创建项目]->(n:label_items) return ID(n),n").data()
    return render_template('index.html', label_items=label_items)


@app.route('/just_label/<item_id>')
def just_label(item_id):
    return render_template('just_label.html', item_id=item_id)

if __name__ == '__main__':
    app.run()
