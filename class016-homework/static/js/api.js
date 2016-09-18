// 定义一个空对象
// 这个对象用来和服务器通信
// 这样我们只需使用函数而不用关心服务器的具体细节
var api = {}

/*
给对象添加一个 ajax 方法
它接受 url method form 等 4 个参数
其中 callback 是函数，用于在收到服务器响应后回调
*/
api.ajax = function(url, method, form, callback) {
  // 生成一个请求
  var request = {
    url: url,
    type: method,
    data: form,
    success: function(response){
        // 这个 response 是 ajax 给我们传的参数
        // 解析后 调用 callback 函数并把参数传给他
        var r = JSON.parse(response)
        callback(r)
    },
    error: function(err){
      // 本函数会在请求发生错误的时候被调用
      // 服务器返回非 200-300 的状态码或者网络错误都会触发
      log('网络错误', error)
      // 对于错误，我们构造一个对象并调用 callback 函数
      var r = {
        'success': false,
        message: '网络错误'
      }
      callback(r)
    }
  }
  // 用 jQuery 的 ajax 函数发送这个请求
  $.ajax(request)
}

// api 内部函数，发一个 get 请求
api.get = function(url, response) {
    // 因为 get 函数不需要传递 form 参数
    // 所以用一个空对象 {} 填充参数
    api.ajax(url, 'get', {}, response)
}

/*
api 内部函数，发一个 post 请求
*/
api.post = function(url, form, response) {
    // response 是一个回调函数
    api.ajax(url, 'post', form, response)
}

// ====================
// 以上是内部函数，内部使用
// --------------------
// 以下是功能函数，外部使用
// ====================

// weibo API
api.weiboAdd = function(form, response) {
    // 添加一条微博  response 是回调函数
    var url = '/api/weibo/add'
    api.post(url, form, response)
}

api.weiboDelete = function(weiboId, response) {
    // 删除一条微博
    var url = '/api/weibo/delete/' + weiboId
    var form = {}
    api.get(url, response)
}

// 评论 API

// 用户 API
