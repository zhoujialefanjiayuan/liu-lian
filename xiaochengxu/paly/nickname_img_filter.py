import json
import requests

def get_access_token():
    id = 'wx16360426dc864b7d'
    secret = '1d0e23ca07aa746e09c774b2140d67a6'
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(id,secret)
    respone = requests.get(url).text
    access_token = json.loads(respone).get("access_token")
    return  access_token

#校验图片
def filterimg(imgurl,access_token):
    apiurl = 'https://api.weixin.qq.com/wxa/img_sec_check?access_token=' + access_token
    imgdata = requests.get(imgurl).content
    response = requests.post(apiurl,files={'media':imgdata})
    errcode = json.loads(response.text)['errcode']
    if errcode == 87014:
        return 'risky content'
    return 'ok'

#校验昵称
def filternick(nickname,access_token):
    apiurl = 'https://api.weixin.qq.com/wxa/msg_sec_check?access_token=' + access_token
    nickname = nickname.encode("utf-8").decode("latin1")
    response = requests.post(apiurl, data=json.dumps({'content':nickname},ensure_ascii=False),headers={"Content-Type":"application/json"})
    print(response)
    print(response.text)
    errcode = json.loads(response.text)['errcode']
    if errcode == 87014:
        return 'risky content'
    return 'ok'

if __name__ == '__main__':
    imgurl = 'https://gss1.bdstatic.com/-vo3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=397816053ffa828bd1239ae5c5242609/54fbb2fb43166d22ca0c87944a2309f79052d2b3.jpg'
    # print(json.dumps({'content':'法轮功'},ensure_ascii=False))
    # print(json.dumps({'content':'法轮功'}))
    print(filternick('投票工作室'))
    #print(filterimg('https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqgQOwCMYnBhR54AA7E0fIQOQWKRyMLn2YVkakp9FZ2ciaLbkJndTgfdPzkGkAWmTJkuHAW47Hmhwg/132'))

