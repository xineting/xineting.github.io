---
layout:     post                    # 使用的布局（不需要改）
title:      docker搭建vulhub               # 标题 
subtitle:   docker搭建vulhub		 #副标题
date:       2017-02-06              # 时间
author:     XT                      # 作者
header-img: img/post-bg-2015.jpg    #这篇文章标题背景图片
catalog: true                       # 是否归档
tags:                               #标签
    - 漏洞
---

# docker搭建vulhub
>搭建vulhub

这次我们来介绍两款使用docker进行搭建的集成了各种漏洞的靶机环境：

1. 由Phithon维护的Vulhub

 项目地址：<https://github.com/phith0n/vulhub>

 Vulhub是一个面向大众的开源漏洞靶场，无需Docker知识，简单执行两条命令即可编译、运行一个完整的漏洞靶场镜像。

2. 由 Medicean 维护的Vulapp项目地址：<https://github.com/Medicean/VulApps>

 Vulapp收集各种漏洞环境，为方便使用，统一采用 Dockerfile 形式。同时也收集了安全工具环境。

 下面来介绍下如果用Docker去搭建Vulhub和Vulapps

##  搭建Vulhub

###  准备环境：

 以下在Ubuntu16.04中操作

 1.在ubuntu16.04中安装pip

```
curl -shttps://bootstrap.pypa.io/get-pip.py | python3
```

 

 2.安装docker

```
apt-get update && apt-getinstall docker.io
```

 

 3.启动docker服务

```
service docker start
```

 

 4.安装compose

 

```
pip install docker-compose
```

 

###  拉取vulhub

 由于国内“不可描述的”原因，使用git clone拉取vulhub可能出现各类不可描述的情况。因此建议直接从github上下载项目就好了

 当然，如果你的网络足够稳定的话，也可以使用下面的命令进行拉取。

```
git clone https://github.com/phith0n/vulhub.git
```

 这里以struts环境为例，打开struts2下的s2-016目录

 

```
cd vulhub/struts/s2-016
```

 

###  在线自动化编译docker环境

 

```
docker-compose build
```

 

###  注意：

 docker自身出错的情况，多出现在使用的docker/docker-compose版本较老时出现的BUG，最好使用最新版docker测试vulhub项目。源码编译失败的情况也可能出现，vulhub中的环境全部基于官方镜像编译，官方镜像可能会更新与升级，linux系统升级后可能造成编译上有一定差别，部分老原来就可能编译不成功了。

 如果反复出现编译不了的情况的话，建议使用作者已经编译好并传到dockerhub的镜像：

 <https://hub.docker.com/u/vulhub/>

 使用方法是将docker-compose.yml里build: .替换成image:vulhub/xxxx

###  启动docker环境

 

```
docker-compose up -d
```

 

 这时访问<http://your-ip:8080/link.action>就可以看到环境已经搭建好了。

 *本文原创作者：XXX，本文属FreeBuf原创奖励计划，未经许可禁止转载[![搭建环境](http://image.3001.net/images/20170809/15022539002214.png!small)](http://image.3001.net/images/20170809/15022539002214.png)

 这时再去使用struts2的利用工具就可以愉快的测试漏洞了

 特别需要注意一点的是，vulhub里的漏洞并不是每一个都需要编译的，建议在运行之前到github上去看下关于特定漏洞的配置说明。

##  搭建Vulapp

 对于没有docker基础的新手，建议使用vulapp的在线拉取镜像。如果国内访问速度很慢的话，建议将docker源替换成国内源：

 推荐使用[中科大源](https://lug.ustc.edu.cn/wiki/mirrors/help/docker)，替换方法可以参考中科大的说明文档。

 Vulapp中每一个漏洞的readme.md文档中包含了详细的安装过程只需按照说明去拉取进行并启动环境即可。

 [![启动环境](http://image.3001.net/images/20170809/15022540041518.png!small)](http://image.3001.net/images/20170809/15022540041518.png)

 

 按照使用说明教程搭建了wordpress的phpmailer漏洞复现环境

 [![复现环境](http://image.3001.net/images/20170809/15022540326159.png!small)](http://image.3001.net/images/20170809/15022540326159.png)

##  总结

 虽然这里只是使用了github中开源的漏洞复现环境进行了介绍，但是也给很多新人学习漏洞和渗透测试的一个新的思路。Docker可以说是近两年一个特别火热的话题，它以轻巧、简单、开源著称，对于新人来说，使用docker去快速搭建一个靶机环境进行测试莫过于成本最低的一个方法，然而对于不太熟练docker的新手来说，vulapp和vulhub又是一个极为节省时间且十分高效的一个方案。

 Vulhub和vulapp都是非常不错的一套靶机环境，这两款靶机环境都涵盖了最近一段时间比较流行的漏洞。特别值得一提的是vulapp不仅仅包含了漏洞还包含了漏洞利用的工具，这也给新人搭建环境测试漏洞提供了便利。这里也要给vulhub和vulapp的维护者点个赞，这两套靶机环境的最近更新时间均为半个月之内，同时也涵盖了最近两个月的漏洞，需要感谢他们的开源才使得更多新人能够更快学到更多知识。