/**
 * Created by jeezy-lyoung on 16-7-31.
 */

function info_none(user_id) {
    document.getElementById("user_info").style.display = "none";
}

function user_info(user) {
    var user_id = user.toString();
    var net = "http://127.0.0.1:8888";
    var time = '1';
    var tooken = '764bfd755bc07f6871eee104219b2b2c';

    for (i=0;i<6-user.toString().length;i++){
        user_id = '0' + user_id;
    }
    var qx = {"time":time, "tooken":tooken};
    $.ajax({
        type:"get",
        url:net + "/api/adminuserinfo?user_id="+user_id,
        data:qx,
        cache:false,
        success:function(data) {

            var is_success;
                var result = eval('(' + data + ')');
                var all_data = result.data;
                is_success = result.message;

                if (is_success == "failed"){

                }
                else{
                    var phone = "<div class='each_info'>电话:"+ all_data.phone +"</br></div>"
                    var age = "<div class='each_info'>年龄:"+ all_data.age +"</br></div>"
                    var sex = "<div class='each_info'>性别:"+ all_data.sex +"</br></div>"
                    var address = "<div class='each_info'>地址:"+ all_data.address +"</br></div>"
                    var email = "<div class='each_info'>邮箱:"+ all_data.email +"</br></div>"

                    document.getElementById("user_info").innerHTML = phone + age + sex + address + email;
                    document.getElementById("user_info").style.display = "block";

                }

        }





    });
    
    
    
}

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
    //left_show.style.height = left_show_height - 50 + "px";
    var second_show = document.getElementById('second');
    second_show.style.height = left_show_height - 50 + "px";
    
    
    var net = "http://127.0.0.1:8888";
    var count = 6;
    var page_value = 1;
    var alrequest = 0;
    var page = "next";
    var time = '1';
    var tooken = '764bfd755bc07f6871eee104219b2b2c';



    function get_user() {
        var qx = {"alrequest":alrequest,"page":page,"time":time, "tooken":tooken};
    $.ajax({
        type:"get",
        url:net + "/api/adminuser?count=6",
        data:qx,
        cache:false,
        success:function(data) {

            var is_success;

                var result = eval('(' + data + ')');
                var all_data = result.data;
                is_success = result.message;

                if (is_success == "failed"){
                    alert("已是最后一页");
                    page_value = page_value - 1;
                }
                else{
                    var table = "";
                    for(i=0;i<all_data.length;i++){
                        table = table + "<tr>" + "<td>"+ all_data[i].user_id +"</td>" + "<td><a id='"+all_data[i].user_id +"' onMouseOver='user_info("+ all_data[i].user_id +")' onmouseout='info_none("+ all_data[i].user_id +")'>"+ all_data[i].user_name +"</a></td>" + "</tr>"
                    }

                    document.getElementById("page1").innerHTML = "<table class='table table-bordered'>" + "<caption>用户管理</caption>" +"<thead>" +"<tr>" + "<th>用户编号</th>" + "<th>昵称</th>" + "</tr>" + "</thead>" + "<tbody>" + table + "</tbody>" + "</table>";



                }

        }



    });
    }

    get_user();

    $("#next").click(function () {
        page = "next";
        alrequest = page_value * 6;
        get_user();
        page_value = page_value + 1;



    });

    $("#last").click(function () {
        page = "last";
        if (page_value == 1){
            alert("已是第一页")
        }else{
            page_value = page_value - 1 ;
            alrequest = page_value * 6;
            get_user();

        }



    });


    
    


})