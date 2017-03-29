var log = function() {
    console.log.apply(console, arguments)
}

var e = function(selector) {
    return document.querySelector(selector)
}

var appendHtml = function(element, html) {
	element.insertAdjacentHTML('beforeend', html)
}

var bindEvent = function(element, eventName, callback) {
    element.addEventListener(eventName, callback)
}

var bindAll = function(selector, eventName, callback) {
    var elements = document.querySelectorAll(selector)
    for(var i = 0; i < elements.length; i++) {
        var e = elements[i]
        bindEvent(e, eventName, callback)
    }
}

var removeClassAll = function(className) {
    var selector = '.' + className
    var elements = document.querySelectorAll(selector)
    for (var i = 0; i < elements.length; i++) {
        var e = elements[i]
        e.classList.remove(className)
    }
}

let Music = [
    {
        src: 'mp3/1.mp3',
        name: '1',
        liked: false,
    },
    {
        src: 'mp3/2.mp3',
        name: '2',
        liked: false,
    },
    {
        src: 'mp3/3.mp3',
        name: '3',
        liked: false,
    },
    {
        src: 'mp3/4.mp3',
        name: '4',
        liked: false,
    },
    {
        src: 'mp3/5.mp3',
        name: '5',
        liked: false,
    },
    {
        src: 'mp3/6.mp3',
        name: '6',
        liked: false,
    },
    {
        src: 'mp3/7.mp3',
        name: '7',
        liked: false,
    }
]

const actives = function(){
	if(e('#action').classList.contains('actives')) {
		var className = 'actives'
		removeClassAll(className)
		var c = e('#stop')
		c.classList.add(className)
	} else {
		var className = 'actives'
		removeClassAll(className)
		var c = e('#action')
		c.classList.add(className)
	}
}

//换按钮
const change = function(){
	if(e('#action').classList.contains('actives')) {
		var className = 'actives'
		removeClassAll(className)
		var c = e('#stop')
		c.classList.add(className)
     }
}

//换背景名字
const img = function(newIndex){
	var img = e('.img')
	var twoimg = e(".two-img")
	img.src = `img/${newIndex}.jpg`
	twoimg.src = `img/${newIndex}.jpg`
	var newId = '#name-'+ String(newIndex)
	var className = 'active'
	removeClassAll(className)
	var c = e(newId)
	c.classList.add(className)
	var newId = '#name1-'+ String(newIndex)
	var nameClass = 'action'
	removeClassAll(nameClass)
	var a = e(newId)
	a.classList.add(nameClass)
}

//开始
const bindAction = function() {
	var element = e('#action')
	bindEvent(element, 'click', function(){
		var a = e('#id-audio-player')
		a.play()
		actives()
        yanse()
	})
}


//暂停
const bindStop = function() {
	var element = e('#stop')
	bindEvent(element, 'click', function(){
		var a = e('#id-audio-player')
		a.pause()
		actives()
        yanse()
	})
}


//分秒
const rjust = function(str, size, delimeter='0') {
	var result = str
	while(result.length < size) {
		result = delimeter + result
	}
	return result
}
const formatTime = function(sum) {
	var m = String(Math.floor(sum % 3600 / 60))
	var s = String(Math.floor(sum % 60))
	var time = `${rjust(m, 2)}:${rjust(s, 2)}`
	return time
}

//总时间
const bindTime = function() {
	var a = e('#id-audio-player')
	bindEvent(a,'canplay',function(){
		var sum = parseInt(a.duration)
		var value = formatTime(sum)
		var time = e('#time')
		time.innerHTML = value
	})
}

const showTime =  function(event){
    var audio = e('#id-audio-player')
    var target = event.target
    var sum = audio.currentTime
    var value = formatTime(sum)
    var now = e('#nowTime')
    now.innerHTML = value
    var input = audio.currentTime / audio.duration * 100
    // console.log('input', input);
    if (Boolean(input) == true) {
        e('.range').value = input
        var b = e('.range').value
        e('.range').style.background = `linear-gradient(90deg, rgba(0, 0, 0, 0.1)${b}%, rgba(255, 255, 255, 1)${b}%)`;
    }
}

