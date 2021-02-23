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
    return render_template('login_register.html')


@app.route('/Labelitem')
def Labelitem():
    label_items = graph.run("match(m: user{username:'" + session['username'] + "'})-[r: 创建项目]->(n:label_items) return ID(n),n").data()
    return render_template('index.html', label_items=label_items)


@app.route('/just_label/<item_id>')
def just_label(item_id):
    sen_count = graph.run("match(n:label_items)-[r:`文件路径`]->(m),(m)-[s:分句]->(q) where ID(n)="+item_id+" return count(q)").data()
    islabel_count = graph.run("match(n:label_items)-[r:`文件路径`]->(m),(m)-[s:分句]->(q) where ID(n)="+item_id+" and q.islabel='yes' return count(q)").data()
    zhanbi = round(int(islabel_count[0]['count(q)'])*100/int(sen_count[0]['count(q)']), 2)
    relation_type = graph.run("MATCH (n:label_items)-[r:`包含`]-(m:`关系类别`) where ID(n)=" + item_id + " return m").data()
    fenju = graph.run("match(n:label_items)-[r:`文件路径`]->(m),(m)-[s:分句]->(q) where ID(n)="+item_id+" return ID(q),q.content,q.islabel order by ID(q)").data()
    return render_template('just_label.html', item_id=item_id, sen_count=sen_count, islabel_count=islabel_count, zhanbi=zhanbi,fenju=str(fenju),relation_type = relation_type)

if __name__ == '__main__':
    app.run()
