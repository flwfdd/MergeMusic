# 聚合音乐 | MergeMusic
结合了网易云音乐、QQ音乐、bilibili的单页面音乐播放下载网站。

功能
* [x] 多平台音乐混合播放
* [x] 音乐歌词图片下载
* [x] 播放列表管理
* [x] 强大的搜索功能
* [x] B站视频作音乐听
* [x] ~~歌词音频可视化~~

### 基于以下模块
* Vue
* Vuetify
* [网易云音乐API](https://github.com/Binaryify/NeteaseCloudMusicApi)
* [QQ音乐API](https://github.com/jsososo/QQMusicApi)
* B站原生API
* Python

后端部分详细介绍请看[backend文件夹]("https://github.com/flwfdd/MergeMusic/tree/master/backend")。

（长时间以来修修补补代码堪称屎山Orz

### 开发日志
@20220104

转眼已经快两年了啊....也已经大学了。两年来的体育节用这个项目配合QQ机器人做了点歌系统，前端搬到了`Vuetify`上，后端搬到了`Serverless`上。现在大概是打算整理一下做一期视频。


@20200404

基本上重构了一遍，统一简化了处理流程，尽量把东西都扔到`API`上。统一了`API`的返回格式。
```json
[{
    "type": "格式，api根据这个确定返回内容。有music|list|p|up|user|fav，b站层级比较多",
    "mid": "音乐ID，有前缀C/Q/B",
    "name": "音乐名称",
    "album": {
      "name": "专辑名称"
    },
    "artist": ["艺术家名字"]
}]
```
增加了`bilibili`的功能，但是必须有服务器缓存音乐才行，用了阿里云的学生机，反正服务器上行带宽是无限的，下行用`HTTP 206`速度够的，问题也不大。


@20200314

增加了播放列表的管理和平滑动画，功能上暂时没什么想加的了。


@20200313

不知为何歌词音频可视化如果不加`crossorigin`就会失效，但是加了以后QQ音乐又会有跨域错误。所以QQ现在没有音频可视化。上传到了`github`