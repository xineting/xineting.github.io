---
layout:     post
title:      在Django 2.2中SQLite3错误
subtitle:    sqlite升级
date:       2019-7-2
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 开发
---


> sqlite

# SQLite3升级



1. 报错信息

   python3 manage.py runserver`启动django项目的时候`

    出现报错信息如下：

   ```
   django.core.exceptions.ImproperlyConfigured: SQLite 3.8.3 or later is required (found 3.7.17).
   ```

2. 查看系统的sqlte3的版本	

   ```
   [root@djangoServer work]# sqlite3 --version 
   3.7.17 2013-05-20 00:56:22 118a3b35693b134d56ebd780123b7fd6f1497668
   [root@djangoServer work]# 
   ```

   果然`Centos`系统自带的`sqlite3`版本偏低，在上面的错误提示中要求需要`SQLite 3.8.3 or later`，那么就需要去升级 `SQlite` 的版本了。

   Centos7安装最新的sqlite3并设置更新python库版本	

   ```shell
   ＃更新SQLite 3
   ＃获取源代码（在主目录中运行）
   [root@djangoServer ~]# cd ~
   [root@djangoServer ~]# wget https://www.sqlite.org/2019/sqlite-autoconf-3270200.tar.gz
   [root@djangoServer ~]# tar -zxvf sqlite-autoconf-3270200.tar.gz
   
   ＃构建并安装
   [root@djangoServer ~]# cd sqlite-autoconf-3270200
   [root@djangoServer sqlite-autoconf-3270200]# ./configure --prefix=/usr/local
   [root@djangoServer sqlite-autoconf-3270200]# make && make install
   [root@djangoServer sqlite-autoconf-3270200]# find /usr/ -name sqlite3
   /usr/bin/sqlite3
   /usr/lib64/python2.7/sqlite3
   /usr/local/bin/sqlite3
   /usr/local/python3/lib/python3.7/site-packages/django/db/backends/sqlite3
   /usr/local/python3/lib/python3.7/sqlite3
   [root@djangoServer sqlite-autoconf-3270200]# 
   
   ＃不必要的文件，目录删除
   [root@djangoServer sqlite-autoconf-3270200]# cd ~
   [root@djangoServer ~]# ls
   anaconda-ks.cfg  sqlite-autoconf-3270200  sqlite-autoconf-3270200.tar.gz
   [root@djangoServer ~]# 
   [root@djangoServer ~]# rm -rf sqlite-autoconf-3270200.tar.gz
   [root@djangoServer ~]# rm -rf sqlite-autoconf-3270200
   
   ＃检查版本
   ## 最新安装的sqlite3版本
   [root@djangoServer ~]# /usr/local/bin/sqlite3 --version
   3.27.2 2019-02-25 16:06:06 bd49a8271d650fa89e446b42e513b595a717b9212c91dd384aab871fc1d0f6d7
   [root@djangoServer ~]# 
   
   ## Centos7自带的sqlite3版本
   [root@djangoServer ~]# /usr/bin/sqlite3 --version
   3.7.17 2013-05-20 00:56:22 118a3b35693b134d56ebd780123b7fd6f1497668
   [root@djangoServer ~]# 
   
   ## 可以看到sqlite3的版本还是旧版本，那么需要更新一下。
   [root@djangoServer ~]# sqlite3 --version
   3.7.17 2013-05-20 00:56:22 118a3b35693b134d56ebd780123b7fd6f1497668
   [root@djangoServer ~]# 
   
   ## 更改旧的sqlite3
   [root@djangoServer ~]# mv /usr/bin/sqlite3  /usr/bin/sqlite3_old
   
   ## 软链接将新的sqlite3设置到/usr/bin目录下
   [root@djangoServer ~]# ln -s /usr/local/bin/sqlite3   /usr/bin/sqlite3
   
   ## 查看当前全局sqlite3的版本
   [root@djangoServer ~]# sqlite3 --version
   3.27.2 2019-02-25 16:06:06 bd49a8271d650fa89e446b42e513b595a717b9212c91dd384aab871fc1d0f6d7
   [root@djangoServer ~]# 
   
   ＃将路径传递给共享库
   # 设置开机自启动执行，可以将下面的export语句写入 ~/.bashrc 文件中，如果如果你想立即生效，可以执行source 〜/.bashrc 将在每次启动终端时执行
   [root@djangoServer ~]# export LD_LIBRARY_PATH="/usr/local/lib"
   
   ＃检查Python的SQLite3版本
   [root@djangoServer ~]# ipython3
   Python 3.7.1 (default, May  3 2019, 09:55:04) 
   Type 'copyright', 'credits' or 'license' for more information
   IPython 7.5.0 -- An enhanced Interactive Python. Type '?' for help.
   
   In [1]: import sqlite3                                                     
   
   In [2]: sqlite3.sqlite_version                                             
   Out[2]: '3.27.2'
   
   In [3]: exit                                                               
   [root@djangoServer ~]# 
   
   ＃启动开发服务器
   [root@djangoServer ~]# cd /work/
   [root@djangoServer work]# ls
   db.sqlite3  manage.py  polls  test_django
   [root@djangoServer work]# python3 manage.py runserver
   Watching for file changes with StatReloader
   Performing system checks...
   
   System check identified no issues (0 silenced).
   May 03, 2019 - 21:32:28
   Django version 2.2.1, using settings 'test_django.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```

