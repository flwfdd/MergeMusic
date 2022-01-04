'''
Author: flwfdd
Date: 2022-01-03 13:44:03
LastEditTime: 2022-01-03 16:40:12
Description: 
_(:з」∠)_
'''
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/80.0.361.66',
    }

api_base_url={
    "C":"",
    "Q":"",
    }

#缓存文件夹
tmp_path=""

# bilibili歌曲缓存，需要存入歌曲并提供url，这里使用阿里云OSS，可根据需求更换
if True:
    # oss配置
    import oss2
    oss_auth = oss2.Auth('', '')
    oss_bucket = oss2.Bucket(oss_auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'su-ours-public')

    # 实现以下函数即可

    # 检查缓存文件是否存在，如果存在返回url，否则返回空字符串
    def check_tmp(filename):
        if oss_bucket.object_exists('ori/bili/'+filename):
            return "https://su-ours-public.oss-cn-hangzhou.aliyuncs.com/ori/bili/"+filename
        else:
            return ""
    
    # 储存文件并返回链接
    def save_tmp(filename,bin):
        oss_bucket.put_object('ori/bili/'+filename,bin)
        return "https://su-ours-public.oss-cn-hangzhou.aliyuncs.com/ori/bili/"+filename

#网易云会员cookie
C_vip_cookie=""
