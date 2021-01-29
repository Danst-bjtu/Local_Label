from flask import render_template, Blueprint, send_from_directory
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo
from docx import Document

just_label = Blueprint('just_label', __name__)  # 蓝图使用方法，参数里给定文件名，还可以给定url前缀
graph = Graph('http://localhost:7474', user='neo4j', password='123456')

@just_label.route('/update_label/<item_id>')
def update_label(item_id):
    return render_template('update_label.html',item_id=item_id)