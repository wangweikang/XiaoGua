"""
2016/11/21

Web 15
服务器的配置


1 准备工作
Windows 下用 bitvise(群里有安装包下载) 来登录并上传文件到服务器(二合一)
(很多人也用 putty, 但不如 bitvise 好, 并且只能登录服务器不能上传文件)

Mac 下直接在终端登录服务器, 不需要安装额外软件
Mac 使用 filezilla(全平台软件) 把代码上传到服务器, 下载地址如下
https://filezilla-project.org/download.php?type=client


2 上传代码
上课讲


3 服务器软件安装
# 给服务器安装连接软件（服务商默认安装好的）
sudo apt-get install openssh-server
# 用 gunicorn 运行服务器程序(理由)
# ====

# 安装好 Ubuntu 后首先要更新服务器软件源, 才能安装软件
sudo apt-get update

# 安装 pip3
sudo apt-get install python3-pip

# 用 pip3 安装 gunicorn
pip3 install gunicorn

# 安装 flask flask-sqlalchemy
sudo pip3 install flask flask-sqlalchemy


# 使用 gunicorn 启动程序
gunicorn main:app -b 0.0.0.0:8000
# -b 用来绑定地址
# main 是主程序名main.py
# app是main中的Flask实例的变量名


# 增加工作进程, 使用 --workders 参数, 4 是工作进程数
# gunicorn --workers 4 main:app -b 0.0.0.0:8000

# 让 gunicorn 在后台持续运行
(gunicorn main:app -b 0.0.0.0:8080 &)



sudo
# nginx 使用（还有 Apache，都是一样流行的服务器软件，
稳定不容易挂）
# ====

有了 gunicorn 为什么要用 nginx(理由)
1， nginx 市场占有率高，发发投入大，安全性高，bug 修复快
2， nginx 可以配置静态文件读取，增加网站访问效率
3， nginx 可以启动多个 gunicorn 实例，并且都绑定在 80 端口

# 安装 nginx
sudo apt-get install nginx

# nginx 常用命令
sudo service nginx restart

# restart 有时候会没效果, 这时候corn就先 stop 再 start
# 或者重启服务器再试试
sudo service nginx stop
sudo service nginx start

简写为下面这句
# service nginx {start|stop|status|restart|reload|configtest}
此处#代表超级用户
$ 不需要管理员权限

nginx 反向代理配置(什么是反向代理)
1，正向代理
2，反向代理
# 正向代理中，proxy和client同属一个LAN，对server透明；
反向代理中，proxy和server同属一个LAN，对client透明。
实际上proxy在两种代理中做的事都是代为收发请求和响应，
 不过从结构上来看正好左右互换了下，所以把后出现的那种代理方式叫成了反向代理。

# 删掉默认网站配置
sudo rm /etc/nginx/sites-enabled/default
# 增加自己的网站, demo 可以是任意你想要的名字
sudo nano /etc/nginx/sites-enabled/demo

# # 开头的行是注释, 注意行尾的分号
# 文件开始, proxy_pass 后面是 gunicorn 的端口
server {
    listen 80;
    location / {
        proxy_pass http://localhost:8000;
    }
}
# 文件结束


静态资源配置(为什么)
server {
    listen 80;
    location /static {
        alias /项目路径/static;
    }
    location / {
        proxy_pass http://localhost:8000;
    }
}

权限问题
路径问题



# 通用 wsgi.py 文件
# (wsgi 是什么)

#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

sys.path.insert(0, abspath(dirname(__file__)))


import app
application = app.configured_app()

"""
建立一个软连接
ln -s /var/www/MyServer2017/conf/bbs.conf /etc/supervisor/conf.d/bbs.conf
ln -s /var/www/MyServer2017/conf/bbs.nginx /etc/nginx/sites-enabled/bbs


➜  ~ cat /etc/supervisor/conf.d/bbs.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c gunicorn.config.py
directory=/var/www/MyServer
autostart=true
autorestart=true


/usr/local/bin/gunicorn wsgi
--bind 0.0.0.0:2001
--pid /tmp/bbs.pid
"""



# 重启服务器的命令可以写成脚本
# (什么是脚本, 怎么写, 有什么用)



# 用 git 管理代码
git 是流行的源代码版本管理软件




# 服务器管理
HHTP服务器
    nginx
    apache

web服务器
    gunicorn

守护进程（监控程序）
    systemd
    supervisor

推荐 gunicorn + nginx + systemd
流行的管理软件是 supervisor, 但是不如 systemd 好用
"""
