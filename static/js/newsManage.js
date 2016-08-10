/**
 * Created by jeezy-lyoung on 16-8-4.
 */
$(document).ready(function () {

    $("#read_list").mouseover(function () {
        document.getElementById('read_list').style.backgroundColor = "#FFBBFF";
    });

    $("#read_list").mouseout(function () {
        document.getElementById('read_list').style.backgroundColor = "#FFAEB9";
    });


    $("#love_list").mouseover(function () {
        document.getElementById('love_list').style.backgroundColor = "#f9d5b0";
    });

    $("#love_list").mouseout(function () {
        document.getElementById('love_list').style.backgroundColor = "#f9c693";
    });


    $("#comment_list").mouseover(function () {
        document.getElementById('comment_list').style.backgroundColor = "#fbe8af";
    });

    $("#comment_list").mouseout(function () {
        document.getElementById('comment_list').style.backgroundColor = "#f7dd90";
    });


    $("#delete_but").mouseover(function () {
        document.getElementById('delete_but').style.backgroundColor = "#c4ddb9";
    });

    $("#delete_but").mouseout(function () {
        document.getElementById('delete_but').style.backgroundColor = "#b6d7a8";
    });




    








    /*自适应高度*/
    var news_list_height = document.getElementById('news_list');
    var each_news_height = document.getElementsByClassName('each_news');

    var show_height;
    if (navigator.userAgent.indexOf("Firefox") > 0) {
        show_height = document.documentElement.scrollHeight;
    }
    if (window.navigator.userAgent.indexOf("Chrome") !== -1 || navigator.userAgent.indexOf("Safari") > 0) {
        show_height = document.body.scrollHeight;
    }
    if (navigator.userAgent.indexOf("MSIE") > 0) {
        show_height = (document.documentElement.scrollHeight > document.documentElement.clientHeight) ? document.documentElement.scrollHeight : document.documentElement.clientHeight;
    } else {
        show_height = (document.documentElement.scrollHeight > document.documentElement.clientHeight) ? document.documentElement.scrollHeight : document.documentElement.clientHeight;
    }
    news_list_height.style.height = (show_height - 300)*0.9 + "px";
    news_list_height.style.marginTop = (show_height - 300)*0.1 + "px";
    news_list_height.style.marginBottom = (show_height - 300)*0.1 + "px";
    //news_list_height.style.fontSize = ($(".each_news").height())*0.5+ "px";
    //alert($(".each_news").height());











});