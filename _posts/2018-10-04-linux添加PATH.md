---
layout:     post
title:      linux添加path
subtitle:    linux添加path
date:       2018-10-4
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 运维
---


> linux添加path

# linux 添加环境变量 $PATH

```
$PATH：决定了shell将到哪些目录中寻找命令或程序，PATH的值是一系列目录，当您运行一个程序时，Linux在这些目录下进行搜寻编译链接。
　　编辑你的 PATH 声明，其格式为：
　　PATH=$PATH:<PATH1>:<PATH2>:<PATH3>:------:<PATHN>
　　你可以自己加上指定的路径，中间用冒号隔开。环境变量更改后，在用户下次登陆时生效，如果想立刻生效而免去重新启动，则可执行下面的语句：
         $source   /etc/profile
　　需要注意的是，最好不要把当前路径 “./” 放到 PATH 里，这样可能会受到意想不到的攻击。这样定制后，就可以避免频繁的启动位于 shell 搜索的路径之外的程序了。
单独查看PATH环境变量，可用：
 echo $PATH

添加PATH环境变量，可用：
sudo exportPATH=/home/tuotu/bin:$PATH
再次查看：
 echo $PATH
/home/tuotu/bin:/usr/bin:usr/sbin……
/home/tuotu/bin目录已经添加成功。
上述方法的PATH 在终端关闭后就会消失。所以还是建议通过编辑/etc/profile来改PATH，也可以改家目录下的.bashrc(即：~/.bashrc)。

第二种方法：
sudo vim/etc/profile
在文档最后，添加:
export PATH="/home/tuotu/bin:$PATH"
保存，退出，然后运行：
#source   /etc/profile
即可

---------------------

本文来自 温柔的大白鹅 的CSDN 博客 ，全文地址请点击：https://blog.csdn.net/kevinhanser/article/details/79352109?utm_source=copy 
```

