import os
from selenium import webdriver
from pyquery import PyQuery as pq
driver = webdriver.PhantomJS()

'''
组成部分
    1. Downloader 下载页面          浏览器  PhantomJS
    2. HTMLParser 解析页面          pyquery     lxml
    3. DataModel 字段 - element     业务逻辑
'''

'''
编码
00011110001111 32bit
127

1. 二进制表示
2. 字符串表示

字符 -> 二进制

ascii english number roma
unicode
    utf-8   1, 2, 3, 4
    utf-16  2，4
    utf-32  4

gbk
gb18030

考虑任何东西的时候，都有一个编码
1. console
2. file
3. editor
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


class RecommendItem(Model):
    """
    存储推荐商品信息
    """
    def __init__(self):
        self.title = ''
        self.cover_url = ''
        self.abstract = ''


def cached_url(url):
    """
    缓存, 避免重复下载网页浪费时间
    """
    folder = 'cached_zh'
    filename = url.rsplit('/')[-2] + '.html'
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 建立 cached 文件夹
        if not os.path.exists(folder):
            os.makedirs(folder)

        driver.get(url)
    #    return driver.page_source
    #    return driver.page_source
        with open(path, 'wb') as f:
            f.write(driver.page_source.encode())
        content = driver.page_source
        return content


def item_from_div(div):
    """
    从一个 div 里面获取到一个电影信息
    """
    e = pq(div)

    # 小作用域变量用单字符
    m = RecommendItem()
    m.abstract = e(".post_box_main .text").text()
    m.name = e(".title_box a").text()
    m.cover_url = e('.post_box_img img').attr('src')
    return m


def item_from_url(url):
    """
    从 url 中下载网页并解析出页面内所有的电影
    """
    page = cached_url(url)
    e = pq(page)
    items = e(".post_box")
    return [item_from_div(i) for i in items]


def main():
    items = item_from_url('http://zhizhizhi.com/gn/1/')
    for i in range(0, 10):
        items = item_from_url("http://zhizhizhi.com/gn/{}/".format(i))
        print(items)
    driver.close()


if __name__ == '__main__':
    main()
