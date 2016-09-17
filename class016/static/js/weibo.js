// window.onload = main;


var log = function() {
  console.log(arguments)
}

var weiboTemplate = function(weibo) {
  var w = weibo
  var t = `
    <div class="weibo-cell cell item">
      <img src="${ w.avatar }" class="avatar">
      <span>${ w.weibo }</span>
      <span class="right span-margin">${ w.created_time }</span>
      <span class="right span-margin">by: ${ w.name }</span>
      <div class="right span-margin">
        <button class="weibo-delete" data-id="${ w.id }">删除</button>
        <a href="#" class="com">评论(${ w.comments_num })</a>
      </div>
      <div class="comment-div hide">
        <div class="">
        </div>
          <input type="hidden" name="weibo_id" value="${ w.id }">
          <input name="comment" class="left m" placeholder="Comment">
          <button>发表</button>
      </div>
    </div>
  `
  return t
}

$(document).ready(function(){
  // 展开评论事件
  $('a.com').on('click', function(){
    $(this).parent().next().slideToggle()
    return false;
  })


  // 绑定删除微博按钮事件
  $('.weibo-container').on('click', '.weibo-delete', function(){
    var weiboId = $(this).data('id')
    log(weiboId)
    var weiboCell = $(this).closest('.weibo-cell')

    var success = function(response) {
      console.log('成功', arguments)
      $(weiboCell).slideUp()
      alert("删除成功")
      // $('.weibo-container').prepend(weiboTemplate(w))
    }
    var error = function() {
          console.log('错误', arguments)
          alert("删除失败")
    }
    api.weiboDelete(weiboId, success, error)
  })

  // 给按钮绑定添加 weibo 事件
  $('#id-button-weibo-add').on('click', function(){
    var weibo = $('#id-input-weibo').val()
    log('weibo,', weibo)
    var form = {
      weibo: weibo,
    }

    var response = function(r) {
        console.log('成功', arguments)
        log(r)
        if(r.success) {
          var w = r.data
          $('.weibo-container').prepend(weiboTemplate(w))
          alert("添加成功")
        } else {
          alert(r.message)
        }
    }

    api.weiboAdd(form, response)
  })
})
/*
function main(){
  $('a.com').on('click', function(){
    $(this).parent().next().slideToggle()
    return false;
  })

  $('a.blog-com').on('click', function(){
    $(this).parent().next().slideToggle()
    return false;
  })

  $('.blog-comment-add').on('click', function(){
      console.log('add button')
      var button = $(this)
      var parent = button.parent()
      var blog_id = parent.find('.comment-blog_id').val()
      console.log('weibo', blog_id)
      var comment = parent.find('.comment-content').val()
      console.log('comment', comment)

      var commentList = parent.parent().find('.comment-list')
      console.log('commentList', commentList)

      var weibo = {
          'blog_id': blog_id,
          'comment': comment
      }
      var request = {
          url: '/blog/comment',
          type: 'post',
          data: weibo,
          success: function() {
              console.log('成功', arguments)
              var response = arguments[0]
              var comment = JSON.parse(response)
              var content = comment.comment
              var avatar = comment.avatar
              var created_time = comment.created_time
              var name = comment.name
              var cell = `
                  <div class="cell-inner item">
                    <img src="${avatar}" class="avatar-s">
                    <span class="comment">${content}</span>
                    <span class="time right span-margin">${created_time}</span>
                    <span class="name right span-margin">by:${name}</span>
                  </div>
              `;
              commentList.append(cell)
              parent.find('.comment-content').val("")

          },
          error: function() {
              console.log('错误', arguments)
          }
      }
      $.ajax(request)
  })


}
*/
