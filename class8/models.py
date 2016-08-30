import json

from utils import log
import time


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """
    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def load(cls, d):
        """
        从保存的字典中生成对象
        setattr(x, 'y', v) 相当于 x.y = v
        """
        m = cls({})
        for k, v in d.items():
            log('load', k, v)
            setattr(m, k, v)
        return m

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls(m) 可以初始化一个 cls 的实例
        # 不明白就 log 大法看看这些都是啥
        ms = [cls.load(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_all(username='gua')
        """
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        all = cls.all()
        models = []
        if k != '':
            for m in all:
                log('find all', m, k, v)
                if v == m.__dict__[k]:
                    models.append(m)
        return models

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        # log('debug save')
        models = self.all()
        # log('models', models)
        # 如果没有 id，说明是新添加的元素
        if self.id is None:
            # 设置 self.id
            # 先看看是否是空 list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1（当然也可以为 0）
                self.id = 1
            else:
                m = models[-1]
                # log('m', m)
                self.id = m.id + 1
            models.append(self)
        else:
            # index = self.find(self.id)
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            log('debug', index)
            models[index] = self
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def delete(self):
        models = self.all()
        index = -1
        for i, m in enumerate(models):
            # log('debug', self, self.__dict__, m.__dict__)
            if self.id == m.id:
                index = i
                break
        del models[index]
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def json_str(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.note = form.get('note', '')

    def validate_login(self):
        # return self.username == 'gua' and self.password == '123'
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    """
    Message 是用来保存留言的 model
    """
    def __init__(self, form):
        self.id = None
        self.author = form.get('author', '')
        self.message = form.get('message', '')


class Weibo(Model):
    """
    """
    def __init__(self, form):
        # id 是独一无二的一条数据
        # 每个 model 都有自己的 id
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # int(time.time()) 得到一个 unixtime
        # unixtime 是现在通用的时间标准
        # 它表示的是从 1970.1.1 到现在过去的秒数
        # 因为 1970 年是 unix 操作系统创造的时间
        self.created_time = int(time.time())
        # 我们用 user_id 来标识这个微博是谁发的
        # 初始化为 None
        self.user_id = form.get('user_id', None)


class Todo(Model):
    """
    """
    def __init__(self, form):
        # id 是独一无二的一条数据
        # 每个 model 都有自己的 id
        self.id = form.get('id', None)
        self.created_time = int(time.time())
        self.content = form.get('content', '')
        self.complete = False

    def toggleComplete(self):
        self.complete = not self.complete

    def status(self):
        return 'status-done' if self.complete else 'status-active'


def test_weibo():
    weibo_form = {
        'content': '今天天气很好'
    }
    w = Weibo(weibo_form)
    log(w.id, w.content, w.created_time)


def test():
    # users = User.all()
    # u = User.find_by(username='gua')
    # log('users', u)
    # form = dict(
    #     username='gua',
    #     password='gua',
    # )
    # u = User(form)
    # u.save()
    # log('u.id', u.id)
    # u3 = User.find(3)
    # u3.password = '123 789'
    # u3.save()
    # log('u3', u3)
    # log(User.all())
    test_weibo()


if __name__ == '__main__':
    test()
