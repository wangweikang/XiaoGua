
const log = function() {
    console.log.apply(console, arguments)
}

const e = function(selector) {
    return document.querySelector(selector)
}

const es = function (sel) {
    return document.querySelectorAll(sel)
}

const bindEvent = function(element, eventName, callback) {
    element.addEventListener(eventName, callback)
}

const bindAll = function(selector, eventName, callback) {
    var elements = document.querySelectorAll(selector)
    for(var i = 0; i < elements.length; i++) {
        var e = elements[i]
        bindEvent(e, eventName, callback)
    }
}

const removeClassAll = function(className) {
    var selector = '.' + className
    var elements = document.querySelectorAll(selector)
    for (var i = 0; i < elements.length; i++) {
        var e = elements[i]
        e.classList.remove(className)
    }
}

const toggleClass = function(element, className) {
    if (element.classList.contains(className)) {
        element.classList.remove(className)
    } else {
        element.classList.add(className)
    }
}

const nowTime = function() {
    var d = new Date()
    var nm = d.getFullYear()
    var yt = d.getMonth() + 1
    var ri = d.getDate()
    var week = d.getDay()
    var array = ['日','一','二','三','四','五','六']
    var weeks = array[week]
    var time = `${nm}-${yt}-${ri} 星期${weeks}`
    log('time',time)
    // e('.date').innerHTML = `${time}`
    e('.time-tite').innerHTML = `${time}`
}

const bindAdd = function() {
    var addButton = e('#id-newTodo')
    addButton.addEventListener('click', function(){
        var todoInput = e('#id-input-add')
        var todo = todoInput.value
        insertTodo(todo, false)
        saveTodos()
        todoInput.value = ''
        // console.log('value',todoInput.value );
    })
}

const insertTodo = function(todo, done) {
    var todoContainer = e('#id-div-container')
    var t = templateTodo(todo, done)
    todoContainer.insertAdjacentHTML('beforeend', t);
    // log('done',done)
}

const templateTodo = function(todo, done) {
    var d = new Date()
    var hours = d.getHours()
    var minutes = d.getMinutes()
    if(hours < 10) {
        hours = `0${hours}`
    }
    if(minutes < 10) {
        minutes = `0${minutes}`
    }
    var time = `${hours}:${minutes}`
    var t = localTodo(todo, done, time)
    return t
}

const bindDonedelete = function() {
    var todoContainer = e('#id-div-container')
    todoContainer.addEventListener('click', function(event){
        // log('container click', event, event.target)
        var target = event.target
        if(target.classList.contains('todo-done')) {
            // log('done')
            var todoDiv = target.parentElement
            toggleClass(todoDiv, 'done')
            toggleClass(target, 'fa-check-circle-o')
            toggleClass(target, 'fa-circle-thin')
            saveTodos()
        } else if (target.classList.contains('todo-delete')) {
            // log('delete')
            var todoDiv = target.parentElement
            todoDiv.remove()
            saveTodos()
        }
    })
}

const bindTheme =function() {
    var selector = e('.theme')
    bindEvent(selector, 'click', function() {
    // var classname = e('.theme-o')
    // e('.theme-color').classList.toggle(classname)
    var se = e('.theme-color')
    se.style.height = '180px';
    })

    var shang = e('.shou')
    bindEvent(shang, 'click', function() {
    var se = e('.theme-color')
    se.style.height = '0px';
    })

}

const bindBlack = function() {
    var selector = e('#theme-0')
    bindEvent(selector, 'click', function() {
        e('.index').style.background = '#353d40';
        e('.date').style.color = '#353d40';
        e('.list').style.background = 'rgb(64, 72, 75)';
        e('.list').style.color = '#00bff3';
        e('.list-0').style.background = '#2c3032';
        e('.list-0').style.color = '#00bff3';
    })
}

const bindPink = function() {
    var selector = e('#theme-1')
    bindEvent(selector, 'click', function() {
        e('.index').style.background = 'rgba(242, 70, 70, 0.34)';
        e('.date').style.color = 'rgba(242, 70, 70, 0.34)';
        e('.list').style.background = 'rgba(242, 70, 70, 0.35)';
        e('.list').style.color = 'white';
        e('.list-0').style.background = 'rgba(242, 70, 70, 0.65)';
        e('.list-0').style.color = 'white';
    })
}

const bindBlue = function() {
    var selector = e('#theme-2')
    bindEvent(selector, 'click', function() {
        e('.index').style.background = 'rgba(118, 195, 221, 0.73)';
        e('.date').style.color = 'rgba(118, 195, 221, 0.73)';
        e('.list').style.background = 'rgba(118, 195, 221, 0.6)';
        e('.list').style.color = 'white';
        e('.list-0').style.background = 'rgb(100, 194, 226)';
        e('.list-0').style.color = 'white';
    })
}

localStorage.name = 'funyear'

const save = function(array) {
    var s = JSON.stringify(array)
    localStorage.todos = s
}

const load = function() {
    var s = localStorage.todos
    return JSON.parse(s)
}

const saveTodos = function() {
    // log('save todos')
    var contents = document.querySelectorAll('.todo-content')
    var times = document.querySelectorAll('.thingTime')
    var todos = []
    for (var i = 0; i < contents.length; i++) {
        var c = contents[i]
        var t = times[i]
        var done = c.parentElement.classList.contains('done')
        var todo = {
            done: done,
            content: c.innerHTML,
            time: t.innerHTML,
        }
        // log('t', t.innerHTML)
        todos.push(todo)
    }
    save(todos)
}

const insertlocalTodo = function(todo, done, time) {
    var todoContainer = e('#id-div-container')
    var t = localTodo(todo, done,time)
    todoContainer.insertAdjacentHTML('beforeend', t);
}

const localTodo = function(todo, done,time) {
    var status = ''
    var gou = 'fa-circle-thin'
    if(done) {
        status = 'done'
        gou = 'fa-check-circle-o'
    }
    var t = `
    <div class='todo-cell ${status}'>
        <time class='thingTime'> ${time}</time>
        <span class='todo-done todo-check fa ${gou}'></span>
        <span class='todo-content'>${todo}</span>
        <i class="todo-delete fa fa-trash" aria-hidden="true"></i>
    </div>
    `
    return t
}

const loadTodos = function() {
    var todos = load()
    // log('load todos', todos)
    for (var i = 0; i < todos.length; i++) {
        var todo = todos[i]
        insertlocalTodo(todo.content, todo.done, todo.time)
    }
    // log('t', todo.time)
}

const init =function() {
    nowTime()
    loadTodos()
}

const bindalls = function() {
    bindAdd()
    bindDonedelete()
    bindTheme()
    bindBlack()
    bindPink()
    bindBlue()
}

const __main = function() {
    init()
    bindalls()
}
__main()
