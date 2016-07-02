/**
 * Created by huangjunqin on 16-6-8.
 */
avalon.config({
    interpolate: ["{&", "&}"]
});

$(function () {
    //已选课程
    var choose = avalon.define({
        $id:"chooseModel",
        data:[]
    });
    $.getJSON('/choose/',null,function (data) {
         choose.data = data;
    });
    //可选课程
    var course = avalon.define({
        $id:"courseModel",
        data:[]
    });
    $.getJSON('/course/',null,function (data) {
        course.data = data;
    });
    //选课日志
    var log = avalon.define({
        $id:"logModel",
        data:[]
    });
    $.getJSON('/log/',null,function (data) {
        log.data = data; 
    });
    //选项卡效果
   $(".header-tab").bind("click",function () {
       $(".header-tab").removeClass("active");
       $(this).addClass("active");
       var index = $(this).index();
       $(".mytab").removeClass("tab-show").eq(index).addClass("tab-show")
   });
    //选课操作
    $(document).on("click",".select_course",function () {
        var that = $(this);
        var weight = that.parent().parent().find("input").eq(0).val();
        if(weight != "" && parseInt(weight) <= parseInt($("#weight").text()) && parseInt(weight) <= 100){
            var cid = that.parent().parent().find("th").eq(0).text();
            var tname = that.parent().parent().find("td").eq(1).text();
            $.ajax({
                url:"/select/",
                type:"POST",
                dataType:"json",
                data:{
                    "cid":cid,
                    "tname":tname,
                    "weight":parseInt(weight)
                },
                success:function (data) {
                    if(data.status == 0){
                        alert("操作成功!");
                        window.location.href = "/index/";
                    }else if(data.status == 1){
                        alert("操作失败！");
                    }
                },
                error:function () {
                    alert("服务器不太给力啊！")
                }
            })
        }else{
            alert("权重值只能是在0~"+ $("#weight").text() +"之间的数");
        }
    });
    //退课操作
    $(document).on("click",".cancel_course",function () {
        var that = $(this);
        var cid = that.parent().parent().find("th").eq(0).text();
            var tname = that.parent().parent().find("td").eq(1).text();
            $.ajax({
                url:"/cancel/",
                type:"POST",
                dataType:"json",
                data:{
                    "cid":cid,
                    "tname":tname
                },
                success:function (data) {
                    if(data.status == 0){
                        alert("操作成功!");
                        window.location.href = "/index/";
                    }else if(data.status == 1){
                        alert("操作失败！");
                    }
                },
                error:function () {
                    alert("服务器不太给力啊！")
                }
            })
    });
});