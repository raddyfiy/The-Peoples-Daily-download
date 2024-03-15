# -*- coding: UTF-8 -*-
import requests
import re
import PyPDF2
import os
import shutil
import datetime
import sys
import argparse
import warnings
warnings.filterwarnings("ignore")
fsock = open('./log', 'w')  
sys.stderr = fsock 


headers={
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}
def download(today,partpath,newspaperpatch):
    today1=today
    today2=today[0:4]+today[5:7]+today[8:10]
    try:
        os.mkdir(newspaperpatch)
    except:
        pass
    filelist=os.listdir(newspaperpatch)
    if "People's.Daily.{}.pdf".format(today2) in filelist:
        print("该日期已经下载过了!")
        print("You alreay download this newspaper!")
        exit(0)
    coverurl="http://paper.people.com.cn/rmrb/html/{}/nbs.D110000renmrb_01.htm".format(today1)
    response=requests.get(coverurl,headers=headers)
    pagenum=re.findall("nbs",response.text)#get page number
    if response.status_code==403:
        print("你选择的日期太久远，网站不提供。只有两年之内的。")
        exit(0)
    try:
        os.mkdir('./part')
    except:
        shutil.rmtree(partpath)
        os.mkdir('./part')
    print("下载中……")
    for page in range(1,len(pagenum)+1):
        for retry in range(5):
            downtplurl="http://paper.people.com.cn/rmrb/images/{0}/{2}/rmrb{1}{2}.pdf"
            formatpage="{0:0>2}".format(page)
            downurl=downtplurl.format(today1,today2,formatpage)
            filename='rmrb{}.pdf'.format(today2+formatpage)
            response=requests.get(downurl,headers=headers)
            file=response.content
            print(len(file))
            if len(file)>1000:
                break
        with open(partpath+"/"+filename,"wb") as fn:
            fn.write(file)
def merge(partpath,newspaperpatch):
    print("合并中……")
    filelist=os.listdir(partpath)
    try:
        pdfFM=PyPDF2.PdfFileMerger(strict=False)
    except:
        pdfFM=PyPDF2.PdfMerger(strict=False)
    for file in filelist:
        fullpath=partpath+'/'+file
        filesize=os.path.getsize(fullpath) #判断文件大小，有的页本身不支持下载，发现为空则合并
        if filesize<10:
            print("第{}页网站不支持下载，已跳过".format(file[-6:-4]))
            continue

        pdfFM.append(fullpath)
    pdfFM.write(newspaperpatch+"/People's.Daily."+filelist[0][4:12]+".pdf")     #保存新文件在newspaperpatch下
    pdfFM.close()

def delete(partpath):
    shutil.rmtree(partpath)

def menu():
    pass

if __name__ == '__main__':
    menu()
    today=datetime.date.today().strftime("%Y-%m/%d")
    argc=len(sys.argv)
    if argc>1:
        argv = sys.argv[1:]
        parser = argparse.ArgumentParser(description='ArgUtils')
        parser.add_argument('-date', type=str, default=today, help="data date")
        args = parser.parse_args()
        today="{}-{}/{}".format(args.date[0:4],args.date[4:6],args.date[6:8])
        print(today)

    partpath="./part" #临时文件夹，存每一页的文件，每次运行会自动创建和删除
    newspaperpatch='./newspaper' #报纸保存位置，没有就自动创建
    
    #today="2000-04/14"     #默认下载当天的，可以命令行-date传入，也可在此手动修改日期，去掉注释按格式设置日期
    print("Date: "+today)
    download(today,partpath,newspaperpatch) #分片下载
    merge(partpath,newspaperpatch)#合并
    delete(partpath)#删除临时文件夹partpath
    print("下载成功！")








