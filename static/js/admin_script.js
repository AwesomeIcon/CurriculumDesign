/**
 * Created by huangjunqin on 16-6-8.
 */
avalon.config({
    interpolate: ["{&", "&}"]
});

$(function () {
    //已有课程
    var course = avalon.define({
        $id:"existCourseModel",
        data:[]
    });
    $.getJSON('/admin/get/course/',null,function (data) {
         course.data = data;
    });
    //已有学生账号
    var student = avalon.define({
        $id:"existStudentModel",
        data:[]
    });
    $.getJSON('/admin/get/student/',null,function (data) {
        student.data = data;
    });
    //已有老师账号
    var teacher = avalon.define({
        $id:"existTeacherModel",
        data:[]
    });
    $.getJSON('/admin/get/teacher/',null,function (data) {
        teacher.data = data; 
    });
    //选项卡效果
   $(".header-tab").bind("click",function () {
       $(".header-tab").removeClass("active");
       $(this).addClass("active");
       var index = $(this).index();
       $(".mytab").removeClass("tab-show").eq(index).addClass("tab-show")
   });
    //删除课程操作
    $(document).on("click",".delete_course",function () {
        var that = $(this);
        var cid = that.parent().parent().find("th").eq(0).text();
        var tname = that.parent().parent().find("td").eq(1).text();
            $.ajax({
                url:"/admin/delete/course/",
                type:"POST",
                dataType:"json",
                data:{
                    "cid":cid,
                    "tname":tname,
                },
                success:function (data) {
                    if(data.status == 0){
                        alert("操作成功!");
                        window.location.href = "/admin/index/";
                    }else if(data.status == 1){
                        alert("操作失败！");
                    }
                },
                error:function () {
                    alert("服务器不太给力啊！")
                }
            })
    });
    //增加课程操作
    $(document).on("click",".add_course",function () {
        var that = $(this);
        var cid = that.parent().parent().find("th").eq(0).find("input").val();
        var cname = that.parent().parent().find("td").eq(0).find("input").val();
        var credit = that.parent().parent().find("td").eq(3).find("input").val();
        var cclass = that.parent().parent().find("td").eq(4).find("input").val();
        var tid = that.parent().parent().find("td").eq(2).find("input").val();
        if(cid != "" && cname != "" && credit != "" && cclass != "" && tid != ""){
            $.ajax({
                url:"/admin/add/course/",
                type:"POST",
                dataType:"json",
                data:{
                    "cid":cid,
                    "cname":cname,
                    "credit":credit,
                    "cclass":cclass,
                    "tid":tid
                },
                success:function (data) {
                    if(data.status == 0){
                        alert("操作成功!");
                        window.location.href = "/admin/index/";
                    }else if(data.status == 1){
                        alert("请先添加该任课老师！");
                    }
                },
                error:function () {
                    alert("服务器不太给力啊！")
                }
            })
        }
    });
    //增加学生操作
    $(document).on("click",".add_student",function () {
        var that = $(this);
        var uid = that.parent().parent().find("th").eq(0).find("input").val();
        var uname = that.parent().parent().find("td").eq(0).find("input").val();
        var usex = that.parent().parent().find("td").eq(1).find("input").val();
        if(uid != "" && uname != "" && usex != ""){
            $.ajax({
            url:"/admin/add/student/",
            type:"POST",
            dataType:"json",
            data:{
                "uid":uid,
                "uname":uname,
                "usex":usex
            },
            success:function (data) {
                if(data.status == 0){
                    alert("添加成功！");
                    window.location.href = "/admin/index/";
                }else if(data.status == 1){
                    alert("添加失败!");
                }
            }, 
            error:function () {
                alert("服务器不太给力啊！");
            }
        })
        }else{
            alert("请先完善学生信息！");
        }
    });
    //重置密码
    $(document).on("click",".reset_passwd",function () {
        var that = $(this);
        var uid = that.parent().parent().find("th").eq(0).text();
        $.ajax({
            url:"/admin/resetPassword/",
            dataType:"json",
            type:"POST",
            data:{
                "uid":uid
            },
            success:function (data) {
                if(data.status == 0){
                    alert("密码重置成功！");
                }else if(data.status == 1){
                    alert("重置失败！");
                }
            },
            error:function () {
                alert("服务器不太给力啊！");
            }
        })
    });
    //删除老师
    $(document).on("click",".delete_teacher",function () {
        var that = $(this);
        var tid = that.parent().parent().find("th").eq(0).text();
        $.ajax({
            url:"/admin/delete/teacher/",
            dataType:"json",
            type:"POST",
            data:{
                "tid":tid
            },
            success:function (data) {
                if(data.status == 0){
                    alert("操作成功！");
                    window.location.href = "/admin/index/";
                }else{
                    alert("删除失败！");
                }
            },
            error:function () {
                alert("服务器不太给力啊！");
            }
        })
    });
    //添加老师
    $(document).on("click",".add_teacher",function () {
        var that = $(this);
        var tid = that.parent().parent().find("th").eq(0).find("input").val();
        var tname = that.parent().parent().find("td").eq(0).find("input").val();
        var tsex = that.parent().parent().find("td").eq(1).find("input").val();
        var ttitle = that.parent().parent().find("td").eq(2).find("input").val();
        if(tid != "" && tname != "" && tsex != "" && ttitle != ""){
            $.ajax({
            url:"/admin/add/teacher/",
            type:"POST",
            dataType:"json",
            data:{
                "tid":tid,
                "tname":tname,
                "tsex":tsex,
                "ttitle":ttitle
            },
            success:function (data) {
                if(data.status == 0){
                    alert("添加成功！");
                    window.location.href = "/admin/index/";
                }else if(data.status == 1){
                    alert("添加失败!");
                }
            },
            error:function () {
                alert("服务器不太给力啊！");
            }
        })
        }else{
            alert("请先完善老师信息！");
        }
    });
});