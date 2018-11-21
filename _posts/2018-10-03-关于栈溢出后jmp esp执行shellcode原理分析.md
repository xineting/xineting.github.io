---
layout:     post                    # 使用的布局（不需要改）
title:      jmp esp执行shellcode原理分析               # 标题 
subtitle:   jmp esp执行shellcode原理分析  #副标题
date:       2018-10-03             # 时间
author:     XT                      # 作者
header-img: img/post-bg-alibaba.jpg    #这篇文章标题背景图片
catalog: true                       # 是否归档
tags:                               #标签
    - pwn
---

# jmp esp执行shellcode原理分析 
>这是jmp esp执行shellcode原理分析 



1. 网上关于栈溢出后用jmp esp执行shellcode的文章有很多，感觉分析的都没有戳到点，所以想结合自己调试的经历写下自己的想法。

   正常情况下，函数栈分布图如下:

   ```
   ---->栈内存由低向高方向----->
   |------------栈变量----------|----ebp----|------返回地址------|函数形参|
   ```

    

   ```
   ---->栈内存由低向高方向----->
   |------------x90x90x90x90x90|x90x90x90..|shellcode缓存区的地址|x90x90.|
   ```

   就像写代码时用绝对路径读取配置文件的内容，偶尔会出错一样，为了解决这种错误，可能会用相对程序运行时的路径去获取配置文件的内容。硬编码shellcode的地址也会出错，于是先人提出一种相对定位shellcode地址的方法，这就是jmp esp。

   这用到了栈指针esp的一个特性：当函数执行ret指令后，Eip寄存器发生了跳转，但Esp还指向函数形参在栈中的地址。如示意图：

   ret返回前 esp的位置:

   ![1542778527338](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/1542778527338.png)

   跳转后，执行的位置确定了，剩下的问题就是寻找用户可访问空间中，哪段内存地址包含了jmp esp这样的指令。于是OD可能提供了这样的插件，用于寻找这样的地址，比如找到0x00ABCDEF这个地址上包含了jmp esp指令。于是，栈溢出后，在返回地址处填入0x00ABCDEF。当被溢出的函数执行ret指令时，首先会跳转到0x00ABCDEF处取指执行。取到的结果是jmp esp，于是Eip被设置成Esp的值---即上图中本是存放函数形参，现在被shellcode覆盖的栈内存处继续执行
