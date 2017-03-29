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

//通用
const tong = function(newIndex) {
		var newId = '#photo-'+ String(newIndex)
        var className = 'active'
		removeClassAll(className)
		var c = e(newId)
		c.classList.add(className)
        var n = (-8) * (newIndex)
        e('.box-reflect').style.transform = `translateX(${n}rem)`;
}

//点击图片
const clicks = function(){
    var selector = '.photo'
    bindAll(selector, 'click', function(event){
		var target = event.target
		var newIndex = parseInt(target.dataset.id)
		var father = event.target.parentElement
		var grandpa = father.parentElement
        var grandpapa = grandpa.parentElement
        tong(newIndex)
		grandpapa.dataset.active = newIndex
	})
}

//上一张
const prev = function() {
    var selector = '.prev'
	bindAll(selector, 'click', function(event){
    var father = event.target.parentElement
    var grandpa = father.parentElement
	var index = parseInt(grandpa.dataset.active)
    var zongUu = parseInt(grandpa.dataset.imgs)
	var newIndex = (index + zongUu - 1) % zongUu
    tong(newIndex)
	grandpa.dataset.active = newIndex
    })
}

//下一张
const next = function() {
    var selector = '.next'
    bindAll(selector, 'click', function(event){
        var father = event.target.parentElement
        var grandpa = father.parentElement
        var index = parseInt(grandpa.dataset.active)
        var zongUu = parseInt(grandpa.dataset.imgs)
        var newIndex = (index + 1) % zongUu
        tong(newIndex)
        grandpa.dataset.active = newIndex
    })
}

const button =function() {
    prev()
    next()
}

const __main = function() {
    clicks()
    button()
}
 __main()
