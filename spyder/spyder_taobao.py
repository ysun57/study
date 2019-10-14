# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 15:36:30 2019

@author: sunyue
"""

import pandas as pd
import requests
import json
import time

proxies = {


}


headers = {

    "Host": "www.zhihu.com",

    "Referer": "https://www.zhihu.com/",

    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

}

session = requests.session()
# response = session.get("https://www.zhihu.com", headers=headers, proxies=proxies,verify=False)


#构造循环爬取的函数
def format_url(base_url,num):    
    urls = []
    for i in range(0,num * 44,44):
        urls.append(base_url[:-1] + str(i))
    return urls

#解析和爬取单个网页
def parse_page(url,cookies,headers):
    result = pd.DataFrame()
    url = url.encode('utf-8')
    html = session.get(url,headers = headers, cookies = cookies, proxies=proxies,verify=False) #cookies = cookies,
    global bs
    bs = html.text
    #获取头部索引地址
    start = bs.find('g_page_config = ') + len('g_page_config = ')
    #获取尾部索引地址
    end = bs.find('"shopcardOff":true}') + len('"shopcardOff":true}')
    
    print("start is:", start)
    print("end is: ", end)
    # print(bs)
    print("*" * 10)
    
    js = json.loads(bs[start:end + 1])

    #所有数据都在这个auctions中
    for i in js['mods']['itemlist']['data']['auctions']:
        #产品标题
        product = i['raw_title'] 
        #店铺名称
        market = i['nick']
        #店铺地址
        place = i['item_loc']
        #价格
        price = i['view_price']
        #收货人数
        sales = i['view_sales']
        url = 'https:' + i['detail_url']
        r = pd.DataFrame({'店铺':[market],'店铺地址':[place],'价格':[price],
                     '收货人数':[sales],'网址':[url],'产品标题':[product]})
        result = pd.concat([result,r])
    time.sleep(5.20)
    return result

#汇总
def main():
    #爬取的基准网页（s = 0）
    base_url = 'https://www.vmall.com/product/10086085431373.html#10086494543078'
    # base_url = base_url.encode('utf-8')
    #定义好headers和cookies
    cookies = {'cookie':""}
    headers = {'Connection': 'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    


    #设置好存储结果的变量
    final_result = pd.DataFrame()

    #循环爬取5页
    for url in format_url(base_url,5):
        print(url)
        final_result = pd.concat([final_result,parse_page(url,cookies = cookies,headers = headers)])
    return final_result
    
if __name__ == "__main__":
    final_result = main()