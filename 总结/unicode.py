从明文到密码是加密，从密码到明文是解密。
在python中，编码：unicode-->str;解码str-->unicode.
既然是编码，那么就和密码领域一样，编码和解码自然涉及到编码/解码方案（对应加密或者解密算法），unicode相当于明文。

str.encode() 设涉及到了一个隐式转化的过程，即：str.decode(sys.defaultencoding).encode()

unicode 函数就是把 str 转化成 unicode 类

任何两种字符编码之间如果想完成转化，必须要通过unicode这个桥梁，先把它抓化成unicode对象；
unicode对象直接进行输出，往往会出现乱码，需要解码成str对象。
另外需要注意：unicode对象，gbk编码，ascii编码，str对象这四个不同的概念。
注意区分什么是字符串类型，什么是编码类型。

不到必须时不要在你的程序里编解码Unicode字符，只在你要写入文件或者数据库或者网络时，才调用encode()函数和decode()函数，
所以，该怎么写就怎么写吧，一旦涉及到写入的操作，再调用这两个方法，转化为相应的编码格式。

总结一下相关的错误：
1. no encoding declared，这个一般是系统默认的编码和你输入的字符有冲突，比如 ascii 就不能识别中文。
2. ‘ascii’ codec can’t decode，decode 时系统的默认编码（ascii）不符合该str原编码格式。
