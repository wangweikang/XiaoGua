'''
1. vagrant(装VirtualBox/vmr)
常用指令：
1）初始化  vagrant init(windows下启动需要管理员权限)
2）编辑 Vagrantfile 文件中的相关内容 比如：config.vm.box = "ubuntu"
3）加载虚拟机 vagrant box add ubuntu(上行的名字) .box文件完整路径
4）启动 vagrant up
5）连接/退出 vagrant ssh/exit
6）打包 vagrant package
多用管理工具

    虚拟化：
    openstack
    docker
2. 架构
web application web应用
SOA 面向服务编程
micro service 微服务
    2.1 不同服务 tcp通信 语言的异构
    2.2 数据接口api， 前端渲染 or 前后端渲染混合
    2.3 自动弹性，容器，虚拟化，LaaS PaaS
3. 分布式
CAP猜想->CAP定理(做分布式的指导思想) CAP三者只能同时保证两者
C 一致性
A 可用性
P 网络分区(一些服务器挂了，另一些还在运行，必须保证的)的可容忍性
    3.1. 小米
    3.2. 电商 做秒杀
4. 后端现有架构图

5. jsonrpc ? xmlrpc? soap ? restful api?
jsonrpc 建立在http协议上 json result['result']
xmlrpc http xml
soap
restful api 使用http标头来做增删改查 http method
6. 性能的代价
jsonrpc ? 缺点
 6.1 overhead  head很长，在网络中传输时间长
 6.2 单工
         好处
 6.3 简单
 6.4 不会乱序

 tcp传数据 并且双工  方法？
7. websocket js socket socket-io

8. 聊天室
1. 聊天，room，对于room广播
2. 加入房间，退出房间
3. jquery
4. socket.io
5. socket.io server
6. tcp层面 socket io 无法操纵session等http层面的东西
'''