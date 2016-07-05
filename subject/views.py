# -*-coding:utf8-*-
import simplejson as simplejson
import time
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import hashlib
from django.db import connection
from models import *
# Create your views here.


def login(request):
    return render_to_response('login.html')


def admin_login(request):
    return render_to_response('admin_login.html')


def logout(request):
    response = HttpResponseRedirect("/")
    response.delete_cookie('username')
    return response


def user_login(request):
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        passwd = md5(request.POST['passwd'])
        stu = Student.objects.filter(uid=username, upasswd=passwd)
        if stu:
            data = simplejson.dumps({"status": 0})
            response = HttpResponse(data, content_type="application/json")
            response.set_cookie('username', username, 3600)
            return response
        else:
            data = simplejson.dumps({"status": 1})
            return HttpResponse(data, content_type="application/json")


def admin_index(request):
    try:
        username = request.COOKIES.get('username')
        stu = Student.objects.get(uid=username).uname
        return render_to_response('admin_index.html', {"id": username, "name": stu})
    except:
        return HttpResponseRedirect('/admin/')


def index(request):
    try:
        username = request.COOKIES.get('username')
        stu = Student.objects.get(uid=username).uname
        cursor = connection.cursor()
        cursor.execute("select sum(weight) from subject_csinfo WHERE uid_id=" + username)
        query_set = cursor.fetchone()[0]
        cursor.close()
        if query_set is None:
            query_set = 0
        return render_to_response('index.html', {"id": username, "name": stu, "weight": 100-query_set})
    except:
        return HttpResponseRedirect('/')


def get_course(request):
    if request.method == "GET":
        username = request.COOKIES.get('username')
        cursor = connection.cursor()
        cursor.execute("select cid,cname,tname,ccredit,cclass from subject_course,subject_teacher where subject_course.tid_id = subject_teacher.tid AND tid NOT IN (SELECT tid_id FROM subject_csinfo WHERE uid_id = " + username + ")")
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def select_course(request):
    if request.method == "POST" and request.is_ajax():
        username = request.COOKIES.get('username')
        cid = request.POST['cid']
        tname = request.POST['tname']
        weight = request.POST['weight']
        try:
            cursor = connection.cursor()
            cursor.execute("select tid FROM subject_course,subject_teacher WHERE subject_course.tid_id=subject_teacher.tid AND subject_teacher.tname='" + tname + "' and subject_course.cid=" + cid)
            tid = cursor.fetchone()[0]
            cursor.execute("select id FROM subject_course where cid=" + cid + " and tid_id=" + tid)
            cid = cursor.fetchone()[0]
            cursor.close()
            csinfo = CSINFO(uid_id=username, tid_id=tid, cid_id=cid, weight=weight)
            csinfo.save()
            nowdate = time.strftime('%Y-%m-%d', time.localtime())
            recordlog = RecordLog(operate='选课', ip=get_client_ip(request), logtime=nowdate, cid_id=cid, uid_id=username)
            recordlog.save()
            data = simplejson.dumps({"status": 0})
            return HttpResponse(data, content_type="application/json")
        except:
            data = simplejson.dumps({"status": 1})
            return HttpResponse(data, content_type="application/json")


def list_course(request):
    if request.method == "GET" and request.COOKIES.get('username') == 'admin':
        cursor = connection.cursor()
        cursor.execute(
            "select cid,cname,tname,ccredit,cclass from subject_course,subject_teacher where subject_course.tid_id = subject_teacher.tid")
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def list_student(request):
    if request.method == "GET" and request.COOKIES.get('username') == 'admin':
        cursor = connection.cursor()
        cursor.execute(
            "select uid,uname,usex from subject_student where uid != 'admin'")
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def list_teacher(request):
    if request.method == "GET" and request.COOKIES.get('username') == 'admin':
        cursor = connection.cursor()
        cursor.execute(
            "select tid,tname,tsex,ttitle from subject_teacher")
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def cancel_course(request):
    if request.method == "POST" and request.is_ajax():
        username = request.COOKIES.get('username')
        cid = request.POST['cid']
        tname = request.POST['tname']
        cursor = connection.cursor()
        cursor.execute("select tid FROM subject_course,subject_teacher WHERE subject_course.tid_id=subject_teacher.tid AND subject_teacher.tname='" + tname + "' and subject_course.cid=" + cid)
        tid = cursor.fetchone()[0]
        cursor.execute("select id FROM subject_course where cid=" + cid + " and tid_id=" + tid)
        cid = cursor.fetchone()[0]
        cursor.close()
        try:
            csinfo = CSINFO.objects.get(uid_id=username, tid_id=tid, cid_id=cid)
            csinfo.delete()
            nowdate = time.strftime('%Y-%m-%d', time.localtime())
            recordlog = RecordLog(operate='退课', ip=get_client_ip(request), logtime=nowdate, cid_id=cid, uid_id=username)
            recordlog.save()
            data = simplejson.dumps({"status": 0})
        except:
            data = simplejson.dumps({"status": 1})
        return HttpResponse(data, content_type="application/json")


