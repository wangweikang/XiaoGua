"""
 
队列的特点是「先进先出」，一般有这几个操作

# enqueue 将一个元素存入队列中
# dequeue 将一个元素从队列中取出，并在队列中删除它

# empty 查看栈是否是空的


可以把队列看做排队，银行叫号机就是队列，先取号的先入队，叫号的时候也就先出队

"""


# Node类是一个节点，有两个属性，一个存储元素，一个存储指向另一个节点的引用
class Node():
    def __init__(self, element=None, next=None):
        self.element = element
        self.next = next

    # 这个函数是会在print的时候被自动调用，就是把这个Node显示出来
    def __repr__(self):
        return str(self.element)


class Queue():
    # 初始化函数，自动被调用
    # 初始化Queue()类的时候，它有2个属性，分别指向头尾
    def __init__(self):
        self.head = Node()
        self.tail = self.head
    
    # 如果head的next属性为空，则说明队列是空的
    def empty(self):
        return self.head.next is None

    # 创建一个node
    # 让tail.next指向它
    # 让tail指向它，tail现在就是新的队尾了
    def enqueue(self, element):
        n = Node(element)
        self.tail.next = n
        self.tail = n

    # 取出head.next指向的元素，如果队列不是空的，就让head.next指向node.next，这样node就不在队列中了
    def dequeue(self):
        node = self.head.next
        if not self.empty():
            self.head.next = node.next
        return node


# 测试函数
def test():
    q = Queue()

    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)

    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())


if __name__ == '__main__':
    # 运行测试函数
    test()
