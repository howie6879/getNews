$(document).ready(function () {
    /*自适应高度*/
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
    //var second_show = document.getElementById('second');
    //second_show.style.height = left_show_height - 50 + "px";
    
    //dataAna
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
    //数据处理
    $('#getNewsStart').click(function () {
        var ttSelect = $("#ttSelect").val();
        var page = $("#page").val();
        var num = $("#num").val();
        $(".show-content").html("<p>开始进行新闻获取:</p>");
        $(".show-content").append("<p>数据量较多,请耐心等待...</p>");
        $.get("/dataOperator", {action: "getNews", ttSelect: ttSelect, page: page, num: num}, function (result) {
            $(".show-content").append("<p>新闻爬取完成,请继续下一步!</p>");
            $('#close2').trigger('click');
        });
    });
    //新闻去重
    $('#repeatedData').click(function () {
        if (confirm("是否已经进行新闻获取？")) {
            $(".show-content").append("<p>正在进行数据去重...</p>");
            $.get("/dataOperator", {action: "repeatedData"}, function (result) {
                $(".show-content").append("<p>数据去重完成,请继续下一步!</p>");
            });
        }
    });
    //特征词分析
    $('#anaData').click(function () {
        if (confirm("是否已经进行新闻去重？")) {
            $(".show-content").append("<p>正在进行内容分析...</p>");
            $.get("/dataOperator", {action: "anaData"}, function (result) {
                $(".show-content").append("<p>内容分析完成,请继续下一步!</p>");
            });
        }
    });
    //数据清洗
    $('#rmAllNews').click(function () {
        if (confirm("确定清洗数据？")) {
            $(".show-content").append("<p>正在进行数据清洗...</p>");
            $.get("/dataOperator", {action: "rmAllNews"}, function (result) {
                $(".show-content").append("<p>数据清洗完成,数据分析完成!</p>");
            });
        }
    });
    //数据保存
    $("#save").mouseover(function () {
        $("#save").attr("src", "/static/images/save.svg");
    });
    $("#save").mouseout(function () {
        $("#save").attr("src", "/static/images/save0.svg");
    });
    $('#save').click(function () {
        $(".show-content").html("<p>正在存储数据...</p>");
        $.get("/dataOperator", {action: "insertDB"}, function (result) {
            $(".show-content").append("<p>数据存储完成!</p>");
            $("#save").css("display", "none")
            $("#save1").css("display", "block")
        });
    });
    //home 底部cmd窗口效果
    $('.show-nav-right-down').click(function () {
        $('.show-nav-right-down').css("display", "none");
        $('.show-nav-right-up').css("display", "block");
        $('.show-nav').css("background-color", "rgb(106, 127, 127)");
        $(".showlog").animate({height: '20px'});
    });
    $('.show-nav-right-up').click(function () {
        $('.show-nav-right-down').css("display", "block");
        $('.show-nav-right-up').css("display", "none");
        $('.show-nav').css("background-color", "#0C0C0C");
        $(".showlog").animate({height: '300px'});
    });
})