# -*- coding: utf-8 -*-
import requests
import json
import time
import os
import config

header=config.header
api_url=config.api_base_url.copy()

check_tmp=config.check_tmp
save_tmp=config.save_tmp


# 网易云

def cloud_user(mid):
    url=api_url["C"]+"/user/playlist?uid="+mid
    print(url)
    r=requests.get(url)
    dic=json.loads(r.text)['playlist']
    
    for ind,i in enumerate(dic):
        x={}
        x['type']='list'
        x['mid']="C"+str(i['id'])
        x['name']=i['name']
        x['artist']=[i['creator']['nickname']]
        x['album']={'name':""}
        dic[ind]=x
    return dic

def cloud_list(mid):
    url=api_url["C"]+"/playlist/detail?id="+mid
    print(url)
    r=requests.get(url)
    Ids=json.loads(r.text)
    #print(Ids['playlist']['tracks'])
    Ids=[str(i['id']) for i in Ids['playlist']['trackIds']]
    
    data={
        'ids':','.join(Ids)
    }
    url=api_url["C"]+"/song/detail?br=320000&t="+str(time.time())
    r=requests.post(url,data=data)
    dic=json.loads(r.text)['songs']
    
    for ind,i in enumerate(dic):
        x={}
        x['type']='music'
        x['mid']="C"+str(i['id'])
        x['name']=i['name']
        x['artist']=[j["name"] for j in i['ar']]
        x['album']={'name':i['al']["name"]}
        dic[ind]=x
    return dic

def cloud_music(mid):
    dic={"lrc":'',"tlrc":'',"src":'',"img":'','type':'music','mid':'C'+mid}
    try:
        data={
            "id":mid,
            "cookie":config.C_vip_cookie
        }
        print(api_url["C"]+"/song/url/?t="+str(time.time()))
        r=json.loads(requests.post(api_url["C"]+"/song/url/?br=320000&t="+str(time.time()),data=data).text)['data'][0]
        dic['src']=r['url']
    except: dic['src']=""
    if not dic['src']: dic['src']=''
    try:
        info=json.loads(requests.get(api_url["C"]+"/song/detail?ids="+mid).text)['songs'][0]
        dic['img']=info['al']['picUrl']
        dic['album']={'name':info['al']['name']}
        dic['artist']=[i['name'] for i in info['ar']]
        dic['name']=info['name']
    except: dic['img']=""

    try:
        dic['lrc']=json.loads(requests.get(api_url["C"]+"/lyric/?id="+mid).text)['lrc']['lyric']
        dic['tlrc']=json.loads(requests.get(api_url["C"]+"/lyric/?id="+mid).text)['tlyric']['lyric']
    except: dic['lrc']="[00:0.00]木有歌词哦"

    return dic

def cloud(mid,Type):
    if Type=="list": dic=cloud_list(mid)
    elif Type=="music": dic=cloud_music(mid)
    elif Type=="user": dic=cloud_user(mid)
    else: dic=[]

    return dic


# QQ

def qq_info(mid):
    url=api_url["Q"]+"/song?songmid="+mid
    r=requests.get(url,headers=header)
    data=json.loads(r.text,encoding="utf-8")['data']['track_info']
    dic={}
    dic['name']=data['title']
    dic['type']='music'
    dic['mid']="Q"+mid
    dic['album']={'name':data['album']['name'],'mid':data['album']['mid']}
    dic['artist']=[i['name'] for i in data['singer']]
    return dic

def qq_src(mid):
    url=api_url['Q']+'/song/url?type=m4a&id='+mid
    r=requests.get(url.format(mid),headers=header)
    try: playurl=json.loads(r.text)['data']
    except: return ""
    return playurl

def qq_img(mid):
    return "http://y.gtimg.cn/music/photo_new/T002R500x500M000"+mid+".jpg"

def qq_lrc(mid):
    url=api_url["Q"]+'/lyric?songmid={}'
    r=requests.get(url.format(mid))
    dic=json.loads(r.text,encoding="utf-8")
    try: return (dic['data']['lyric'],dic['data']['trans'])
    except: return ("[00:0.00]木有歌词哦","")

def qq(mid,Type):
    dic=qq_info(mid)
    dic["src"]=qq_src(mid)
    dic["img"]=qq_img(dic['album']['mid'])
    dic["lrc"],dic["tlrc"]=qq_lrc(mid)
    return dic

# bili

def bili_get_vid(vid): #获取视频详情
    if vid[0]=="B":r=requests.get("https://api.bilibili.com/x/web-interface/view?bvid="+vid)
    else: r=requests.get("https://api.bilibili.com/x/web-interface/view?aid="+vid[2:])
    return json.loads(r.text)

def bili_get_playinfo(vid): #获取播放链接
    r=requests.get("https://www.bilibili.com/video/"+vid)
    s=r.text
    p=s.find("playinfo__=")
    s=s[p+11:]
    p=s.find("</script>")
    s=s[:p]
    return json.loads(s)

