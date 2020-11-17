---
layout:     post
title:       安装Transmission
subtitle:    安装Transmission
date:       2020-10-18
author:     XT
header-img: img/post-bg-coffee.jpeg
catalog: 	 true
tags:
    - 运维
---


> 安装Transmission



# 一、Transmission的安装

在Ubuntu中，打开终端，输入以下命令安装：

```
sudo apt-get install transmission-daemon
```



| Item             | Loccation                              |
| ---------------- | -------------------------------------- |
| 启动初始化脚本   | /etc/init.d/transmission-daemon        |
| 基本配置文件     | /etc/default/transmission-daemon       |
| 详细配置文件目录 | /var/lib/transmsision-daemon/info      |
| 下载存储目录     | /var/lib/transmission-daemon/downloads |

- settings.json： 主要的配置文件，设置daemon的各项参数，包括RPC的用户名密码配置。它实际上是一个符号链接，指向的原始文件是/etc/transmission-daemon/settings.json。里面的参数解释可以参考[官网的配置说明](https://trac.transmissionbt.com/wiki/EditConfigFiles)。
- torrents/： 用户存放.torrent种子文件的目录,凡是添加到下载任务的种子，都存放在这里。.torrent的命名包含,种子文件本身的名字和种子的SHA1 HASH值。
- resume/： 该存放了.resume文件，.resume文件包含了一个种子的信息，例如该文件哪些部分被下载了，下载的数据存储的位置等等。
- blocklists/： 存储被屏蔽的peer的地址。
- dht.dat： 存储DHT节点信息。

```bash
启动 sudo service transmission-daemon start
停止 sudo service transmission-daemon stop
```



# 二、配置

打开文件/var/lib/transmission-daemon/info/settings.json，修改配置参数如下：2

```j
{

    "rpc-authentication-required": true
    
    "rpc-bind-address": "0.0.0.0", 
    
    "rpc-enabled": true, 
    
    "rpc-password": "123456", 
    
    "rpc-port": 9091,
    
    "rpc-url": "/transmission/",    
  
    "rpc-username": "transmission", 
    
    "rpc-whitelist": "*", 
    
    "rpc-whitelist-enabled": true,
    
}
```

我将用户名设置为了transmission，密码设置为了123456，whitelist设置成了”*”，表示任何IP都可以通过RPC协议访问这个daemon。

需要注意的是password设置成了明文。当启动daemon之后，daemon会自动检测密码设置。如果发现密码配置被修改了，daemon会自动计算修改后的密码的HASH值，并用这个HASH值替换掉配置文件中的明文密码，这样会更安全。

```
service transmission-daemon start
```

启动程序后，打开settings.json，会看到rpc-password一项被改为了HASH值。

```
"rpc-password": "{5f4bd5498bddd9aa2ad8f4d475dcebe23e9d8c8bsorspnUE"}, 
```

## 配置其它参数

settings.json里面还有很多参数可以配置，包括上传/下载速度的限制、DHT的配置、端口设置等等，详细的参数解释可以参考[官网的配置说明](https://trac.transmissionbt.com/wiki/EditConfigFiles)，这里不再赘述。



# 三、使用Web界面控制Transmission daemon

经过上述配置后，我们就可以通过Web界面来访问和控制Transmission daemon了。在浏览器里面输入以下地址

```
http://<your.server.ip.addr>:9091/transmission/web/
```

浏览器提示你输入刚才配置的用户名和密码，就可以成功登陆Web管理界面。界面和桌面版的GUI程序有点像，操作起来很方便。下图是我尝试使用的界面。