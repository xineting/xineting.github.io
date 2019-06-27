---
layout:     post
title:      dirsearch脚本使用
subtitle:    渗透
date:       2019-6-16
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 渗透
---


> dirsearch使用方法

# dirsearch使用方法

脚本链接https://github.com/xineting/dirsearch

dirsearch是一个基于python3的命令行工具，旨在暴力扫描页面结构，包括网页中的目录和文件。

## 系统支持

WindowsXP/7/8/10

GNU/Linux

MacOSX

## 特点

dirsearch拥有以下特点：

> 多线程
> 可保持连接
> 支持多种后缀（-e|–extensions asp,php）
> 生成报告（纯文本，JSON）
> 启发式检测无效的网页
> 递归的暴力扫描
> 支持HTTP代理
> 用户代理随机化
> 批量处理
> 请求延迟

## 扫描器与字典

字典必须是文本文件，除了使用特殊的％EXT％之外，其余每行都会被处理。

例：

```
example/
example.%EXT%
```

使用扩展名“asp”和“aspx”会生成下面的字典：

```
example/
example.asp
example.aspx
```

### Linux下的使用示例：

```
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch/
./dirsearch.py -u 目标网址 -e *
```

### Windows系统下的使用示例

![1560741509147](https://raw.githubusercontent.com/xineting/xineting.github.io/master/pic/1560741509147.png)

