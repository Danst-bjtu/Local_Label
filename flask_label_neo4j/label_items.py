from flask import render_template, Blueprint, send_from_directory
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo
from docx import Document

label_items = Blueprint('label_items', __name__)  # 蓝图使用方法，参数里给定文件名，还可以给定url前缀
graph = Graph('http://localhost:7474', user='neo4j', password='123456')
# graph = Graph('bolt://211.71.75.98:7687', user='neo4j', password='zss1234')  #实验室Neo4j数据库连接
UPLOAD_FOLDER = 'upload/'


@label_items.route("/add_item", methods=['POST', 'GET'])
def add_item():
    item_name = request.form['item_name']
    item_describe = request.form['item_describe']
    itemID = graph.run("match(n: user{username: '"+session['username']+"'}) "
    "create(n)-[r: 创建项目]->(m:label_items{name:'"+item_name+"', describe:'"+item_describe+"'}) return ID(m)").data()
    item_id = str(itemID[0]['ID(m)'])
    f = request.files['file']
    list = f.filename.split(".")
    newfilename = item_id + "." + list[1]
    f.save(os.path.join(UPLOAD_FOLDER, secure_filename(newfilename)))
    fileid = graph.run(
        "match(n:label_items) where ID(n)=" + item_id + " create (n)-[r:文件路径]->(m:文本文件{path:'" + os.path.join(
            UPLOAD_FOLDER, secure_filename(newfilename)) + "'}) return ID(m)").data()
    if (list[1] == 'txt'):
        with open(os.path.join(UPLOAD_FOLDER, secure_filename(newfilename)), encoding='utf-8') as f:
            s = f.read().split('。')
            for juzi in s:
                if (juzi != ""):
                    juzi = juzi.replace('\n', '').replace('\r', '')
                    graph.run("match(n:文本文件) where ID(n)=" + str(
                        fileid[0]['ID(m)']) + " create (n)-[r:分句]->(m:单句{content:'" + juzi + "',islabel:'no'})")
    elif (list[1] == 'docx'):
        doc = Document(os.path.join(UPLOAD_FOLDER, secure_filename(newfilename)))
        for para in doc.paragraphs:
            if (str(para.text) != ""):
                text = str(para.text).replace('\n', '').replace('\r', '')
                graph.run("match(n:文本文件) where ID(n)=" + str(
                    fileid[0]['ID(m)']) + " create (n)-[r:分句]->(m:单句{content:'" + text + "',islabel:'no'})")
    f.close()
    label_items = graph.run("match(m: user{username:'" + session[
        'username'] + "'})-[r: 创建项目]->(n:label_items) return ID(n),n").data()
    return render_template('index.html', label_items=label_items, error="添加成功!")


@label_items.route("/reset_date/<item_id>")
def reset_date(item_id):
    graph.run("match (n:label_items)-[r:`文件路径`]->(m),(m)-[rr:`分句`]->(p),(p)-[s:`三元组`]->(q),(q)-[ss]->(k) where ID(n)="+item_id+" set p.islabel='no' detach delete q,k")
    return redirect(url_for('Labelitem'))


@label_items.route("/del_label_item/<item_id>")
def del_label_item(item_id):
    filepath = graph.run("match (n:label_items)-[r:`文件路径`]->(m) where ID(n)=" + item_id + " return m.path").data()
    graph.run("match (n:label_items)-[r:`文件路径`]->(m),(m)-[rr:`分句`]->(p),(p)-[s:`三元组`]->(q),(q)-[ss]->(k) where ID(n)="+item_id+" set p.islabel='no' detach delete q,k")
    graph.run("match (n:label_items)-[b:`包含`]->(c) where ID(n)="+item_id+" detach delete c union match (n:label_items)-[r:`文件路径`]->(m),(m)-[rr:`分句`]->(p) where ID(n)="+item_id+" detach delete p,m,n")
    try:
        os.remove(str(filepath[0]['m.path']))
        return redirect(url_for('Labelitem'))
    except(FileNotFoundError):
        return redirect(url_for('Labelitem'))

