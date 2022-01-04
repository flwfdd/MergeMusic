#from websocket import create_connection
import requests
import base64
import json
import os

head={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69',
    'Referer': 'https://www.bilibili.com'
    }

def get_vid(vid): #获取视频详情
    if vid[0]=="B":r=requests.get("https://api.bilibili.com/x/web-interface/view?bvid="+vid)
    else: r=requests.get("https://api.bilibili.com/x/web-interface/view?aid="+vid[2:])
    return json.loads(r.text)

def get_online(aid,cid): #获取在线人数
    aid=str(aid)
    cid=str(cid)
    wsurl="wss://broadcast.chat.bilibili.com:7823/sub"
    base1=[""]*4
    base1[1]="AAAAXQASAAEAAAAHAAAAAQAA"
    base1[2]="AAAAWwASAAEAAAAHAAAAAQAA"
    base1[3]="AAAAXAASAAEAAAAHAAAAAQAA"
    base2="AAAAIQASAAEAAAACAAAABgAAW29iamVjdCBPYmplY3Rd"
    send1='{"room_id":"video://'+aid+'/'+cid+'","platform":"web","accepts":[1000]}'
    base1[0]=base64.b64encode(send1.encode('utf-8')).decode('utf-8')
    for i in range(1,4):
        try:
            ws = create_connection(wsurl)
            ws.send(base64.b64decode(base1[i]+base1[0]))
            r=ws.recv()
            break
        except: continue
    ws.send(base64.b64decode(base2))
    r=ws.recv()
    ws.close()
    n=json.loads(str(r[18:],'utf-8'))['data']['room']['online']
    return n

def get_playinfo(vid):
    r=requests.get("https://www.bilibili.com/video/"+vid)
    s=r.text
    p=s.find("playinfo__=")
    s=s[p+11:]
    p=s.find("</script>")
    s=s[:p]
    return json.loads(s)

def get_audio_url(vid):
    dic=get_playinfo(vid)
    try: return dic["data"]["dash"]["audio"][0]["baseUrl"]
    except: return ""

def get_audio(vid):
    url=get_audio_url(vid)
    filename="/tmp/"+vid.replace("?p=","_")
    if not os.path.exists(filename+".aac"):
        r=requests.head(url,headers=head)
        if(int(r.headers['Content-Length'])>30*1024*1024): 0/0

        r=requests.get(url,headers=head)
        with open(filename+".m4s","wb") as f:
            f.write(r.content)
        os.system("ffmpeg -i {}.m4s -c copy {}.aac -y -v quiet".format(filename,filename))
    return filename+".aac"

def get_img(vid):
    info=get_vid(vid)
    with open("/tmp/"+vid+".jpg","wb") as f:
        f.write(requests.get(info['data']['pic']).content)
        #f.write(requests.get(info['data']['pic']+"@233w_233h.jpg").content)
    return "/tmp/"+vid+".jpg"

def get_user_fav(uid):
    url="https://api.bilibili.com/x/v3/fav/folder/created/list?pn=1&ps=100&up_mid="+uid
    r=requests.get(url)
    return json.loads(r.text)

def get_fav(mid):
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

def get_user(uid):
    url="https://api.bilibili.com/x/space/acc/info?mid="+uid
    r=requests.get(url)
    return json.loads(r.text)

def get_up_vid(uid):
    url="https://api.bilibili.com/x/space/arc/search?ps=100&mid="+uid+"&pn="
    c=1
    r=requests.get(url+str(c))
    dic=json.loads(r.text)
    while len(dic['data']['list']['vlist'])<dic['data']['page']['count']:
        c+=1
        r=requests.get(url+str(c))
        mdic=json.loads(r.text)
        dic['data']['list']['vlist']+=mdic['data']['list']['vlist']
    return dic
