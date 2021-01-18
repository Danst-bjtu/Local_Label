from py2neo import Graph,Node,Relationship,NodeMatcher
import py2neo

graph = Graph('http://localhost:7474',user='neo4j',password='123456')
sql = ("MATCH (n:`标注项目`) RETURN ID(n),n")
basesum = graph.run(sql).data()
# print(basesum)
items = {}
for item in basesum:
    print(item['ID(n)'],item['n'])