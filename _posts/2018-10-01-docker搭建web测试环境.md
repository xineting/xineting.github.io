---
layout:     post
title:      docker搭建Web漏洞渗透测试
subtitle:    docker搭建Web漏洞渗透测试
date:       2018-10-1
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 安全
---


> docker搭建Web漏洞渗透测试

# 使用docker搭建Web漏洞渗透测试环境



靶机环境的部署一直是网安小白头疼的问题，为了解决他们的问题，这里介绍一下使用docker部署Web漏洞包括 bWAPP、DVWA、OWASP WebGoat等，项目已经发布在github上：参照[github地址](https://link.jianshu.com?t=https://github.com/MyKings/docker-vulnerability-environment).
 <h1>Installation</h1>
 <h2>首先拉取你想生成的靶机镜像
 或者到github下载源码进行docker build</h2>
 Docker for Penetration Testing

- [Kali Linux Docker Image](https://link.jianshu.com?t=https://www.kali.org/news/official-kali-linux-docker-images/)
   docker pull kalilinux/kali-linux-docker
- [official OWASP ZAP](https://link.jianshu.com?t=https://github.com/zaproxy/zaproxy)
   docker pull owasp/zap2docker-stable
- [official WPScan](https://link.jianshu.com?t=https://hub.docker.com/r/wpscanteam/wpscan/)
   docker pull wpscanteam/wpscan
- [docker-metasploit](https://link.jianshu.com?t=https://hub.docker.com/r/pandrew/metasploit/)
   docker pull pandrew/metasploit
- [Damn Vulnerable Web Application (DVWA)](https://link.jianshu.com?t=https://hub.docker.com/r/citizenstig/dvwa/)
   docker pull citizenstig/dvwa
- [Vulnerable WordPress Installation](https://link.jianshu.com?t=https://hub.docker.com/r/wpscanteam/vulnerablewordpress/)
   docker pull wpscanteam/vulnerablewordpress
- [Vulnerability as a service: Shellshock](https://link.jianshu.com?t=https://hub.docker.com/r/hmlio/vaas-cve-2014-6271/)
   docker pull hmlio/vaas-cve-2014-6271
- [Vulnerability as a service: Heartbleed](https://link.jianshu.com?t=https://hub.docker.com/r/hmlio/vaas-cve-2014-0160/)
   docker pull hmlio/vaas-cve-2014-0160
- [Security Ninjas](https://link.jianshu.com?t=https://hub.docker.com/r/opendns/security-ninjas/)
   docker pull opendns/security-ninjas
- [Docker Bench for Security](https://link.jianshu.com?t=https://hub.docker.com/r/diogomonica/docker-bench-security/)
   docker pull diogomonica/docker-bench-security
- [OWASP Security Shepherd](https://link.jianshu.com?t=https://hub.docker.com/r/ismisepaul/securityshepherd/)
   docker pull ismisepaul/securityshepherd
- [OWASP WebGoat Project docker image](https://link.jianshu.com?t=https://hub.docker.com/r/danmx/docker-owasp-webgoat/)
   docker pull danmx/docker-owasp-webgoat
- [OWASP NodeGoat](https://link.jianshu.com?t=https://github.com/owasp/nodegoat#option-3---run-nodegoat-on-docker)
   docker-compose build && docker-compose up
- [OWASP Mutillidae II Web Pen-Test Practice Application](https://link.jianshu.com?t=https://hub.docker.com/r/citizenstig/nowasp/)
   docker pull citizenstig/nowasp
- [OWASP Juice Shop](https://link.jianshu.com?t=https://github.com/bkimminich/juice-shop#docker-container--)
   docker pull bkimminich/juice-shop

# 运行靶机容器（使用方法）

各链接中都具有使用方法：

- bWAPP

   

  ![img](https://upload-images.jianshu.io/upload_images/5765738-354cf1f5f057cdf4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/745/format/webp) 

  使用bwApp方法.png

- [xssed](https://link.jianshu.com?t=https://github.com/MyKings/docker-vulnerability-environment/blob/master/xssed/README.md)

- [DVWA](https://link.jianshu.com?t=https://github.com/MyKings/docker-vulnerability-environment/blob/master/DVWA/README.md)

- [WebGoat]([https://github.com/MyKings/docker-vulnerability--](https://link.jianshu.com?t=https://github.com/MyKings/docker-vulnerability--)
   environment/blob/master/WebGoat/README.md)

- [DVWA-WooYun-edition](https://link.jianshu.com?t=https://github.com/MyKings/docker-vulnerability-environment/blob/master/DVWA-WooYun-edition/README.md)

- [DSVW](https://link.jianshu.com?t=https://github.com/MyKings/docker-vulnerability-environment/blob/master/DSVW/README.md)

- [WAVSEP](https://link.jianshu.com?t=https://github.com/MyKings/docker-vulnerability-environment/blob/master/WAVSEP/README.md)

# 小例子

小巧门：先使用docker search <image> 查找当前STARS最多的镜像，这样的话下载速度会提升，而无须下载官方的国外的冷门镜像，如：

![img](https://upload-images.jianshu.io/upload_images/5765738-76b2bb2aae761ae1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

下载速度较快的镜像

 

当然使用方法有可能不尽相同：没事，访问dockerhub上进行查找

![img](https://upload-images.jianshu.io/upload_images/5765738-59433814670f50bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/580/format/webp)

查找当前下载的镜像说明.png

![img](https://upload-images.jianshu.io/upload_images/5765738-4159668047597820.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

了解到当前镜像的用法.png

然后将原来的： docker run -p 1337:80 szsecurity/webgoat
 稍微改变一下：docker run -d --name webgoat  -p 1337:80 szsecurity/webgoat

![img](https://upload-images.jianshu.io/upload_images/5765738-5890da81c41e5dd2.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1000/format/webp)

启动靶机容器

最后访问[http://yourip:1337/WebGoat](https://link.jianshu.com?t=http://yourip:1337/WebGoat)

![img](https://upload-images.jianshu.io/upload_images/5765738-52c54e613c8bed3d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/759/format/webp)

webGoat界面

------

如有不了解的地方，欢迎在评论区留言噢～

参考链接：[https://github.com/enaqx/awesome-pentest](https://link.jianshu.com?t=https://github.com/enaqx/awesome-pentest)

 