# -*-coding:utf8-*-
import simplejson as simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response
import hashlib
from django.db import connection
from models import *
# Create your views here.


def login(request):
    return render_to_response('login.html')


def user_login(request):
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        passwd = md5(request.POST['passwd'])
        try:
            Student.objects.get(uid=username, upasswd=passwd)
            data = simplejson.dumps({"status": 0})
            return HttpResponse(data, content_type="application/json")
        except:
            data = simplejson.dumps({"status": 1})
            return HttpResponse(data, content_type="application/json")


def index(request):
    return render_to_response('index.html')


def get_course(request):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("select cid,cname,tname,ccredit,cclass from subject_course,subject_teacher where subject_course.tid_id = subject_teacher.tid")
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def get_log(request):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("select subject_course.cid,cname,operate,subject_student.uid,ip,logtime from subject_course,subject_student,subject_recordlog where subject_student.uid = subject_recordlog.uid_id AND subject_course.id = subject_recordlog.cid_id")
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def get_already_choose(request):
    if request.method == "GET":
        cursor = connection.cursor()
        cursor.execute("select cid,cname,tname,ccredit,cclass,weight from subject_csinfo,subject_course,subject_teacher,subject_student WHERE subject_student.uid = subject_csinfo.uid_id AND subject_teacher.tid = subject_csinfo.tid_id AND subject_course.id = subject_csinfo.cid_id")
        query_set = simplejson.dumps(cursor.fetchall())
        cursor.close()
        return HttpResponse(query_set, content_type="application/json")


def md5(obj):
    m = hashlib.md5()
    m.update(obj)
    return m.hexdigest()
