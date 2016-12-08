## chat

## 安装需求
> apt-get install redis-server
> pip3 install redis python-redis gunicorn gevent

## 如果执行上述安装报错，尝试下面两项
> apt-get install build-essential
> apt-get install python3-dev

## 开启redis
> redis-server&

## 使用 gunicorn 启动
> gunicorn --worker-class=gevent -t 9999 redischat:app -b 0.0.0.0:3000

## 开启DeBug输出
> gunicorn --log-level debug --worker-class=gevent -t 999 redis_chat81:app

## 把 gunicorn 输出写入到 gunicorn.log 文件中
> gunicorn --log-level debug --access-logfile gunicorn.log --worker-class=gevent -t 999 redis_chat81:app


###################################################################################
由于 gunicorn 会捕捉 flask 的错误输出(比如 500 的异常错误信息)
所以我们无法在 flask 出错的时候(500 错误)看到具体的信息

通过下面的配置, 可以解决这个问题



1, 在初始化 app 后, 执行下面的代码让 flask 把错误扔给 gunicorn
# 设置 log, 否则输出会被 gunicorn 吃掉
if not app.debug:
    import logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)


2, 以这样的方式启动 gunicorn
这个意思是, 把程序的错误输出写入 flask.log.file 文件中
2>&1 是指把错误信息也写入
(gunicorn wsgi -b 0.0.0.0:8000 > flask.log 2>&1 &)


3, 在 flask.log 里面查看程序的错误日志