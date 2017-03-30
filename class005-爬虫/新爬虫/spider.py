import os
import requests
from pyquery import PyQuery as pq

'''
1. 抓包软件
    TCP
        外挂： 1 解包工具 2. 抓包工具
    HTTP
        1. 前后端交互过程
        2. 学习的作用
        3. 模拟网络情况
    fiddler

2
http client server 没有加密
https 证书 非对称加密 抓包： 信任一个证书

3 爬虫
    1. 搜索引擎 query -> page rank
    2. 数据统计

    1. 裸请求 百度 google
    2. 反爬虫策略
    3. js 频繁上新的页面

    组成部分
    1. Downloader 下载页面          requests
    2. HTMLParser 解析页面          pyquery     lxml
    3. DataModel 字段 - element     业务逻辑

    1. 先下载页面，如果没有更新过应该不在下载第二次
    2. 这个拆分可以方便逻辑的扩展
'''

class Model(object):
    """
    基类, 用来显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Movie(Model):
    """
    存储电影信息
    """
    def __init__(self):
        self.name = ''
        self.score = 0
        self.quote = ''
        self.cover_url = ''
        self.ranking = 0


def cached_url(url):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached'
    filename = url.split('=', 1)[-1] + '.html'
    'cached/0.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)

        headers = {
            'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
        }
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(url, headers)
        with open(path, 'wb') as f:
            f.write(r.content)
        return r.content


def movie_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = Movie()
    m.name = e('.title').text()
    m.score = e('.rating_num').text()
    m.quote = e('.inq').text()
    m.cover_url = e('img').attr('src')
    m.ranking = e('.pic').find('em').text()

    return m


def movies_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    '''
    只会下载一次
    '''
    page = cached_url(url)
    '''
    1. 解析 dom
    2. 找到父亲节点
    3. 每个子节点拿一个movie
    '''
    e = pq(page)
    # print(page.decode())
    # 2.父节点
    items = e('.item')
    # 调用 movie_from_div
    # list comprehension
    movies = [movie_from_div(i) for i in items]
    return movies


def download_image(url):
    folder = "img"
    name = url.split("/")[-1]
    path = os.path.join(folder, name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(path):
        return

    headers = {
        'user-agent': '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8''',
    }
    # 发送网络请求, 把结果写入到文件夹中
    r = requests.get(url, headers)
    with open(path, 'wb') as f:
        f.write(r.content)


def main():
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        movies = movies_from_url(url)
        print('top250 movies', movies)
        [download_image(m.cover_url) for m in movies]


if __name__ == '__main__':
    main()
