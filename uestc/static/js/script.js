/**
 * Created by huangjunqin on 16-6-8.
 */
$(function () {
   $(".header-tab").bind("click",function () {
       $(".header-tab").removeClass("active");
       $(this).addClass("active");
       var index = $(this).index();
       $(".mytab").removeClass("tab-show").eq(index).addClass("tab-show")
   }) 
});