def get_log(request):
    if request.method == "GET":
        username = request.COOKIES.get('username')
        cursor = connection.cursor()
        cursor.execute("select subject_course.cid,cname,operate,subject_student.uid,ip,logtime from subject_course,subject_student,subject_recordlog where subject_student.uid = subject_recordlog.uid_id AND subject_course.id = subject_recordlog.cid_id AND subject_student.uid = " + username)
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def get_already_choose(request):
    if request.method == "GET":
        username = request.COOKIES.get('username')
        cursor = connection.cursor()
        cursor.execute("select cid,cname,tname,ccredit,cclass,weight from subject_csinfo,subject_course,subject_teacher,subject_student WHERE subject_student.uid = subject_csinfo.uid_id AND subject_teacher.tid = subject_csinfo.tid_id AND subject_course.id = subject_csinfo.cid_id AND subject_student.uid = " + username)
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def md5(obj):
    m = hashlib.md5()
    m.update(obj)
    return m.hexdigest()


def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = "unknow"
    return regip


def delete_course(request):
    if request.method == 'POST' and request.COOKIES.get('username') == 'admin' and request.is_ajax():
        cid = request.POST['cid']
        tname = request.POST['tname']
        cursor = connection.cursor()
        cursor.execute(
            "select tid FROM subject_course,subject_teacher WHERE subject_course.tid_id=subject_teacher.tid AND subject_teacher.tname='" + tname + "' and subject_course.cid=" + cid)
        tid = cursor.fetchone()[0]
        cursor.close()
        course = Course.objects.get(cid=cid, tid_id=tid)
        course.delete()
        data = simplejson.dumps({"status": 0})
        return HttpResponse(data, content_type="application/json")


def add_course(request):
    if request.method == 'POST' and request.COOKIES.get('username') == 'admin' and request.is_ajax():
        cid = request.POST['cid']
        cname = request.POST['cname']
        credit = request.POST['credit']
        cclass = request.POST['cclass']
        tid = request.POST['tid']
        teacher = Teacher.objects.filter(tid=tid)
        if teacher:
            course = Course(cid=cid, cname=cname, ccredit=credit, cclass=cclass, tid_id=tid)
            course.save()
            data = simplejson.dumps({"status": 0})
        else:
            data = simplejson.dumps({"status": 1})
        return HttpResponse(data, content_type="application/json")


def add_student(request):
    if request.method == 'POST' and request.COOKIES.get('username') == 'admin' and request.is_ajax():
        uid = request.POST['uid']
        uname = request.POST['uname']
        usex = request.POST['usex']
        stu = Student(uid=uid, uname=uname, usex=usex, upasswd=md5('123456'))
        try:
            stu.save()
            data = simplejson.dumps({"status": 0})
        except:
            data = simplejson.dumps({"status": 1})
        return HttpResponse(data, content_type="application/json")


def reset_passwd(request):
    if request.method == 'POST' and request.COOKIES.get('username') == 'admin' and request.is_ajax():
        uid = request.POST['uid']
        stu = Student.objects.get(uid=uid)
        try:
            stu.upasswd = md5("123456")
            stu.save()
            data = simplejson.dumps({"status": 0})
        except:
            data = simplejson.dumps({"status": 1})
        return HttpResponse(data, content_type="application/json")


def delete_teacher(request):
    if request.method == 'POST' and request.COOKIES.get('username') == 'admin' and request.is_ajax():
        tid = request.POST['tid']
        teacher = Teacher.objects.get(tid=tid)
        teacher.delete()
        data = simplejson.dumps({"status": 0})
        return HttpResponse(data, content_type="application/json")


def add_teacher(request):
    if request.method == 'POST' and request.COOKIES.get('username') == 'admin' and request.is_ajax():
        tid = request.POST['tid']
        tname = request.POST['tname']
        tsex = request.POST['tsex']
        ttitle = request.POST['ttitle']
        teacher = Teacher(tid=tid, tname=tname, tsex=tsex, ttitle=ttitle)
        try:
            teacher.save()
            data = simplejson.dumps({"status": 0})
        except:
            data = simplejson.dumps({"status": 1})
        return HttpResponse(data, content_type="application/json")