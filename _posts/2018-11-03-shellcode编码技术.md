---
layout:     post
title:      shellcode编码技术
subtitle:    shellcode编码技术
date:       2018-11-3
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - pwn
    - shellcode
---


> shellcode编码技术

# shellcode编码技术



## 位置代码无关性技术

* 定义：位置无关代码（PIC）是指不使用硬编码地址来寻址指令或数据的代码

* 必要性：因为Shellcode被加载到内存地址执行时，指令的内存地址是不确定的，比如一个有漏洞的程序的不同版本会加载shellcode到不同的内存位置，因此需要要求shellcode是位置无关的代码

  

  第1条汇编指令中call指令包含一个32位有符号的偏移值，通过指令在内存中的地址加上该偏移值，是位置无关代码

  第3条汇编指令中mov指令访问了一个固定的内存地址dword_407030 ，不是位置无关代码

  ![1541215556868](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/shellcode.png)

## 如何获取shellcode起始位置

* Shellcode在以位置无关方式访问时，首先需要引用一个基址指针，用该基址指针加上或减去一定的偏移，从而顺利的访问shellcode中包含的数据。

* Shellcode在以位置无关的方式访问指令和数据时，通常是通过基址地址加上偏移的方式来实现，该基址地址通常是shellcode执行时的起始位置。

* 获取到该起始位置后，需要将其写入到一个通用寄存器中，作为后续基址指针来使用。可能大家很容易想到通过mov eax，eip这条指令直接把当前eip的值放入到eax中遗憾的是，x86架构上指令指针寄存器eip不能被软件直接访问。

* call/pop指令

  Shellcode可以通过在一个call指令后立即执行pop指令，将上一刻压入栈中的指令地址载入到寄存器中，从而获取到shellcode起始的内存地址。

  ![1541215840365](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/1541215840365.png)

## 手动符号解析

* 符号解析定义

  即获取shellcode中想要执行的函数的内存地址

  * 为什么需要手动符号解析？

  * Shellcode不能确保所有的外部函数依赖都被解决，相反，必须自己找到这个函数，不能使用硬编码地址来找函数，需要动态定位这些函数，确保shellcode的通用性

  * 为了确保shellcode在不同的环境下均能可靠地工作，shellcode大多使用kernel32.dll中的LoadLibraryA和GetProcAddress两个函数来进行函数解析。

    LoadLibraryA函数加载指定的库到内存，并返回一个
    句柄；

    GetProcAddress函数在库的导出表中查找给定
    符号名或序号。

## 空雪橇指令

​	在shellcode之前一段很长的指令序列，其并不是shellcode正常功能必需的，但是被包括在漏洞利用中，以增加漏洞利用成功的可能性	shellcode编写者往往可以通过在shellcode前插入一大段空指令雪橇实现这一点，只要代码执行到这个空指令雪橇中的某处，shellcode中功能代码就会得到运行

![1541216160952](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/1541216160952.png)

通常由一长段NOP（0x90）指令序列组成,为了避免杀软的检测，也会用到0x40-0x4F范围内，这些都是
单字节指令，表示对寄存器的递增或者递减.

![1541216217604](https://raw.githubusercontent.com/xineting/xineting.github.io/master/img/1541216217604.png)

## 坏字符

* 如果shellcode中包含某些字符后便不能成功执行，则称该字符为坏字符。

* 坏字符就是破坏漏洞或者导致shellcode不能成功执行的字符

  第一类是该字符截断了后续输入，使shellcode未能完整的装载进内存，该情况下坏字符的产生是由输入函数本身决定
  的
  第二类是该字符在代码解析过程中，被替换成其他字符或者被自动忽略，导致被当做汇编代码执行时语义发生改变，该情况下坏字符的产生是由程序处理逻辑决定的.

  C语言输入函数所对应的第一类坏字符
  出现场景：阻止后续内容写入内存

  | 函数名称 | 坏字符    |
  | -------- | --------- |
  | gets     | \x00,\x0a |
  |  scanf     | \x09,\x0a,\x0b,\x0c,\x0d,\x20,\xff |
  |  strcpy     |  \x00 |

## 相关工具介绍

### pwntools–shellcraft

  * 在Linux系统下可以使用pwntools加速漏洞利用脚本的
  * 开发过程与shellcode开发的相关的功能模块shellcraft
  * 该模块可以生成不同指令架构（Intel 80386、AArch64、AMD64、ARM、MIPS）下不同功能的shellcode。



### Msfvenom

  Msfvenom是Metasploit工具箱中的一款工具，  通过它能够产生不同平台架构、不同操作系统、  不同功能的shellcode；
  结合了payload和encode功能，不仅内置多种  payload，而且还可以对shellcode进行多种编码  以绕过杀毒软件的检测，是shellcode开发中必备神器




​							**msfvenom常用参数及功能对照表**
|参数| 功能|
|-|-|
|-p, --payload <payload> |指定需要使用的payload(攻击载荷),通过-l –payload参数可以列举所有的|payload选项|
|-l, --list [module_type] |列举出可用资源|
|-n, --nopsled<length>| 指定NOP滑行长度|
|-e, --encoder <encoder> |指定所需要使用的编码器，可以通过-l encoders来获取所有支持的编码器选项|
|-a, --arch <architecture> |指定payload的目标平台，即CPU架构|
|-s, --space <length>| 指定有效攻击载荷的最大长度|
|-b, --bad-chars <list>| 指定规避的坏字符集|
|-f, --format <format>| 指定输出格式，可以使用—help-formats来获取支持的输出格式|
|--smallest |最小化生成的payload|
|-o, --out <path> |指定生成路径|
|-x, --template <path>| 指定一个自定义可执行文件作为模板，把shellcode注入进去|
|-k, --keep |保护模板程序的动作，注入的payload作为一个新的进程运行。在进程注入时一定要加上此参数|
|EXITFUNC| 适用于Shellcode注入其他进程时，指定shellcode运行完是结束线程还是结束进程|
