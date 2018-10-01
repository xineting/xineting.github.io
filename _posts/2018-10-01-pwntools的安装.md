---
layout:     post
title:      Pwntools
subtitle:   pwn
date:       2018-10-1
author:     XT
header-img: img/post-bg-unix-linux.jpg
catalog: 	 true
tags:
    - Pwn环境
---


>Pwntools

# Pwntools的安装

------


### 安装capstone

```
1.cd ~
2.git clone https://github.com/aquynh/capstone
3.cd capstone
4.make
5.make install
```

### 安装pwntools

```
1.cd ~
2.git clone https://github.com/Gallopsled/pwntools
3.cd pwntools
4.python setup.py install
```

验证一下pwntools安装成功：

```
1.python
2.import pwn
3.pwn.asm("xor eax,eax")
```

出现`'1\xc0'` 说明安装成功