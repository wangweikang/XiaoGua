/*
需要掌握的 jQuery 知识
AJAX 相关的内容请看 api.js


1, 选择各种元素的方法

普通标签选择器, 用标签名
$('body')

id 选择器, id 前加 #
$('#id-button-weibo-add')

class 选择器, class 前加 .
$('.weibo-cell')


用一个元素找到其他元素
例如在 .weibo-delete 的回调函数中中找到 .weibo-cell
$('body').on('click', '.weibo-delete' function(event){
    // 回调函数其实有一个 event 参数
    // 用 event.target 就可以得到响应事件的标签, 这里是按钮
    var button = $(event.target)

    // 用 closest 找到一个父（或者爷或者爷爷爷爷爷）节点
    // 总之是包含自己的某个上层元素
    var cell = button.closest('.weibo-cell')

    // 可以用 parent 函数得到自己的父节点
    // 比如 cell.parent() 会得到 <div class="box weibo-container">

    // 有了 cell 就可以找到 .weibo-content
    // 使用的函数是 find
    // find 用于查找子节点
    var span = cell.find('.weibo-content')

    // 得到标签内的文本数据用 text 函数
    var weibo = span.text()
    // 同样的, 你也可以用这个函数设置它的文本数据
    span.text('hello')


    // DOM 操作用于增加、删除、修改网页上的元素
    // append 用于增加
    // $('body').append('<h1>网页尾巴</h1>')

    // remove 用于删除
    cell.remove()

    // 控制显示
    span.show()
    span.hide()
    // 或者开关显示
    span.toggle()


    // 下面三个函数用于操作元素的 class
    // 典型的应用比如选中元素高亮、跑马灯幻灯片等
    // addClass removeClass toggleClass
})
*/
