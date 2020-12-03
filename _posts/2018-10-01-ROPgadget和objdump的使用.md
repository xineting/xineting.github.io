---
layout:     post
title:      ROPgadget和objdump
subtitle:   ROPgadget objdump
date:       2018-10-1
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 安全
---


>ROPgadget and objdump命令

# 一、ROPgadget

------

```
ROPgadget --binary b0verfl0w --only 'jmp|ret'
查询包含的语句的地址
➜  X-CTF Quals 2016 - b0verfl0w git:(iromise) ✗ ROPgadget --binary b0verfl0w --only 'jmp|ret'         
Gadgets information
============================================================
0x08048504 : jmp esp
0x0804836a : ret
0x0804847e : ret 0xeac1

Unique gadgets found: 3
```



# 二、objdump
------

**objdump -f test**

显示test的文件头信息


![](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/obj1.png)

**objdump -d test**

反汇编test中的需要执行指令的那些section![](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/obj2.png)



**objdump -D test**

与-d类似，但反汇编test中的所有section

 

**objdump -h test**

显示test的Section Header信息

 

 

**objdump -x test**

显示test的全部Header信息

 

 

**objdump -s test**

除了显示test的全部Header信息，还显示他们对应的十六进制文件代码

 

**举例：**

将C源代码和反汇编出来的指令对照：

1.编译成目标文件（要加-g选项）

**gcc -g -o test.c**

 

2.输出C源代码和反汇编出来的指令对照的格式

**objdump -S test.o**

![](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/obj3.png)