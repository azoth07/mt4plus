forked from 青山大神

更是适配python3

环境需求按照requirement.txt 

pip install -r requirements.txt

~~增加tushare备份~~

~~tushare原版：https://github.com/waditu/tushare~~

使用方法：https://zhuanlan.zhihu.com/p/28845789

原版：https://github.com/flameOnYou/mt4plus
# mt4plus
一款将股市十年价格导入MT4的插件

无法使用了，由于
http://quotes.money.163.com/service/chddata.html?code=
网易数据源已经失效 --20230206

替换daily源为akshare
https://github.com/akfamily/akshare

替换hourly源为ashare
https://github.com/mpquant/Ashare

不再保留python2版本，全量更新为python3

指数代码参考：http://quote.eastmoney.com/center/hszs.html
