# 作业 6.1
#
"""
增加一个新的路由如下
    '/weibo/edit': login_required(route_weibo_edit)
    '/weibo/update': login_required(route_weibo_update)

功能如下
1, 在 weibo 主页添加一个链接如下 /weibo/edit?id=1
	请参考删除的链接
    它的功能是显示一个页面, 包含了更新微博所用的表单(目前只有 id 和 content 两个内容)
    把包含 id 和 content 的表单数据传给 /weibo/update

2, /weibo/update 接收一个 POST 请求, 并且根据 id 找到存储的 Weibo 数据
    修改后保存并 redirect 到 weibo 主页
"""