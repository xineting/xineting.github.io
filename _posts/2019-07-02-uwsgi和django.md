---
layout:     post
title:      nginx、uwsgi和django
subtitle:    centos从入坑到入坟
date:       2019-7-2
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 开发
---


>  django，uwsgi，nginx三者搭建

## python3安装

先安装python3，这个在前篇文章有提过，这里省去了

```shell
pip install uwsgi
uwsgi --version    # 查看 uwsgi 版本
```



## uwsgi安装

我们使用pip安装，或者pip3安装，可能安装后我们的uwsgi并不在/usr/bin中

我们可以使用

```shell
find / -name uwsgi
```

查询到uwsgi并把它关联到/usr/bin目录下

```shell
ln -s /opt/python3.5/bin/uwsgi /usr/bin/uwsgi
```

测试 uwsgi 是否正常：

新建 test.py 文件，内容如下：

```python
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello World"
```

然后在终端运行：

```shell
uwsgi --http :8001 --wsgi-file test.py
```

然后访问本地8001端口。看看有没有内容输出。



## 安装django

```shell
pip install django
```

依旧需要关联，我怀疑这可能是我python安装的问题

```SHELL
ln -s /opt/python3.5/bin/django-admin /usr/bin/django-admin
```



## 安装nginx

我是直接yum install nginx安装的

不过配置，着实让我崩溃了一波



## uwsgi 配置

我们project的目录如图

```shell
[root@localhost wzx]# ls
helloworld  
```

我们新建一个文件夹

```shell
mkdir script
```

这个文件夹来放我们的uwsgi的配置文件

```shell
[root@localhost wzx]# cd script/
[root@localhost script]# vi uwsgi.ini 
```

进入vim页面后

```

[uwsgi]
socket = 0.0.0.0:9000   #这个是通过socket传给nginx的数据
http = 0.0.0.0:8080     #这个参数可以直接通过8080访问到我们的django目录
chdir = /home/wzx/helloworld  #project的目录
module = helloworld.wsgi:application   #wsgi的位置
master = true             
daemonize = uwsgi.log      #日志
socket = /home/wzx/script/uwsgi.sock        #这个跟上边的socket按道理可以只留一个，
aemonize = /home/wzx/script/uwsgi.log
static-map=/static=/home/wzx/helloworld/static #静态访问
process = 3
uid=root
gid=root
vacuum =true
```

这个错测测，不一定什么时候就成功了，网上的答案天花乱坠，看到头晕，这里的参数http那个最容易测出来，然后改测socket，然后配置nginx的conf，就可以访问了。



## nginx配置

[root@localhost script]# vim /etc/nginx/conf.d/default.conf 

```nginx
server {
    listen       80;
    listen      [::]:80;
    server_name 127.0.0.1 192.168.203.140;

    location / {
        include /etc/nginx/uwsgi_params;
        uwsgi_pass 127.0.0.1:9000;
        uwsgi_param UWSGI_SCRIPT helloworld.wsgi;
        uwsgi_param UWSGI_CHDIR  /home/wzx/helloworld;
        index index.html index.htm;
        client_max_body_size 35m;
    }
    location /static/ {
        alias /home/wzx/helloworld/static/;
        index index.html index.htm;
    }

}
```

这里最主要的是就是uwsgi_pass代表的socket（跟上边的一致），uwsgi_param UWSGI_SCRIPT，uwsgi_param UWSGI_CHDIR（享目根目录），这三个的正确性了。

之后

```shell
uwsgi --ini /home/wzx/script/uwsgi.ini & nginx
```

访问127.0.0.1就可以看到我们的项目了！