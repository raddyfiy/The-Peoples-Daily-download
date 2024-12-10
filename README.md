# The-Peoples-Daily-download
人民日报电子版自动下载脚本V4  
20241210更新：修复官网URL升级导致的问题。目前脚本可以兼容新旧两种情况，使用方法不变。  

20240612更新:修复某些系统下页码顺序错乱的问题  

20240315更新：增加下载失败重试机制、去除报错、兼容PyPDF2模块新老版本。  

注意：网站不是所有页都提供下载，以前的版本遇到了会报错，以后的版本检测到下载失败的页会丢弃，继续向后下载。

安装所需模块：pip3 install PyPDF2

用法：

下载当天报纸： python3 peoples_daily_download.py 

下载指定日期报纸：python3 peoples_daily_download.py -date 20221010

权限：目录下允许读写

最佳使用姿势：可以在windows建立一个计划任务，每天定时执行此脚本，报纸会自动出现在你的桌面。

--------------------------

因为报纸方要求不得将电子版应用于商业，故此脚本也不得用于商业，仅供学习与非盈利个人场合使用（虽然这个脚本下载的人肯定少，但还是写上吧emmm）
