# [](https://github.com/imgyh/tiktok/compare/v1.5.2...v) (2023-03-05)


### Bug Fixes

* **web:** 取消指定端口为必选项 ([1b85b19](https://github.com/imgyh/tiktok/commit/1b85b1989119cb35888e4e2d4f4018ed276f68d2))


### Features

* **live:** 增加直播解析方法的提示信息开启或关闭选项 ([469fe2c](https://github.com/imgyh/tiktok/commit/469fe2c5217ff22e42c1523d089a119415266c23))
* **url:** 添加速度更快的X-Bogus接口 ([7c44b94](https://github.com/imgyh/tiktok/commit/7c44b9426dc30f3be97d6e5824bf628c47276a87))
* **web:** 增加命令行指定web端口 ([98a9f74](https://github.com/imgyh/tiktok/commit/98a9f74d4b0b319ea1aeb3883c105c0b805105f1))



# [](https://github.com/imgyh/tiktok/compare/v1.5.1...v) (2023-03-04)


### Bug Fixes

* **live:** 修复无法播放http的直播地址 ([04ec0f1](https://github.com/imgyh/tiktok/commit/04ec0f1c400adb5bfacf74dca0114ec9d625e3cc))


### Features

* **live:** 适配web端的直播解析 ([f7fdcd1](https://github.com/imgyh/tiktok/commit/f7fdcd141b3a9877f5fd888383bfa48875d023bf))
* **tiktok:** 支持本地生成X-Bogus ([#3](https://github.com/imgyh/tiktok/issues/3)) ([a4328cd](https://github.com/imgyh/tiktok/commit/a4328cd53bd8a0342cf053050a8066130e008cde))
* **utils:** 重新加入远程调用X-Bogus接口作为备用,防止本地没有JS环境 ([4467018](https://github.com/imgyh/tiktok/commit/44670186afdcb1314194b0c00f39d1baa9681985))
* **web:** 增加web端直播解析 ([90aa105](https://github.com/imgyh/tiktok/commit/90aa10515f7bc90ed35c9484e2993083a533d6cc))



# [](https://github.com/imgyh/tiktok/compare/v1.5.0...v) (2023-03-02)


### Bug Fixes

* **tiktok:** cookies增加passport_csrf_token ([ebe3be4](https://github.com/imgyh/tiktok/commit/ebe3be43ef676c39cd1cd63cc606df1a9e5b1995))



#  (2023-03-02)


### Bug Fixes

* **command:** 修复头像封面音乐总是会下载 ([665ca47](https://github.com/imgyh/tiktok/commit/665ca47b08623699606d56e424eb096a92afa9fe))
* **tiktok:** 自动获取ttwid ([c6bcff6](https://github.com/imgyh/tiktok/commit/c6bcff67da8a659afb1c722ab40da733f1a79403))


### Features

* **tiktok:** 增加下载前n个作品功能 ([4efeb62](https://github.com/imgyh/tiktok/commit/4efeb62701acc6cf8d9fd06d1a80499a7ad5c6cc))
* **tiktok:** 增加音乐合集批量下载功能 ([b3aadf6](https://github.com/imgyh/tiktok/commit/b3aadf630ad8be9b79fa26a18799336c38569645))
* **url:** 增加音乐合集URL ([fa635eb](https://github.com/imgyh/tiktok/commit/fa635ebe7f70478e8408b5a8afe30ff0b1ff890f))



#  (2023-02-23)


### Bug Fixes

* **live:** 统一直播获取的header, 直播接口添加X-Bogus ([197d126](https://github.com/imgyh/tiktok/commit/197d12627d855f3353dba3fd68f0b308593f62e8))
* **tiktok:** 修复主页作品接口 ([e3029be](https://github.com/imgyh/tiktok/commit/e3029be42b021dcdad0736800a4f13428ddd5b98))
* **tiktok:** 修复用户主页作品接口 ([8a01e68](https://github.com/imgyh/tiktok/commit/8a01e681b5206c27a44f4ba10f840e856686e33b))
* **tiktok:** 添加单个作品获取失败后重试逻辑 ([ac73a97](https://github.com/imgyh/tiktok/commit/ac73a97c19840bd7147f3a7e4b400a37b1365fb2))


### Features

* **tiktok:** 增加合集下载功能 ([b95d718](https://github.com/imgyh/tiktok/commit/b95d7188282de5474861043ab011ed27baa79796))



#  (2023-02-20)


### Bug Fixes

* **tiktok:** 修复主页作品接口与直播接口 ([909b9f3](https://github.com/imgyh/tiktok/commit/909b9f3f1cec9684da33f63aeb816aaab2e7e6b9))
* **tiktok:** 修复主页作品接口获取数据不稳定, 增加X-Bogus接口限制 ([62072e8](https://github.com/imgyh/tiktok/commit/62072e881eb3531df68f9fe6d8bdab03a4f00790))


#  (2023-02-13)


### Bug Fixes

* **tiktok:** 修改X-Bogus接口 ([abb9a8e](https://github.com/imgyh/tiktok/commit/abb9a8e857ea98b38b47e3419554dfe490ec1d78))


#  (2023-02-11)


### Bug Fixes

* **tiktok:** 修复失效API，增加X-Bogus ([53d3b58](https://github.com/imgyh/tiktok/commit/53d3b5875ecd4de57f4dc4df4c228cf80b15c764))


#  (2023-01-30)


### Features

* **tiktok:** 初始提交 ([74f9c91](https://github.com/imgyh/tiktok/commit/74f9c91e75b324ae5e0dc5f9fa5bc4baf4611bd2))



