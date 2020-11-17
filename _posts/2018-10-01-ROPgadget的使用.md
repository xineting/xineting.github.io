---
layout:     post
title:      ROPgadget
subtitle:   ROPgadget
date:       2018-10-1
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 安全
---


>ROPgadget

# ROPgadget

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