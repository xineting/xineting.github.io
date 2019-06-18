---
layout:     post
title:      ubunut更换终端颜色
subtitle:    ubunut更换终端颜色
date:       2019-6-6
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - linux
---


> ubunut更换终端颜色

# ubunut更换终端颜色



首先需要在命令行执行

```shell
vi ~/.bashrc
```



在最后添加如下代码：

```shell
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;35;40m\]\u\[\033[00;00;40m\]@\[\033[01;35;40m\]\h\[\033[00;31;40m\]:\[\033[00;00;40m\]\w \[\033[01;32;40m\]\$ \[\033[01;36;40m\]'
```

```shell
source ~/.bashrc
```

有关配色

|前景             | 背景       |       颜色|
| ---- | ---- |
|30             |      40        |          黑色|
|31             |      41            |      紅色|
|32             |      42            |      綠色|
|33             |      43            |      黃色|
|   34            |       44            |      藍色|
|   35             |      45             |     紫紅色|
|   36        |           46            |      青藍色|
|   37            |       47       |          白色|
|   1                 |    1     |           透明色|

| 代码 | 意义 |
| ---- | ---- |
|   0    |          OFF|
|1                |    高亮显示 |
|4             |       underline|
|5             |       闪烁|
|7               |     反白显示|
|8          |          不可见|


