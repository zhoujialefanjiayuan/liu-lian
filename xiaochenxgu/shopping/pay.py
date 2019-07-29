import hashlib
import random
# requests.get('http://www.dict.baidu.com/s', params={'wd': 'python'})    #GET参数实例
# requests.post('http://www.itwhy.org/wp-comments-post.php', data={'comment': '测试POST'})    #POST参数实例
#随机生成字符串
from bs4 import BeautifulSoup

def randnum():
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    c = ''
    for i in range(26):
        c += random.choice(str)
    return  ''.join(c)

def get_sign(data_dict, key):
    # 签名函数，参数为签名的数据和密钥
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
    # 组织参数字符串并在末尾添加商户交易密钥
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
    sign = md5.hexdigest().upper()  # 完成加密并转为大写
    return sign

def trans_dict_to_xml(data_dict):  # 定义字典转XML的函数
    data_xml = []
    for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
        v = data_dict.get(k)  # 取出字典中key对应的value
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml)).encode('utf-8')  # 返回XML，并转成utf-8，解决中文的问题

def trans_xml_to_dict(data_xml,findlabel='xml'):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find(findlabel)  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict

# url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
# appid =	'wx16360426dc864b7d'
# mch_id = '1537642871'
# body = 'test' #类目
# out_trade_no = '20191210' #商户订单号
# total_fee = 88 #支付金额，单位分
# spbill_create_ip = '14.23.150.211'  #终端ip
# notify_url = 'https://www.jianshu.com/p/40c7bd9388a6'  #通知回调url
# trade_type = 'JSAPI'
# nonce_str = randnum()
# key = '123456789qwertyuiopasdfghjklzxcv'
# data_params = {
#     'appid':appid,
#     'mch_id':mch_id,
#     'body':body,
#     'out_trade_no':out_trade_no,
#     'total_fee':total_fee,
#     'spbill_create_ip':spbill_create_ip,
#     'notify_url':notify_url,
#     'trade_type':trade_type,
#     'nonce_str':nonce_str,
#     'openid':'orMHc4jj3K6-IZUu7DUMN8hVzwWw'
# }
# #生成sign
# sign = get_sign(data_params, key)
# data_params['sign'] = sign
# xml_params = trans_dict_to_xml(data_params)

#访问微信支付统一下单接口
# def pay_wx(xml_params):
#     response = requests.post(url,data=xml_params)
#     get_dict = trans_xml_to_dict(response.text)
#     return get_dict
