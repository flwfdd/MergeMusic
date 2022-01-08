# MergeMusic 后端

使用`Python`构建，支持传统服务器实例或`Serverless`云函数计算运行。

[网易云音乐API](https://github.com/Binaryify/NeteaseCloudMusicApi) 和 [QQ音乐API](https://github.com/jsososo/QQMusicApi) 部分为了偷懒用了两个现成的项目，根据项目文档调`API`即可。B站部分为自研，播放音频原理为B站视频是音视频分离的`m4s`格式，但因为`Referer`的原因没有办法直接播放，现在必须要使用自己的服务器缓存，还没有找到好解决方法。

## 文件架构

* `config.py`: 配置文件
* `app.py`: 基于`Flask`的服务器实例版本主程序
* `index.py`: 阿里云函数计算入口函数。
* `search.py`: 搜索功能模块
* `music.py`: 歌曲功能模块

## 音乐接口格式
```json
[{
    "type": "格式，api根据这个确定返回内容。有music|list|p|up|user|fav，b站层级比较多",
    "mid": "音乐ID，有前缀C/Q/B",
    "name": "音乐名称",
    "src": "音乐源链接",
    "img": "封面图链接",
    "lrc": "歌词",
    "tlrc": "翻译歌词",
    "album": {
      "name": "专辑名称"
    },
    "artist": ["艺术家名字"]
}]
```

## 如何使用？

进入`config.py`完成配置，跑起后端，再更改前端代码中的`apiurl`即可。首先在`api_base_url`填写搭建好的上面提到的两个`API`的链接。

**使用阿里云函数计算**

`tmp_path`需为`/tmp/`（否则函数计算中会报无权写入错误）。创建一个`Python`环境的函数，把后端文件夹整体上传。


**使用阿里云OSS**

根据官方文档配置OSS部分，`oss_path`是OSS内路径，`oss_url`是OSS外网访问地址。

**使用传统服务器**

运行`app.py`即可，默认运行在`9000`端口。要配置好`tmp_path`。如果不使用`OSS`，需要自己实现那两个函数。