def bili_get_audio(vid): #获取音频
    head=config.header
    head['Referer']='https://www.bilibili.com'
    dic=bili_get_playinfo(vid)
    url=dic["data"]["dash"]["audio"][0]["baseUrl"]
    filename=config.tmp_path+vid.replace("?p=","_")
    r=requests.head(url,headers=head)
    #if(int(r.headers['Content-Length'])>30*1024*1024): 0/0
    r=requests.get(url,headers=head)
    with open(filename+".m4s","wb") as f:
            f.write(r.content)
    os.system("ffmpeg -i {}.m4s -c copy {}.aac -y -v quiet".format(filename,filename))
    os.remove(filename+".m4s")
    with open(filename+".aac","rb") as f:
        bin=f.read()
    os.remove(filename+".aac")
    return save_tmp(filename+".aac",bin)

def bili_get_img(vid): #获取封面图
    info=bili_get_vid(vid)
    bin=requests.get(info['data']['pic']).content
    #f.write(requests.get(info['data']['pic']+"@233w_233h.jpg").content)
    return save_tmp(vid+".jpg",bin)

def bili_get_user_fav(uid):
    url="https://api.bilibili.com/x/v3/fav/folder/created/list?pn=1&ps=100&up_mid="+uid
    r=requests.get(url)
    return json.loads(r.text)

def bili_get_fav(mid):
    url="https://api.bilibili.com/x/v3/fav/resource/list?media_id={}&ps=20&pn=".format(mid)
    dic=json.loads(requests.get(url).text)
    mm=dic['data']['info']['media_count']-20
    c=2
    while mm>0:
        mdic=json.loads(requests.get(url+str(c)).text)
        dic['data']['medias']+=mdic['data']['medias']
        c+=1
        mm-=20
    return dic

def bili_get_user(uid):
    url="https://api.bilibili.com/x/space/acc/info?mid="+uid
    r=requests.get(url)
    return json.loads(r.text)

def bili_get_up_vid(uid):
    url="https://api.bilibili.com/x/space/arc/search?ps=50&mid="+uid+"&pn="
    c=1
    r=requests.get(url+str(c))
    dic=json.loads(r.text)
    while len(dic['data']['list']['vlist'])<dic['data']['page']['count']:
        c+=1
        r=requests.get(url+str(c))
        mdic=json.loads(r.text)
        dic['data']['list']['vlist']+=mdic['data']['list']['vlist']
    return dic

def bili(mid,Type):
    vid=mid
    if Type=="p":
        if vid.find("?")!=-1: vid=vid[:vid.find("?")]
        dic=bili_get_vid(vid)['data']
        l=[]
        for i in dic['pages']:
            x={}
            x["type"]="music"
            x["name"]=dic['title']+"-"+i["part"]
            x["mid"]="Bav"+str(dic['aid'])+"_"+str(i["page"])
            x["album"]={"name":""}
            x["artist"]=[dic["owner"]["name"]]
            l.append(x)
        return l
    elif Type=="music":
        if vid.find("_")==-1: vid+='_1'
        p=int(vid[vid.find("_")+1:])
        vid=vid[:vid.find("_")]
        info=bili_get_vid(vid)['data']
        vid='av'+str(info['aid'])

        audio_name=vid+"_"+str(p)+".aac"
        src=check_tmp(audio_name)
        if not src:
            src=bili_get_audio(vid+"?p="+str(p))
        
        img_name=vid+".jpg"
        img=check_tmp(img_name)
        if not img:
            img=bili_get_img(vid)

        dic={
            "type":"music",
            "mid":"B"+vid+'_'+str(p),
            "src":src,
            "img":img,
            "lrc":"[00:00.00]木有歌词哦",
            "album":{"name":""},
            "artist":[info['owner']['name']],
            "name":info['title']+' - '+info['pages'][min(p,len(info['pages']))-1]['part']
        }
        return dic
    elif Type=="user":
        dic=bili_get_user_fav(vid)
        try: dic=dic['data']['list']
        except: dic=[]
        for ind,i in enumerate(dic):
            x={}
            x["type"]="fav"
            x["name"]=i['title']
            x["mid"]="B"+str(i['id'])
            x["album"]={"name":""}
            x["artist"]=[]
            dic[ind]=x
        mdic=bili_get_up_vid(vid)
        if mdic['data']['page']['count']!=0:
            y={
                "type":"up",
                "name":"投稿(不支持分P自动拆分)",
                "mid":"B"+vid,
                "album":{"name":""},
                "artist":[]
            }
            dic=[y]+dic
        return dic
    elif Type=="fav":
        dic=bili_get_fav(vid)
        dic=dic['data']['medias']
        for ind,i in enumerate(dic):
            x={}
            x["type"]="p"
            x["name"]=i['title']
            x["mid"]="Bav"+str(i['id'])
            x["album"]={"name":""}
            x["artist"]=[i['upper']['name']]
            x['p']=i['page']
            dic[ind]=x
        return dic
    elif Type=="up":
        dic=bili_get_up_vid(vid)
        dic=dic['data']['list']['vlist']
        for ind,i in enumerate(dic):
            x={}
            x["type"]="p"
            x["name"]=i['title']
            x["mid"]="Bav"+str(i['aid'])
            x["album"]={"name":""}
            x["artist"]=[i['author']]
            dic[ind]=x
        return dic

# 入口函数
def main(dic):
    mid=dic['mid']
    Type=dic['type']
    
    platform=mid[0]
    mid=mid[1:]
    
    if platform=="C": res=cloud(mid,Type)
    elif platform=="Q": res=qq(mid,Type)
    elif platform=="B": res=bili(mid,Type)

    return json.dumps(res,ensure_ascii=False)