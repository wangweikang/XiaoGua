from flask import Flask, redirect, url_for, jsonify, request

app = Flask(__name__)
users = []
'''
RESTful api

Dr. Fielding
url 用资源来组织的 名词

/GET /players 拿到所有玩家
/GET /player/id 访问id的玩家的数据
/PUT /players 全量更新
/PATCH /players 部分更新
/DELETE /player/id 删除一个玩家
/GET /player/id/level
'''


@app.route("/", methods=["GET"])
def index():
    return'''<form method=post action='/add'>
    <input type=text name=author>
    <button>提交</button>
    </form>
    '''


@app.route("/add", methods=["POST"])
def add():
    form = request.form
    users.append(dict(author=form.get("author", "")))
    return redirect(url_for(".index"))


@app.route("/json")
def json():
    return jsonify(users)


app.run()