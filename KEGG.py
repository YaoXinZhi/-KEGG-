#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:29:09 2019

@author: yaoxinzhi
"""

import requests
from bs4 import BeautifulSoup
import os
import time

def getHTMLText(url):
    # 获得 url 的源代码
    try:
        # 该结构是防止解析失败
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def save_img(img_url, out):
    # 根据 img_url 得到图片名字
    img_name = img_url.split('/')[-1]
    
    # 解析 img_url 
    response = requests.get(img_url)
    # 得到图片二进制储存
    img = response.content
    # 写入文件 即保存图片
    with open ('{0}/{1}'.format(out, img_name), 'wb') as wf:
        wf.write(img)
        
#    print ('save done')

def url_parse(url):
    # 获得 url 的源代码
    html = getHTMLText(url)
    # 解析源代码 为 soup 结构
    soup = BeautifulSoup(html, 'html.parser')
    
    # 根据对url人工观察找到图片所处位置的 特征属性
    img = soup.find(attrs={'name':'pathwayimage'}).attrs['src']
    # 该url 只给了 图片url后半部分 应该kegg都是这么做的 其他网站再分析
    img_url = 'http://www.kegg.jp' + img
    
    return img_url

def read_file(url_file):
    
    url_list = []
    with open(url_file) as f:
        # 删除标题行
        line = f.readline()
        # 把url都存下来
        for line in f:
            url = line.strip().split(',')[-1]
            url_list.append(url)
    return url_list

def main(kegg_file, out):
    # 读取 所有url
    url_list = read_file(kegg_file)
    err_list = []
    
    # 遍历 计时
    count = 0
    start = time.time()
    for url in url_list:

        try:
            # 解析url 下载图片
            img_url = url_parse(url)
            save_img(img_url, out)
            count += 1
        except:
            # 报错了 存下错误的url
            err_list.append(url)
            continue
        # 每下载50张报告下用时
        if count % 50 == 0 :
            end = time.time()
            # 休息60秒
            time.sleep(60)
            print ('download img: {0} / {2}, time: {1}'.format(count, end-start, len(url_list)))
    print ('download img: {0} / {2}, time: {1}'.format(count, end-start, len(url_list)))

    # 把下载失败的url存下来
    with open('err.log', 'w') as wf:
        for err in err_list:
            wf.write('{0}\n'.format(err))
    
    print ('下载 成功： {0} /{1}, 失败 {2} /{1}'.format(count, len(url_list), len(err_list)))
        
if __name__ == '__main__':
    
    # 你给我的文件转出csv格式 就是通过逗号分割的 要保证和代码在同一个目录下
    kegg_file = './kegg_pathway.csv'
    
    # 网页的 url 要先去看网页源代码结构 自己要爬的内容在哪个结构里
    # javascript 写的网页难爬
    url = 'http://www.kegg.jp/kegg-bin/show_pathway?map00430/C00245%09green/C00022%09green'
    # 要储存的文件夹
    out = './KEGG_img'
    
    # 判断文件下是否存在
    if not os.path.exists(out):
        os.mkdir(out)
    
    main(kegg_file, out)