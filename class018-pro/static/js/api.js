
var api = {}

api.ajax = function(url, method, form, success, error) {
  var request = {
    url: url,
    type: method,
    data: form,
    success: function(response){
      var r = JSON.parse(response)
      success(r)
    },
    error: function(err){
      log('网络错误', error)
      var r = {
        'success': false,
        message: '网络错误'
      }
      error(r)
    }
  }
  $.ajax(request)
}

api.get = function(url, success, error) {
  api.ajax(url, 'get', {}, success, error)
}

api.post = function(url, form, response) {
  api.ajax(url, 'post', form, response, response)
}

// weibo API
api.weiboAdd = function(form, response) {
  var url = '/api/weibo/add'
  api.post(url, form, response)
}

api.weiboDelete = function(weiboId, success, error) {
  var url = '/api/weibo/delete/' + weiboId
  var form = {}
  api.get(url, success, error)
}

// 评论 API

// 用户 API
