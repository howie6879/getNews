/**
 * Created by jeezy-lyoung on 16-8-2.
 */
$(document).ready(function () {

    var net = "http://127.0.0.1:8888";
    var count = 3;
    var page_value = 1;
    var alrequest = 0;
    var page = "xia";
    var time = '1';
    var tooken = '764bfd755bc07f6871eee104219b2b2c';



    function get_user() {
        var qx = {"alrequest":alrequest,"page":page,"time":time, "tooken":tooken};
    $.ajax({
        type:"get",
        url:net + "/api/adminfeedback?count=3",
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
                    var u_id = "";
                    var feed_content = "";
                    var get_time = ""
                    var name = "";
                    var is_rep = "";
                    var rep_button = "";
                    for(i=0;i<all_data.length;i++){
                        name = "<div class='feedback_name'>"+ all_data[i].user_name +": </div>"
                        feed_content = "<div class='feedback_content'>"+ all_data[i].contents +": </div>"
                        get_time = "<div class='feedback_gettime'>"+ all_data[i].times +": </div>"
                        is_rep = "<div class='feedback_isreply'>是否已审批: <span class='rep'>否</span>: </div>"
                        rep_button = "<input class='rep_button' type='button' value='审批'>"
                        table = table +  "<div class='each_feedback'>" +name+feed_content+get_time+is_rep+rep_button + "</div>"

                    }

                    document.getElementById("not_feedback").innerHTML = table;



                }

        }



    });
    }

    get_user();

    $("#xia").click(function () {
        page = "xia";
        alrequest = page_value * 3;
        get_user();
        page_value = page_value + 1;



    });

    $("#shang").click(function () {
        page = "shang";
        if (page_value == 1){
            alert("已是第一页")
        }else{
            page_value = page_value - 1 ;
            alrequest = page_value * 3;
            get_user();

        }



    });


    
    


})