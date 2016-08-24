# 作业 5.1
#
"""
在 routes.py 文件中的 route_message 函数中我们返回了一个 302 响应
写一个函数 redirect , 可以直接 redirect('/') 来得到重定向响应

这是文件中返回 302 的函数
def route_message(request):
    headers = {
        'Content-Type': 'text/html',
        # 'Set-Cookie': 'height=169; gua=1; pwd=2; Path=/',
        # 'Location': ''
    }

    log('本次请求的 method', request.method)
    username = current_user(request)
    log('username', username)
    if username == '游客':
        # 没登录 不让看 重定向到 /
        headers['Location'] = '/'
        header = response_with_headers(headers, 302)
        r = header + '\r\n' + ''
        return r.encode(encoding='utf-8')
        # return redirect('/')
"""


def redirect(location):
    """
    返回一个 302 重定向响应
    """
    pass

# 作业 5.2
#
# 给 User 添加 1 个新属性 note 表示签名
# 做法如下
# 1, 在 注册 页面添加一个新的 input 让用户输入 note
# 2, 在 User 类的初始化中添加一个新的属性 note 并且用 form 里的元素赋值


# 作业 5.3
#
# 添加一个新的路由 /profile (在 routes.py 文件中)
# 如果没登录, 302 重定向到登录界面
# 如果登录了, 则返回一个页面显示用户的三项资料(id, username, note)
