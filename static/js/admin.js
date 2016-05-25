$(document).ready(function(){
    /*解决底部栏footer在高度不适应情况下在底部*/
    var left_show = document.getElementById('left');
    var left_show_height;
    if(navigator.userAgent.indexOf("Firefox")>0){
        left_show_height = document.documentElement.scrollHeight;
    }
    if(window.navigator.userAgent.indexOf("Chrome") !== -1||navigator.userAgent.indexOf("Safari")>0 ){
        left_show_height = document.body.scrollHeight;
    }
    if(navigator.userAgent.indexOf("MSIE")>0) {
        left_show_height = (document.documentElement.scrollHeight >document.documentElement.clientHeight) ? document.documentElement.scrollHeight : document.documentElement.clientHeight;
    }else{
        left_show_height = (document.documentElement.scrollHeight >document.documentElement.clientHeight) ? document.documentElement.scrollHeight : document.documentElement.clientHeight;
    }
    left_show.style.height = left_show_height-50+"px";
})