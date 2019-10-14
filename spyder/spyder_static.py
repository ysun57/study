# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 09:24:59 2019

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
    base_url = 'https://s.taobao.com/search?q=%E6%B4%97%E5%8F%91%E6%B0%B4&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&sort=sale-desc&bcoffset=0&p4ppushleft=%2C44&s=0'
    # base_url = base_url.encode('utf-8')
    #定义好headers和cookies
    cookies = {'cookie':'dnk=qwertyasdfgh1993; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie15=Vq8l%2BKCLz3%2F65A%3D%3D; uc3=lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dBy3KzvOfiCDxV5lI%3D&nk2=EuLXbC20SpeuLH%2BbRgeqIQ%3D%3D&id2=UoezTUxuy9AttA%3D%3D; tracknick=qwertyasdfgh1993; lid=qwertyasdfgh1993; _l_g_=Ug%3D%3D; unb=1672220134; lgc=qwertyasdfgh1993; cookie1=VFQgT%2FPNL3ed6rGI5rKeTxr9xPLQEJgBsTqt%2BSsrad8%3D; login=true; cookie17=UoezTUxuy9AttA%3D%3D; cookie2=1e1f25c5d8cb96b1774462fcac7747de; _nk_=qwertyasdfgh1993; t=6ccdf8273a3480b6dd41529f695baecb; sg=34d; csg=483cb024; enc=AR9RY0E5R61ojIx9zMmttZouayquTegTuhX9e14EhDt84sqIaXNqSQ%2B0jperQXau1xsWUAWAx4fENByilq6ucA%3D%3D; _tb_token_=f1ed1b3671b13; pnm_cku822=098%23E1hve9vUvbpvUvCkvvvvvjiPRF5ZgjimR2qU1jYHPmPw6jECR2Mw0j1PPsz91jnC2QhvCvvvMMGCvpvVvvpvvhCvmphvLCCOMvvjnzc6D76fdeQEfa3lYCyXwDTxfwLhdigfBdmxfwofd56OfwLvaXwXaZRQD7zh58tYLYLZeE7rejwu%2BExr1EuKNpRxfwLyd34tvpvIvvvvvhCvjvUvvUnvphvWEQvv96CvpC29vvm2phCvhhvvvUnvphvppUyCvvOUvvVva68ivpvUvvmvn%2BWQcE9tvpvhvvvvv8wCvvpvvUmm; cna=0DZkFbEyQjcCAWfa2HzEeopW; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=30914; whl=-1%260%260%260; x=__ll%3D-1%26_ato%3D0; l=cBjjkqGuqsNfDj2QKOfZKurza779wpAjXsPzaNbMiIB193BLZdvCrHwI91Nv63QQE95frEtzA9rOJRUX7Ya38EGTnBwAKXIpB; isg=BNbWatIPl_CYkqNVkr3gfTI9J4zYdxqxfEgJjkAx872QA0-dpATkwE-xm99KqxLJ'}
    headers = {'Connection': 'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    


    #设置好存储结果的变量
    final_result = pd.DataFrame()

    #循环爬取5页
    for url in format_url(base_url,5):
        final_result = pd.concat([final_result,parse_page(url,cookies = cookies,headers = headers)])
    return final_result
    
if __name__ == "__main__":
    final_result = main()