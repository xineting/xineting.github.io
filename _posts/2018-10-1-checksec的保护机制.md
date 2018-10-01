---
layout:     post
title:      checksec的保护机制
subtitle:   checksec的保护机制
date:       2018-10-1
author:     XT
header-img: img/post-bg-map.jpg
catalog: 	 true
tags:
    - Pwn
---


>checksec的保护机制

# checksec的保护机制



今天在研究liunx下栈溢出的时候发现自己对各种保护机制并不是特别了解，因此就这方面的知识在网上查找了一些资料并总结了一些心得和大家分享。

操作系统提供了许多安全机制来尝试降低或阻止缓冲区溢出攻击带来的安全风险，包括DEP、ASLR等。在编写漏洞利用代码的时候，需要特别注意目标进程是否开启了DEP（Linux下对应NX）、ASLR（Linux下对应PIE）等机制，例如存在DEP（NX）的话就不能直接执行栈上的数据，存在ASLR的话各个系统调用的地址就是随机化的。

**一、checksec：**

checksec是一个脚本软件，也就是用脚本写的一个文件，不到2000行，可用来学习shell。

源码参见

[http://www.trapkit.de/tools/checksec.html](https://link.jianshu.com?t=http%3A%2F%2Fwww.trapkit.de%2Ftools%2Fchecksec.html)

[https://github.com/slimm609/checksec.sh/](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fslimm609%2Fchecksec.sh%2F)

下载方法之一为

wget [https://github.com/slimm609/checksec.sh/archive/1.6.tar.gz](https://link.jianshu.com?t=https%3A%2F%2Fgithub.com%2Fslimm609%2Fchecksec.sh%2Farchive%2F1.6.tar.gz)

checksec到底是用来干什么的？

它是用来检查可执行文件属性，例如PIE, RELRO, PaX, Canaries, ASLR, Fortify Source等等属性。

checksec的使用方法：

![img](https://upload-images.jianshu.io/upload_images/1731834-2f42b018c1221828?imageMogr2/auto-orient/strip%7CimageView2/2/w/530/format/webp)

checksec –file /usr/sbin/sshd

![img](https://upload-images.jianshu.io/upload_images/1731834-671f3d35f355b786?imageMogr2/auto-orient/strip%7CimageView2/2/w/844/format/webp)

一般来说，如果是学习二进制漏洞利用的朋友，建议大家使用gdb里peda插件里自带的checksec功能，如下：

下面我们就图中各个保护机制进行一个大致的了解。

**二、CANNARY(栈保护)**

这个选项表示栈保护功能有没有开启。

栈溢出保护是一种缓冲区溢出攻击缓解手段，当函数存在缓冲区溢出攻击漏洞时，攻击者可以覆盖栈上的返回地址来让shellcode能够得到执行。当启用栈保护后，函数开始执行的时候会先往栈里插入cookie信息，当函数真正返回的时候会验证cookie信息是否合法，如果不合法就停止程序运行。攻击者在覆盖返回地址的时候往往也会将cookie信息给覆盖掉，导致栈保护检查失败而阻止shellcode的执行。在Linux中我们将cookie信息称为canary。

gcc在4.2版本中添加了-fstack-protector和-fstack-protector-all编译参数以支持栈保护功能，4.9新增了-fstack-protector-strong编译参数让保护的范围更广。

因此在编译时可以控制是否开启栈保护以及程度，例如：

gcc -fno-stack-protector -o test test.c  //禁用栈保护

gcc -fstack-protector -o test test.c   //启用堆栈保护，不过只为局部变量中含有 char 数组的函数插入保护代码

gcc -fstack-protector-all -o test test.c //启用堆栈保护，为所有函数插入保护代码

**三、FORTIFY**

这个保护机制查了很久都没有个很好的汉语形容，根据我的理解它其实和栈保护都是gcc的新的为了增强保护的一种机制，防止缓冲区溢出攻击。由于并不是太常见，也没有太多的了解。

举个例子可能简单明了一些：

一段简单的存在缓冲区溢出的C代码

void fun(char *s) {

​        char buf[0x100];

​        strcpy(buf, s);

​        /* Don't allow gcc to optimise away the buf */

​        asm volatile("" :: "m" (buf));

}

用包含参数-U_FORTIFY_SOURCE编译

08048450 :

  push   %ebp               ;

  mov    %esp,%ebp

  sub    $0x118,%esp        ; 将0x118存储到栈上

  mov    0x8(%ebp),%eax     ; 将目标参数载入eax

  mov    %eax,0x4(%esp)     ; 保存目标参数

  lea    -0x108(%ebp),%eax  ; 数组buf

  mov    %eax,(%esp)        ; 保存

  call   8048320

  leave                     ;

  ret

用包含参数-D_FORTIFY_SOURCE=2编译

08048470 :

  push   %ebp               ;

  mov    %esp,%ebp

  sub    $0x118,%esp        ;

  movl   $0x100,0x8(%esp)   ; 把0x100当作目标参数保存

  mov    0x8(%ebp),%eax     ;

  mov    %eax,0x4(%esp)     ;

  lea    -0x108(%ebp),%eax  ;

  mov    %eax,(%esp)        ;

  call   8048370 <__strcpy_chk@plt>

  leave                      ;

  ret

我们可以看到gcc生成了一些附加代码，通过对数组大小的判断替换strcpy, memcpy, memset等函数名，达到防止缓冲区溢出的作用。

**四、NX（DEP）**

NX即No-eXecute（不可执行）的意思，NX（DEP）的基本原理是将数据所在内存页标识为不可执行，当程序溢出成功转入shellcode时，程序会尝试在数据页面上执行指令，此时CPU就会抛出异常，而不是去执行恶意指令。

工作原理如图：

![img](https://upload-images.jianshu.io/upload_images/1731834-9fd297e93278f44d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/577/format/webp)

gcc编译器默认开启了NX选项，如果需要关闭NX选项，可以给gcc编译器添加-z execstack参数。

例如：

gcc -z execstack -o test test.c

在Windows下，类似的概念为DEP（数据执行保护），在最新版的Visual Studio中默认开启了DEP编译选项。

**五、PIE（ASLR）**

一般情况下NX（Windows平台上称其为DEP）和地址空间分布随机化（ASLR）会同时工作。

内存地址随机化机制（address space layout randomization)，有以下三种情况

0 - 表示关闭进程地址空间随机化。

1 - 表示将mmap的基址，stack和vdso页面随机化。

2 - 表示在1的基础上增加栈（heap）的随机化。

可以防范基于Ret2libc方式的针对DEP的攻击。ASLR和DEP配合使用，能有效阻止攻击者在堆栈上运行恶意代码。

Built as PIE：位置独立的可执行区域（position-independent executables）。这样使得在利用缓冲溢出和移动操作系统中存在的其他内存崩溃缺陷时采用面向返回的编程（return-oriented programming）方法变得难得多。

liunx下关闭PIE的命令如下：

sudo -s echo 0 > /proc/sys/kernel/randomize_va_space

**六、RELRO**

设置符号重定向表格为只读或在程序启动时就解析并绑定所有动态符号，从而减少对GOT（Global Offset Table）攻击。RELRO为” Partial RELRO”，说明我们对GOT表具有写权限。

 

 

 

 

 