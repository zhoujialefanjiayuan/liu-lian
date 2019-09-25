import base64
import hashlib
import re

import requests

# 顾客编码(clientCode)： LLYLKJSZ
# 您的应用 校验码 (checkWord) ： STGuVhBlDznxZbvyFFSxP5fdsyH8geFq
clientCode = 'LLYLKJSZ'
checkWord = 'STGuVhBlDznxZbvyFFSxP5fdsyH8geFq'


def compose_addorderxml(order_data):
    xml = """
    <Request service = "OrderService" lang = "zh-CN" > 
    <Head>{clientCode}</Head>
    <Body>
    <Order 
    	orderid="{orderid}"
    	j_company="深圳榴莲科技有限公司" 
    	j_contact="张先生" 
    	j_tel="075526806888" 
    	j_mobile="075526806888" 
    	j_province="广东省" 
    	j_city="深圳市"
    	j_county="福田区"
    	j_address="福田区南山街道滨江社区滨河大道2001号7楼08-09单元" 
    	d_contact="{getman}" 
    	d_tel="1235" 
    	d_mobile= "{order_phone}"
    	d_province="{d_province}"
    	d_city="{d_city}"
    	d_county="{d_county}"
    	d_address="{d_address}" 
    	express_type="1" 
    	pay_method="1" 
    	custid="7550069706" 
    	parcel_quantity="1" 
    	is_docall="2"
    	sendstarttime="{sendtime} 10:30:00"  
    	remark="{goodname}"
        is_unified_waybill_no="1">
    </Order>
    </Body> 
    </Request>
    """.format(clientCode=clientCode, orderid=order_data['order_num'], getman=order_data['getman'],
               order_phone=order_data['order_phone'],
               d_province=order_data['d_province'], d_city=order_data['d_city'], d_county=order_data['d_county'], d_address=order_data['d_address'],
               goodname=order_data['goodname'],sendtime=order_data['sendtime'])
    return xml


def compose_delorderxml(order_num):
    p = """<Request service="OrderConfirmService" lang="zh-CN">
    <Head>{clientCode}</Head>
    <Body>
    <OrderConfirm
    orderid="{order_num}"
    dealtype="2">
    </OrderConfirm>
    </Body>
    </Request>""".format(clientCode=clientCode, order_num=order_num)
    return p


def compose_verifyCode(xml):
    params_str = xml + checkWord
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
    sign = md5.digest()
    code = base64.b64encode(sign)
    return code


def response_to_dict(str):
    try:
        resdata = re.search(r'<Order.*?>', str).group()[1:-1].split(' ')[1:]
        res_dict = {}
        for i in resdata:
            l = i.split('=')
            res_dict[l[0]] = l[1].strip('""')
        return res_dict
    except:
        resdata = re.search(r'<ERROR .*?</ERROR>', str).group()
        return resdata


# 生成订单
def addorder(xml):
    url = 'http://bsp-oisp.sf-express.com/bsp-oisp/sfexpressService'
    code = compose_verifyCode(xml)
    res = requests.post(url, data={'xml': xml, 'verifyCode': code}).text
    res_data = response_to_dict(res)
    return res_data


def getstatu(order_num):
    url = 'http://bsp-oisp.sf-express.com/bsp-oisp/sfexpressService'
    p = """
    <Request service="OrderSearchService"  lang="zh-CN">
    <Head>{clientCode}</Head>
    <Body>
    <OrderSearch orderid="{order_num}"/>
    </Body>
    </Request>""".format(clientCode=clientCode, order_num=order_num)
    code = compose_verifyCode(p)
    res = requests.post(url, data={'xml': p, 'verifyCode': code}).text
    print(res)
    data = response_to_dict(res)
    return data


# 删除订单
def fengqiaodelorder(xml):
    url = 'http://bsp-oisp.sf-express.com/bsp-oisp/sfexpressService'
    code = compose_verifyCode(xml)
    res = requests.post(url, data={'xml': xml, 'verifyCode': code}).text
    res_data = response_to_dict(res)
    return res_data


# 查询路由
def query_xml(order_num):
    p = """<Request service='RouteService' lang='zh-CN'>
    <Head>{clientCode}</Head>
    <Body>
    <RouteRequest
    tracking_type='1'
    method_type='1'
    tracking_number='{order_num}'/>
    </Body>
    </Request>""".format(clientCode=clientCode, order_num=order_num)
    return p

def queryorder(xml):
    url = 'http://bsp-oisp.sf-express.com/bsp-oisp/sfexpressService'
    code = compose_verifyCode(xml)
    r = requests.post(url, data={'xml': xml, 'verifyCode': code}).text
    print('查查接口',r)
    res = re.findall(r"<Route.*?>", r, re.S)
    list_data = []
    for i in res:
        ds = re.findall(r' .+?=".*?"', i)
        obj = {}
        for d in ds:
            item = d.split('=')
            obj[item[0].strip(' ')] = item[1].strip('""')
        list_data.append(obj)
    return list_data


if __name__ == '__main__':
    obj = {'couponid': "",
           'getman': "ggfd",
           'goodimg': "http://liulian.szbeacon.com/1.png",
           'goodname': "2017周笔畅Not Typical全纪录册",
           'goodnum': "1",
           'goodprice': "100.00",
           'order_end_time': "2019-06-21 14:16:04",
           'order_location': "广东,深圳,福田区,鹿丹村一号",
           'order_num': "KFYZA4RBQDREIMMEAVUZHI1HHq",
           'order_phone': "fdgfd",
           'order_start_time': "2019-06-21 14:06:04",
           'order_true_pay': "0.01",
           'order_user': "orMHc4jj3K6-IZUu7DUMN8hVzwWw489",
           'type': 1,
           'zhoubianid': 2, }
    xml = compose_addorderxml(obj)
    #response = addorder(xml)
    print(xml)

    # # res = {'filter_result': '"2"', 'destcode': '"755"', 'mailno': '"444016218022"', 'origincode': '"755"',
    # #        'orderid': '"KFYZA4RBQDREIMMEAVUZHI1HHu"'}
    # delxml = compose_delorderxml('KFYZA4RBQDREIMMEAVUZHI1HHy')
    # res = delorder(delxml)
    # print(res)
    # xml = query_xml("KFYZA4RBQDREIMMEAVUZHI1HHq")
    # queryorder(xml)





