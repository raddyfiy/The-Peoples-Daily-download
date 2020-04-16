# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import re
import PyPDF2
import os
import shutil
import datetime

headers={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}
def download(today):
    tableurl="http://paper.people.com.cn/rmrb/html/"+today+"/nbs.D110000renmrb_01.htm"
    response=requests.get(tableurl,headers=headers) 
    response.encoding = response.apparent_encoding      #解决中文乱码
    tree = etree.HTML(response.text)
    linklist=[link for link in tree.xpath("//@href") if ".pdf" in link] #找到页面所有下载链接
    linklist.pop(0)
    filenamelist=[]
    filepartpath="part"
    try:
        os.mkdir(filepartpath)
    except:
        pass
    for link in linklist:
        fileurl=tableurl+"/../"+link
        filename=re.findall(r'[a-zA-Z0-9]*\.pdf',link)[0]
        response=requests.get(fileurl,headers=headers)
        file=response.content
        fn=open("./"+filepartpath+"/"+filename,"wb")
        fn.write(file)
        fn.close()

def merge():
    filelist=os.listdir("./part/")
    pdfFM=PyPDF2.PdfFileMerger(strict=False)
    for file in filelist:
        pdfFM.append("./part/"+file)
    pdfFM.write("People's.Daily."+filelist[0][4:12]+".pdf")     #保存新文件在当前目录下
    pdfFM.close()

def delete():
    shutil.rmtree("./part")
    os.mkdir("part")

if __name__ == '__main__':
    today=datetime.date.today().strftime("%Y-%m/%d")
    #today="2020-04/14"     #手动修改日期
    download(today) #分片下载
    merge()     #合并
    delete()    #删除分片








