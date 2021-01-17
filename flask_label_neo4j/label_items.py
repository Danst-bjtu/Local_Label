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
UPLOAD_FOLDER = 'upload/'


@label_items.route("/add_label_item")
def add_label_item():
    return render_template('add_label_item.html')


@label_items.route("/add_label_item/submit_add_item", methods=['POST', 'GET'])
def submit_add_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_describe = request.form['item_describe']
        graph.run("match(n: user{username: '"+session['username']+"'}) "
        "create(n) - [r: 创建项目]->(m:label_items{name:'"+item_name+"', describe:'"+item_describe+"'}) return n, r, m")
        return redirect(url_for('Labelitem'))


@label_items.route("/del_label_item/<item_id>", methods=['POST', 'GET'])
def del_label_item(item_id):
    graph.run("match (n:label_items) where ID(n)="+ item_id +" DETACH delete n")
    return redirect(url_for('Labelitem'))


@label_items.route("/upload_file/<item_id>")
def upload_file(item_id):
    return render_template('upload_file.html', item_id=item_id)


@label_items.route("/submit_file/<item_id>", methods=['GET', 'POST'])
def submit_file(item_id):
    if request.method == 'POST':
        error = None
        filenum = graph.run("match(n:label_items)-[r:文件路径]->(m:文本文件) where ID(n)="+ item_id +" return count(m)").data()
        if filenum[0]['count(m)'] == 0:
            f = request.files['file']
            list = f.filename.split(".")
            newfilename = item_id+"."+list[1]
            f.save(os.path.join(UPLOAD_FOLDER, secure_filename(newfilename)))
            fileid = graph.run("match(n:label_items) where ID(n)="+item_id+" create (n)-[r:文件路径]->(m:文本文件{path:'"+os.path.join(UPLOAD_FOLDER, secure_filename(newfilename))+"'}) return ID(m)").data()
            if(list[1]=='txt'):
                with open(os.path.join(UPLOAD_FOLDER, secure_filename(newfilename)), encoding='utf-8') as f:
                    s = f.read().split('。')
                    for juzi in s:
                        if(juzi!=""):
                            juzi = juzi.replace('\n', '').replace('\r', '')
                            graph.run("match(n:文本文件) where ID(n)="+str(fileid[0]['ID(m)'])+" create (n)-[r:分句]->(m:单句{content:'"+juzi+"',islabel:'no'})")
            elif(list[1]=='docx'):
                doc = Document(os.path.join(UPLOAD_FOLDER, secure_filename(newfilename)))
                for para in doc.paragraphs:
                    if(str(para.text)!=""):
                        text = str(para.text).replace('\n', '').replace('\r', '')
                        graph.run("match(n:文本文件) where ID(n)="+str(fileid[0]['ID(m)'])+" create (n)-[r:分句]->(m:单句{content:'"+text+"',islabel:'no'})")
            return redirect(url_for('Labelitem'))
        else:
            error = "文本文件已存在，不可重复导入"
            label_items = graph.run("match(m: user{username:'" + session['username'] + "'})-[r: 创建项目]->(n:label_items) return ID(n),n").data()
    return render_template('index.html', label_items=label_items,error=error)