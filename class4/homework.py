# 作业 4.1
#
# 对每一个 Model 添加一个 id 属性, 初始值为 None
# 每一个 Model 的 id 是独一无二并且增长的数字
# save 的时候, 如果 id 属性为 None 就给它赋值并添加/保存
# 如果 id 属性不为 None 就在所有数据中修改并保存
#
# 用法例子如下
"""
# 假设有这个用户
u = User.find_by(username='gua')
u.password = 'pwd'
u.save()
# 直接保存


form = dict(
	username='newgua',
    password='123'
	)
u = User(form)
u.save()
# 因为这是一个新用户, 并没有 id
# 所以 save 的时候被赋予了一个 id
"""


# 作业 4.2
#
# 该看资料中提及的两本书了
# 另外请大致阅读下面这篇文章的内容
http://www.ituring.com.cn/tupubarticle/1204