# redis 的详细介绍和其他数据的比较
# http://redisinaction.com/preview/chapter1.html



import redis


def log(*args):
    print(*args)


import redis

config = dict(
    host='localhost',
    port=6379,
    db=1,
)

r = redis.Redis(**config)
info = r.info()

log('info', info)

log('get name', r.get('name'))


# string operation
# 设置元素
r.set('name', 'aa')
log(r.get('name'))

# 为c1设置值
r['c1'] = 'bar'
log('set set', r.getset('c1', 'jj'))

# 得到所有包含name的key的值
log('keys:', r.keys('name*'))

# 随机取一个Key值
log('randomkey:', r.randomkey())

# 查看数据是否存在
log('exists', r.exists('name'))

# 删除数据  删除成功返回1
log('delete:', r.delete('name'))
log(r.delete('c1'))

# 更改key的值：
log(r.set('name', 'gina'))
r.rename('name', 'new_name')
log(r.get('new_name'))

# 设置数据过期时间
r.expire('c1', 5)
# 查看过期时间  永不过期返回-1
r.set('name', 'haha')
log(r.ttl('name'))

r.save()
# 取最后一次save时间
log(r.lastsave())
r.set('intv', '9')
log(r.incr('intv'))
log(r.incrby('intv', '5'))

r['c1'] = 'aa'
r['c2'] = 'bb'

# 批量获取数据
log(r.mget('c1', 'c2'))

# 获取开头为c的key的值
log(r.keys('*c*'))

# ---------------------对list集合进行操作---------------------
log(r.lpush('students', 'gina'))
log('list len:', r.llen('students'))
log(r.lrange('students', start=0, end=3))
# 取出一位
log('list index 0:', r.lindex('gina', 0))
# 截取列表
log(r.ltrim('students', start=0, end=3))

# --------------------对set集合进行操作-----------------------
r.sadd('s', 'a')
r.scard('s')
# 判断对象是否存在
log(r.sismember('s', 'a'))
log(r.sinterstore('s1', 's2', 's3'))

# 求并集
r.sunion('s1', 's2')
# 在s1中有，但在s2,s3中没有的数：
r.sdiff('s1', 's2', 's3')
# 取一个随机数
log(r.srandmember('s1'))
