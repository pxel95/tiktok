# 前言

本文主要是关于我写的抖音批量下载与去水印工具的介绍。

本项目分为单个作品(视频/图集)去水印工具和批量下载工具

代码已经开源在我的GitHub上，欢迎大家star。

开源地址：https://github.com/imgyh/tiktok

抖音去水印工具Web demo：https://dy.gyh.im/

**联系方式:**

> [TG](https://t.me/gyh9527)
> [TG群组](https://t.me/GYHgroup)
> [Email](mailto:admin@imgyh.com)

## 抖音去水印工具 Feature

* 通过作品分享链接获取去水印作品、音乐、封面图、头像
* 获取点赞数、评论数、收藏数、分享数、作品描述等信息
* 支持直播解析
* 基于Flask实现 Web 交互界面
* 提供相关接口，支持单个作品、直播、主页喜欢、主页作品、主页合集、合集、音乐(原声)通过接口获取

![tiktokweb](img/tiktokweb.jpg)
![tiktokweb video](img/tiktokwebvideo.jpg)
![tiktokweb preview video](img/tiktokwebpreviewvideo.jpg)
![tiktokweb image](img/tiktokwebimage.jpg)
![tiktokweb preview image](img/tiktokwebpreviewimage.jpg)

## 抖音批量下载工具 Feature

* 支持个人主页链接、作品分享链接、抖音直播Web链接、合集链接、音乐(原声)集合链接
* 支持单个作品下载、主页作品下载、主页喜欢下载、直播解析、单个合集下载、主页所有合集下载、音乐(原声)集合下载
* 下载视频、视频封面、音乐、头像
* 去水印下载
* 自动跳过已下载
* 支持指定下载作品数量
* 多线程下载
* 支持多链接下载
* 增量更新与数据持久化到数据库, 保存每条作品信息到数据库, 并根据数据库是否存在来增量请求下载

![](img/tiktokcommand1.jpg)
![](img/tiktokcommand2.jpg)
![tiktokcommandl ive](img/tiktokcommandlive.jpg)
![tiktokcommand download](img/tiktokcommanddownload.jpg)
![tiktokcommand download detail](img/tiktokcommanddownloaddetail.jpg)

# 使用方法

- 支持的地址格式, 形如

```
抖音app分享链接:
1. 作品(视频或图集)、直播、合集、音乐集合、个人主页    https://v.douyin.com/BugmVVD/    
抖音网页版浏览器URL:
2. 单个视频             https://www.douyin.com/video/6915675899241450760
3. 单个图集             https://www.douyin.com/note/7014363562642623777
4. 用户主页             https://www.douyin.com/user/MS4wLjABAAAA06y3Ctu8QmuefqvUSU7vr0c_ZQnCqB0eaglgkelLTek
5. 单个合集             https://www.douyin.com/collection/7208829743762769975
6. 音乐(原声)下的视频     https://www.douyin.com/music/7149936801028131598
7. 直播                https://live.douyin.com/759547612580                     
```

## 安装node.js环境(可选)

> 为了快速获取X-Bogus加密参数, 推荐在本地安装node.js环境, 这样可以通过本地执行获取X-Bogus加密参数的js文件
> 当然如果没有安装node.js环境, 程序会从我服务器上部署的接口获取X-Bogus加密参数

## 抖音去水印工具

### 使用方式

使用抖音去水印工具有4种方式

1. (推荐)直接使用我搭建的抖音去水印工具：https://dy.gyh.im/

2. 使用docker运行

```
docker run -d -p 5000:5000 --name tiktok --restart=always imgyh/tiktokweb
```

3. 本地搭建`python3.9`环境运行

```
cd /path/to/tiktok
python -m pip install -r requirements.txt
python TikTokWeb.py
```

4. windows用户也可以下载 Releases 中的 [TikTokWeb.exe](https://github.com/imgyh/tiktok/releases) 文件双击运行

5. 指定端口运行

```
# 指定端口运行
python TikTokWeb.py -p 5001
.\TikTokWeb.exe -p 5001
```

访问: http://localhost:5000


## 抖音批量下载工具

批量下载有两种方式运行, 配置文件和命令行

默认使用配置文件方式

### 安装依赖

windows用户下载 Releases 中的 [TikTokCommand.exe](https://github.com/imgyh/tiktok/releases) 文件运行
windows用户本地有`python3.9`环境, 也可按照linux与mac用户的方式运行

linux与mac用户下载本项目, 在本地`python3.9`环境中运行, 首先需要安装依赖, 安装命令

```
cd /path/to/tiktok
python -m pip install -r requirements.txt
```

### 使用Docker

请映射以下两个目录(三个位置需要修改), 根据实际情况修改目录地址

`/path/to/tiktok` 源代码目录
`/path/to/downloads` 下载位置

```
docker run -d -p 5000:5000 --name tiktok --restart=always -v /path/to/tiktok:/app -v /path/to/downloads:/path/to/downloads imgyh/tiktokweb
```

将所有用到 `python TikTokCommand.py` 替换成 `docker exec -it tiktok python3 TikTokCommand.py`

### 配置文件方式

配置文件名必须叫 `config.yml`, 并将其放在TikTokCommand.py或者TikTokCommand.exe同一个目录下

直接运行TikTokCommand.py或者TikTokCommand.exe, 无需在命令中加入任何参数, 所有参数都从配置文件中读取

基本配置示例如下, 请自己登录网页版抖音后F12获取cookie

```yaml
#######################################
# 说明:
# 1. 井号(#)为注释
# 2. 缩进严格对齐，使用空格缩进, 注意有些冒号后面有一个空格, 有些没有空格
# 3. 请使用英文字符
# 4. 更多yaml语法请上网查看
#######################################


# 作品(视频或图集)、直播、合集、音乐集合、个人主页的分享链接或者电脑浏览器网址
# (删除文案, 保证只有URL, https://v.douyin.com/kcvMpuN/ 或者 https://www.douyin.com/开头的)
# 可以设置多个链接, 确保至少一个链接
# 必选
link:
  - https://live.douyin.com/759547612580
  - https://v.douyin.com/BugmVVD/
  - https://v.douyin.com/BugrFTN/
  - https://v.douyin.com/B38oovu/
  - https://v.douyin.com/S6YMNXs/

# 下载保存位置, 默认当前文件位置
# 必选
path: C:\project\test333

# 是否下载视频中的音乐(True/False), 默认为True
# 可选
music: True

# 是否下载视频的封面(True/False), 默认为True, 当下载视频时有效
# 可选
cover: True

# 是否下载作者的头像(True/False), 默认为True
# 可选
avatar: True

# 是否保存获取到的数据(True/False), 默认为True
# 可选
json: True

# link是个人主页时, 设置下载发布的作品(post)或喜欢的作品(like)或者用户所有合集(mix), 默认为post, 可以设置多种模式
# 可选
mode:
  - post
  - like
  - mix

# 下载作品个数设置
# 可选
number:
  post: 5     # 主页下作品下载个数设置, 默认为0 全部下载
  like: 5     # 主页下喜欢下载个数设置, 默认为0 全部下载
  allmix: 1   # 主页下合集下载个数设置, 默认为0 全部下载
  mix: 5      # 单个合集下作品下载个数设置, 默认为0 全部下载
  music: 5    # 音乐(原声)下作品下载个数设置, 默认为0 全部下载

# 增量下载, 下载作品范围: 抖音最新作品到本地的最新作品之间的作品, 如果本地没有该链接的任何视频则全部下载
# 可配合 number 选项一起使用
# 情况1: number(假如设置5) 和 increase(假如抖音博主更新了3条作品,本地并未下载) 则会获取5条数据并下载(已下载就跳过)
# 情况2: number(假如设置5) 和 increase(假如抖音博主更新了6条作品,本地并未下载) 则会获取6条数据并下载(已下载就跳过)
# 情况3: number(假如设置5) 和 increase(假如本地并未下载该博主视频) 则会获取所有的视频
# 情况4: 当获取主页所有mix时(mode是mix模式)比较特殊, number(allmix) 控制下载多少个合集, increase(allmix) 对每个合集进行增量更新
# 可选
increase:
  post: False     # 是否开启主页作品增量下载(True/False), 默认为False
  like: False     # 是否开启主页喜欢增量下载(True/False), 默认为False
  allmix: False   # 是否开启主页合集增量下载(True/False), 默认为False
  mix: False      # 是否开启单个合集下作品增量下载(True/False), 默认为False
  music: False    # 是否开启音乐(原声)下作品增量下载(True/False), 默认为False

# 设置线程数, 默认5个线程
# 可选
thread: 5

# cookie 请登录网页抖音后F12查看
# cookies 和 cookie 二选一, 要使用这种形式, 请注释下面的cookie
# 目前只需要msToken、ttwid、odin_tt、passport_csrf_token、sid_guard
# 可以动态添加, 程序会根据填的键查找，并没有写死, 如果抖音需要更多的cookie自己加上就行了
cookies:
  msToken: xxx
  ttwid: xxx
  odin_tt: xxx
  passport_csrf_token: xxx
  sid_guard: xxx

# cookie 请登录网页抖音后F12查看
# cookies 和 cookie 二选一, 要使用这种形式, 请注释上面的cookies及包含的所有键值对
# 设置了这个后上面的cookies选项自动失效, 这个优先级更高
# 格式: "name1=value1; name2=value2;" 注意要加冒号
# 冒号中的内容包括不限于以下键值对, 如果抖音需要更多的cookie自己加上就行了
#cookie: "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"


```

### 命令行方式

运行示例:

- 获取帮助信息

```
windows用户:
.\TikTokCommand.exe -h
linux与mac用户:
python TikTokCommand.py -h
```

- 参数介绍

```
-h, --help                       展示帮助页
--cmd CMD, -C CMD                使用命令行(True)或者配置文件(False), 默认为False
--link LINK, -l LINK             作品(视频或图集)、直播、合集、音乐集合、个人主页的分享链接或者电脑浏览器网址, 可以设置多个链接
                                 (删除文案, 保证只有URL, https://v.douyin.com/kcvMpuN/ 或者 https://www.douyin.com/开头的)
--path PATH, -p PATH             下载保存位置, 默认当前文件位置
--music MUSIC, -m MUSIC          是否下载视频中的音乐(True/False), 默认为True
--cover COVER, -c COVER          是否下载视频的封面(True/False), 默认为True, 当下载视频时有效
--avatar AVATAR, -a AVATAR       是否下载作者的头像(True/False), 默认为True
--json JSON, -j JSON             是否保存获取到的数据(True/False), 默认为True
--mode MODE, -M MODE             link是个人主页时, 设置下载发布的作品(post)或喜欢的作品(like)或者用户所有合集(mix), 默认为post, 可以设置多种模式
--postnumber POSTNUMBER          主页下作品下载个数设置, 默认为0 全部下载
--likenumber LIKENUMBER          主页下喜欢下载个数设置, 默认为0 全部下载
--allmixnumber ALLMIXNUMBER      主页下合集下载个数设置, 默认为0 全部下载
--mixnumber MIXNUMBER            单个合集下作品下载个数设置, 默认为0 全部下载
--musicnumber MUSICNUMBER        音乐(原声)下作品下载个数设置, 默认为0 全部下载
--postincrease POSTINCREASE      是否开启主页作品增量下载(True/False), 默认为False
--likeincrease LIKEINCREASE      是否开启主页喜欢增量下载(True/False), 默认为False
--allmixincrease ALLMIXINCREASE  是否开启主页合集增量下载(True/False), 默认为False
--mixincrease MIXINCREASE        是否开启单个合集下作品增量下载(True/False), 默认为False
--musicincrease MUSICINCREASE    是否开启音乐(原声)下作品增量下载(True/False), 默认为False
--thread THREAD, -t THREAD       设置线程数, 默认5个线程
--cookie COOKIE                  设置cookie, 格式: "name1=value1; name2=value2;" 注意要加冒号
```

- 多链接多模式混合下载, 可以传入多个链接和多个模式(post、like、mix)

```
windows用户:
.\TikTokCommand.exe -C True `
  -l https://live.douyin.com/759547612580 `
  -l https://v.douyin.com/BugmVVD/ `
  -l https://v.douyin.com/BugrFTN/ `
  -l https://v.douyin.com/B72pdU5/ `
  -l https://v.douyin.com/B72QgDw/ `
  -l https://v.douyin.com/AJp8D3f/ `
  -l https://v.douyin.com/B38oovu/ `
  -l https://v.douyin.com/S6YMNXs/ `
  -p C:\project\test `
  -M post `
  -M like `
  -M mix `
  --postnumber 5 `
  --likenumber 5 `
  --allmixnumber 1 `
  --mixnumber 5 `
  --musicnumber 5 `
  --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"

linux与mac用户:
python TikTokCommand.py -C True \
  -l https://live.douyin.com/759547612580 \
  -l https://v.douyin.com/BugmVVD/ \
  -l https://v.douyin.com/BugrFTN/ \
  -l https://v.douyin.com/B72pdU5/ \
  -l https://v.douyin.com/B72QgDw/ \
  -l https://v.douyin.com/AJp8D3f/ \
  -l https://v.douyin.com/B38oovu/ \
  -l https://v.douyin.com/S6YMNXs/ \
  -p /path/to/downdir \
  -M post \
  -M like \
  -M mix \
  --postnumber 5 \
  --likenumber 5 \
  --allmixnumber 1 \
  --mixnumber 5 \
  --musicnumber 5 \
  --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载单个作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/kcvMpuN/ -p C:\project\test --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/kcvMpuN/ -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载主页全部作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/kcvSCe9/ -p C:\project\test --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/kcvSCe9/ -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载主页前n个作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/kcvSCe9/ -p C:\project\test --postnumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/kcvSCe9/ -p /path/to/downdir --postnumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载主页全部喜欢

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/kcvSCe9/ -p C:\project\test -M like --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/kcvSCe9/ -p /path/to/downdir -M like --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载主页前n个喜欢

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/kcvSCe9/ -p C:\project\test -M like --likenumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/kcvSCe9/ -p /path/to/downdir -M like --likenumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载单个合集全部作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/B3J63Le/ -p C:\project\test --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/B3J63Le/ -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载单个合集前n个作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/B3J63Le/ -p C:\project\test --mixnumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/B3J63Le/ -p /path/to/downdir --mixnumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载主页全部合集下所有作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/B38oovu/ -p C:\project\test -M mix --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/B38oovu/ -p /path/to/downdir -M mix --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载主页前n个合集下所有作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/B38oovu/ -p C:\project\test -M mix --allmixnumber 2 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/B38oovu/ -p /path/to/downdir -M mix --allmixnumber 2 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载音乐(原声)集合下所有作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/S6YMNXs/ -p C:\project\test --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/S6YMNXs/ -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 下载音乐(原声)集合下前n个作品

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/S6YMNXs/ -p C:\project\test --musicnumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/S6YMNXs/ -p /path/to/downdir --musicnumber 30 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 关闭头像下载, cover, music json数据也是一样的设置对应选项为 False

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/kcvSCe9/ -p C:\project\test -a False --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/kcvSCe9/ -p /path/to/downdir -a False --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 多线程设置, 默认5个线程, 可以自己调节线程数

```
windows用户:
.\TikTokCommand.exe -C True -l https://v.douyin.com/kcvSCe9/ -p C:\project\test -t 8 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://v.douyin.com/kcvSCe9/ -p /path/to/downdir -t 8 --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```

- 直播推流地址解析

```
windows用户:
.\TikTokCommand.exe -C True -l https://live.douyin.com/802939216127 -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
或者
.\TikTokCommand.exe -C True -l https://v.douyin.com/SnXMoh2/ -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
linux与mac用户:
python TikTokCommand.py -C True -l https://live.douyin.com/802939216127 -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
或者
python TikTokCommand.py -C True -l https://v.douyin.com/SnXMoh2/ -p /path/to/downdir --cookie "msToken=xxx; ttwid=xxx; odin_tt=xxx; passport_csrf_token=xxx; sid_guard=xxx;"
```



# Web版接口

1. 单个作品、图集接口

   ```
   接口地址: 127.0.0.1:5000/douyin/aweme
   请求方式: POST
   请求参数, JSON或form表单: 
   {
   "share_link":"https://v.douyin.com/kcvMpuN/",
   "cookie":"xxxx"
   }
   ```

2. 直播解析接口

   ```
   接口地址: 127.0.0.1:5000/douyin/live
   请求方式: POST
   请求参数, JSON或form表单: 
   {
   "share_link":"https://v.douyin.com/DdWaSBd/",
   "cookie":"xxxx"
   }
   ```

   

3. 主页作品

   ```
   接口地址: 127.0.0.1:5000/douyin/user/post
   请求方式: POST
   请求参数, JSON或form表单: 
   {
   "share_link":"https://v.douyin.com/B72pdU5/",
   "cursor":0,
   "cookie":"xxxx"
   }
   ```

   

4. 主页喜欢

   ```
   接口地址: 127.0.0.1:5000/douyin/user/like
   请求方式: POST
   请求参数, JSON或form表单: 
   {
   "share_link":"https://v.douyin.com/AoWVvYH/",
   "cursor":0,
   "cookie":"xxxx"
   }
   ```

   

5. 主页合集

   ```
   接口地址: 127.0.0.1:5000/douyin/user/mix
   请求方式: POST
   请求参数, JSON或form表单: 
   {
   "share_link":"https://v.douyin.com/B38oovu/",
   "cursor":0,
   "cookie":"xxxx"
   }
   ```

   

6. 单个合集

   ```
   接口地址: 127.0.0.1:5000/douyin/mix
   请求方式: POST
   请求参数, JSON或form表单: 
   {
   "share_link":"https://www.douyin.com/collection/7217644759668492345", // https://v.douyin.com 这种类型也可以
   "cursor":0,
   "cookie":"xxxx"
   }
   ```

   

7. 音乐(原声)

   ```
   接口地址: 127.0.0.1:5000/douyin/music
   请求方式: POST
   请求参数, JSON或form表单: 
   {
   "share_link":"https://v.douyin.com/S6YMNXs/",
   "cursor":0,
   "cookie":"xxxx"
   }
   ```



# ToDo

- [x] 单个合集下载
- [x] 主页所有合集下载
- [x] 获取分享的音乐(原声)链接下的所有作品
- [x] 指定下载作品数量
- [ ] 获取热搜榜数据
- [x] 多链接批量下载
- [x] 多线程下载
- [x] 保存数据至数据库
- [x] 制作成接口
- [ ] 获取收藏与观看历史
- [ ] 直播间数据

# 鸣谢

本项目部分思路来自[TikTokDownload](https://github.com/Johnserf-Seed/TikTokDownload)

# 申明

本项目只作为学习用途, 切勿他用

# License

[MIT](https://opensource.org/licenses/MIT) © [imgyh](https://www.imgyh.com/)

# Star History

[![Star History Chart](https://api.star-history.com/svg?repos=imgyh/tiktok&type=Date)](https://star-history.com/#imgyh/tiktok&Date)
