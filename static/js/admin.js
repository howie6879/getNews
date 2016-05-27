$(document).ready(function () {
    //更改密码
    $('#changePass').click(function () {
        var pass = $("#pass").val();
        var confirm = $("#confirm").val();
        if (pass == confirm) {
            $.get("/changePass", {pass: pass}, function (result) {
                alert(result)
                $('#close').trigger('click');
            });
        } else {
            alert("请确认您是否输入正确")
        }
    });
    //home 数据处理步骤
    var numOperator = $('.col-operator');
    for (i = 0; i < numOperator.length; i++) {
        numOperator.eq(i).click(function () {
            numOperator.removeClass('col-operator-active');
            $(this).addClass('col-operator-active')
        })
    }
    //home 底部cmd窗口效果
    $('.show-nav-right-down').click(function () {
        $('.show-nav-right-down').css("display", "none");
        $('.show-nav-right-up').css("display", "block");
        $('.show-nav').css("background-color","rgb(106, 127, 127)");
        $(".showlog").animate({height: '20px'});
    });
    $('.show-nav-right-up').click(function () {
        $('.show-nav-right-down').css("display", "block");
        $('.show-nav-right-up').css("display", "none");
        $('.show-nav').css("background-color","#0C0C0C");
        $(".showlog").animate({height: '300px'});
    });
    /*解决底部栏footer在高度不适应情况下在底部*/
    var left_show = document.getElementById('left');
    var left_show_height;
    if (navigator.userAgent.indexOf("Firefox") > 0) {
        left_show_height = document.documentElement.scrollHeight;
    }
    if (window.navigator.userAgent.indexOf("Chrome") !== -1 || navigator.userAgent.indexOf("Safari") > 0) {
        left_show_height = document.body.scrollHeight;
    }
    if (navigator.userAgent.indexOf("MSIE") > 0) {
        left_show_height = (document.documentElement.scrollHeight > document.documentElement.clientHeight) ? document.documentElement.scrollHeight : document.documentElement.clientHeight;
    } else {
        left_show_height = (document.documentElement.scrollHeight > document.documentElement.clientHeight) ? document.documentElement.scrollHeight : document.documentElement.clientHeight;
    }
    left_show.style.height = left_show_height - 50 + "px";
})