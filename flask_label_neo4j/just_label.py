from flask import render_template, Blueprint, send_from_directory
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request, flash
from werkzeug.utils import secure_filename
import os
from py2neo import Graph, Node, Relationship, NodeMatcher
import py2neo
from docx import Document
import json

just_label = Blueprint('just_label', __name__)  # 蓝图使用方法，参数里给定文件名，还可以给定url前缀
graph = Graph('http://localhost:7474', user='neo4j', password='123456')


@just_label.route('/update_label/<item_id>', methods=['POST', 'GET'])
def update_label(item_id):
    entity_type = graph.run("MATCH (n:label_items)-[r:`包含`]-(m:`实体类别`) where ID(n)=" + item_id + " return m").data()
    relation_type = graph.run("MATCH (n:label_items)-[r:`包含`]-(m:`关系类别`) where ID(n)=" + item_id + " return m").data()
    entity_count = len(list(entity_type))
    relation_count = len(list(relation_type))
    return render_template('update_label.html', item_id=item_id, entity_type=entity_type, relation_type=relation_type, entity_count = entity_count, relation_count = relation_count)


@just_label.route('/update_label_submit/<item_id>', methods=['POST'])
def update_label_submit(item_id):
    entity = str(request.form.getlist('entity')).replace('[', '').replace(']', '').replace('\'', '').split(',')
    relation = str(request.form.getlist('relation')).replace('[', '').replace(']', '').replace('\'', '').split(',')
    entitytype = list(filter(lambda x: x and x.strip(), entity))
    relationtype = list(filter(lambda x: x and x.strip(), relation))
    for entity in entitytype:
        graph.run("match(n:label_items) where ID(n)=" + item_id + " create(n)-[r:包含]->(m:实体类别{name:'" + entity + "'})")
    for relation in relationtype:
        graph.run("match(n:label_items) where ID(n)=" + item_id + " create(n)-[r:包含]->(m:关系类别{name:'" + relation + "'})")
    entity_type = graph.run("MATCH (n:label_items)-[r:`包含`]-(m:`实体类别`) where ID(n)="+item_id+" return m").data()
    relation_type = graph.run("MATCH (n:label_items)-[r:`包含`]-(m:`关系类别`) where ID(n)="+item_id+" return m").data()
    return render_template('update_label.html', item_id=item_id, entity_type=entity_type, relation_type=relation_type, alert="提交成功！")
