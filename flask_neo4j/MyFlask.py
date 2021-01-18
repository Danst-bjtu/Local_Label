from flask import Flask,render_template,request
from py2neo import Graph,Node,Relationship,NodeMatcher
import py2neo
app = Flask(__name__)


# 写一个函数来处理浏览器发送过来的请求
# @app.route("/")  # 当访问127.0.0.1:5000/的时候执行函数,找/这个路由请求
# def index() :
#     # 负责处理业务
#     return "你好啊，我叫张少帅"
#
# @app.route("/linux")
# def linux() :
#     return "linux教学视频"

# @app.route("/")  # 当访问127.0.0.1:5000/的时候执行函数,找/这个路由请求
# def index() :
#     # 负责处理业务
#     return render_template("hello.html") # 自动去寻找templates里面的hello.html文件

# @app.route("/")  # 当访问127.0.0.1:5000/的时候执行函数,找/这个路由请求
# def index() :
#     # 负责处理业务
#     # 传字符串
#     s = "你好啊，我不叫赛利亚了"
#     # 传列表
#     lst = ["pro14","air14","yoga14s"]
#     return render_template("hello.html",jay=s,lst = lst)  # 自动去寻找templates里面的hello.html文件

# @app.route("/")
# def index() :
#     return render_template("login.html")
#
#
@app.route("/login",methods=['POST'])
def login() :
    # 接受用户名和密码
    # requests = request.args.get("ss") # get方式传参
    username = request.form.get("username")  # post方式传参
    password = request.form.get("pwd")
    if (username == "123" and password == "123") :
        return "登录成功"
    else :
        return render_template("login.html",msg="登录失败")


if __name__ == '__main__' :
    app.run()  # 启动一个Flask项目
