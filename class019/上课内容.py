"""
Web 19 上课用品
2016/09/19



1, 数据库自动迁移
具体代码在 autoMigrate.py 中

自动迁移需要安装如下两个库
pip3 install flask-migrate flask-script

使用的时候, 初始化数据库用
python autoMigrate.py db init

数据改动后, 使用下面两个命令迁移并且升级数据库
python autoMigrate.py db migrate
python autoMigrate.py db upgrade

可以给迁移加上注释, 就像是 git 一样
db migrate -m "增加了 password 字段"



2, SQLAlchemy 中不同数据间的自动关联
具体的代码在 relationship.py 中



3, SQLAlchemy 中定义多对多的关系
具体的代码在 complicated.py 中



4, SQLAlchemy 关系的其他参数
order_by
指定关系中记录的排序方式

lazy 参数指定加载关系数据的方式
    select 用到了才加载, 默认值
    immediate 立即加载
    dynamic 提供查询让用户自行加载
    noload 永不加载
    还有暂时用不到的两个值 joined 和 subquery, 现在不关心



5, js 的 this 天坑和事件对象和 js 文件引用



6, 模板文件的复用

{% extends "base.html" %}
{% block head %}
  {{ super() }}
  <style type="text/css">
    p {
        background: red;
    }
  </style>
{% endblock %}
{% block title %}主页{% endblock %}
{% block content %}
    <h1>index</h1>
    <p>
        填充模板内容
    </p>
{% endblock %}








<!doctype html>
<html>
  <head>
    <title>
        {% block title %}{% endblock %} - 炼瓜研究所
    </title>
    {% block head %}
        <script>
            console.log('父模板的 log')
        </script>
    {% endblock %}
  </head>
<body>
  <div>{% block content %}{% endblock %}</div>
  <div>
    {% block footer %}
        Copyright 2016 by <a href="/">gua</a>.
    {% endblock %}
  </div>
</body>
</html>

"""