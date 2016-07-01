/**
 * Created by huangjunqin on 16-6-8.
 */
avalon.config({
    interpolate: ["{&", "&}"]
});

$(function () {
    var choose = avalon.define({
        $id:"chooseModel",
        data:[]
    });
    $.getJSON('/choose/',null,function (data) {
         choose.data = data;
    });
    var course = avalon.define({
        $id:"courseModel",
        data:[]
    });
    $.getJSON('/course/',null,function (data) {
        course.data = data;
    });
    var log = avalon.define({
        $id:"logModel",
        data:[]
    });
    $.getJSON('/log/',null,function (data) {
        log.data = data; 
    });
   $(".header-tab").bind("click",function () {
       $(".header-tab").removeClass("active");
       $(this).addClass("active");
       var index = $(this).index();
       $(".mytab").removeClass("tab-show").eq(index).addClass("tab-show")
   }) 
});