//当前时间
const nowtime = function() {
    var audio = e('#id-audio-player')
    audio.addEventListener('timeupdate', showTime)
}

//列表颜色
const yanse = function() {
    let audio = e('audio')
    let id = parseInt(audio.dataset.now)
    var newId = '#title-'+ String(id)
        var className = 'yanSe'
		removeClassAll(className)
		var c = e(newId)
		c.classList.add(className)
}

//通用
const goIndex = function(newIndex) {
    var audio = e('audio')
    audio.src = Music[newIndex].src
    bindEvent(audio, 'canplay', function(){
            audio.play()
            img(newIndex)
            change()
            showHeart(newIndex)
            yanse()
        })
        audio.dataset.now = newIndex
}

//上一首
const bindPrev = function() {
    var selector = e('#shangSong')
    bindEvent(selector, 'click', function(){
        let audio = e('audio')
        let index = parseInt(audio.dataset.now)
        let zongUu = Music.length
        let newIndex = (index + zongUu - 1) % zongUu
        goIndex(newIndex)
    })
}


//下一首
const bindNext = function() {
    var selector = e('#nextSong')
    bindEvent(selector, 'click', function(){
        let audio = e('audio')
        let index = parseInt(audio.dataset.now)
        let zongUu = Music.length
        let newIndex = (index + 1) % zongUu
        goIndex(newIndex)
    })
}


// 给 input range 添加拖动事件
const bindRange = function() {
    e('.range').addEventListener('input', function(event){
        e('#id-audio-player').removeEventListener('timeupdate', showTime)
        var v = this.value
        // console.log('v', v)
    	e('#id-audio-player').currentTime = e('#id-audio-player').duration * v / 100
        nowtime()
    })
}

const showHeart = function(now) {
    let className = 'pink-heart'
    let a = e('.heart')
    if (Music[now].liked === true) {
        a.classList.add(className)
    } else {
        a.classList.remove(className)
    }
    // log('Music[now].liked',Music[now].liked)
}

//心
const bindHeart = function() {
    var b = e('.heart')
    var audio = e('audio')
    bindEvent(b, 'click', function(){
        let now = audio.dataset.now
        var className = 'pink-heart'
        if (Music[now].liked === true) {
            Music[now].liked = false
            b.classList.remove(className)
        } else {
            Music[now].liked = true
            b.classList.add(className)
        }
    })
}

//列表
const bindList = function(){
    var list = e('.list')
    var a = e('.gray')
    bindEvent(list, 'click', function(){
        var className = 'move'
    	removeClassAll(className)
        var classN = 'move-1'
        a.classList.add(classN)
    })
    bindEvent(a, 'click', function(){
        var className = 'move'
        var songList = e('.songList')
    	songList.classList.add(className)
        var classN = 'move-1'
        removeClassAll(classN)
    })
}

//列表点歌
const bindClick = function() {
    var selector = '.songtitle'
    bindAll(selector, 'click', function(event){
        let target = event.target
        let newIndex = parseInt(target.dataset.path)
        goIndex(newIndex)
    })
}

//循环
const bindAlways = function() {
    var selector = e('audio')
    bindEvent(selector, 'ended', function(){
        let audio = e('audio')
        let index = parseInt(audio.dataset.now)
        let zongUu = Music.length
        let newIndex = (index + 1) % zongUu
        goIndex(newIndex)
    })
}

const bindalls = function() {
    bindAction()
    bindStop()
    bindTime()
    bindPrev()
    bindNext()
    bindRange()
    bindHeart()
    bindList()
    bindClick()
    bindAlways()
    nowtime()
}

const __main = function(){
    bindalls()
}
__main()
