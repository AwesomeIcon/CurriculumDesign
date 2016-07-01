# 课程设计：选课系统实现

## 准备工作

* PyCharm

* git

* mysql

### 环境安装

* django 1.9.6

```bash
pip install django==1.9.6
```

* python 2.7

### 用到的python库：

* simplejson

* MySQLdb

## 需求分析

实现一个单机选课系统，
通过windows图形界面进行基本的选课操作（需要考虑并发情况）并且纪录所有日志，能在选课系统上进行数据库的监控（并发量比较大的时候的系统运行情况以及系统操作的Log设计），
能使用系统正常进行选课，以及能展示选课的Log

