from flask import render_template, Blueprint, send_from_directory
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo
from flask import current_app as app

UPLOAD_FOLDER = 'upload/'
newfilename = 'test.txt'
graph = Graph('http://localhost:7474', user='neo4j', password='123456')
app = Flask(__name__)


@app.route('/')
def index():
    fileid = graph.run("match(n:label_items) where ID(n)=3 create (n)-[r:文件路径]->(m:文本文件{path:'"+os.path.join(UPLOAD_FOLDER, secure_filename(newfilename))+"'}) return ID(m)").data()
    ss = fileid[0]['ID(m)']
    return "mm"+str(ss)
    # path = os.path.join(UPLOAD_FOLDER, secure_filename(newfilename))
    # with open(path, encoding='utf-8') as f:
    #     s = f.read().split('。')
    #for juzi in s:
        #graph.run("match(n:文本文件) where ID(n)="+fileid[0]['ID(m)']+" create (n)-[r:分句]->(m:单句{content:'" + juzi + "',islabel:'no'})")
    # return '完成'+fileid[0]['ID(m)']


if __name__ == '__main__':
    app.run()

