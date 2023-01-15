'''
Author: flwfdd
Date: 2022-01-03 13:44:03
LastEditTime: 2023-01-15 20:47:41
Description: 配置文件
_(:з」∠)_
'''
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66',
}

api_base_url = {
    "C": "http://x.x.x.x:3000",  # 网易云音乐API
    # "Q": "http://x.x.x.x:3300",  # QQ音乐API
}

# bilibili歌曲缓存，需要存入歌曲并提供url，这里使用阿里云OSS，可根据需求更换
if True: # 使用阿里云OSS
    import oss2
    oss_auth = oss2.Auth('xxx',
                         'xxx')
    oss_bucket = oss2.Bucket(
        oss_auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'xxx')
    oss_path = "ori/bili/"
    oss_url = "https://xxx.oss-cn-hangzhou.aliyuncs.com/"+oss_path

    # 实现以下函数即可

    # 检查缓存文件是否存在，如果存在返回链接，否则返回空字符串
    def check_tmp(filename):
        if oss_bucket.object_exists(oss_path+filename):
            return oss_url+filename+"?x-oss-traffic-limit=819200"
        else:
            return ""

    # 储存文件并返回链接
    def save_tmp(filename, bin):
        oss_bucket.put_object(oss_path+filename, bin)
        return oss_url+filename+"?x-oss-traffic-limit=819200"
else: #使用腾讯云COS
    from qcloud_cos_v5 import CosConfig
    from qcloud_cos_v5 import CosS3Client
    secret_id = ''     # 替换为用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
    secret_key = ''   # 替换为用户的 SecretKey，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi
    region = 'ap-chengdu'      # 替换为用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
                            # COS支持的所有region列表参见https://cloud.tencent.com/document/product/436/6224
    token = None               # 如果使用永久密钥不需要填入token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见https://cloud.tencent.com/document/product/436/14048
    scheme = 'https'           # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    client = CosS3Client(config)

    cos_path = "bili/"
    cos_url = "https://xxx.cos.ap-chengdu.myqcloud.com/"+cos_path

    # 实现以下函数即可

    # 检查缓存文件是否存在，如果存在返回链接，否则返回空字符串
    def check_tmp(filename):
        if client.object_exists("xxx",cos_path+filename):
            return cos_url+filename+"?x-cos-traffic-limit=819200"
        else:
            return ""

    # 储存文件并返回链接
    def save_tmp(filename, bin):
        client.put_object("xxx",bin,cos_path+filename)
        return cos_url+filename+"?x-cos-traffic-limit=819200"

# 网易云账号cookie
C_vip_cookie = ""
# QQ音乐账号cookie
# Q_vip_cookie = ""