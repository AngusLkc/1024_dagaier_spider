# caoliu_1024_dagaier_spider
爬取草榴论坛"达盖尔的旗帜"分类下的主题图片<br>

https://raw.githubusercontent.com/cary-zhou/caoliu_1024_dagaier_spider/master/dagaier.zip

运行：
=========
linux:<br>
python ./达盖尔.py<br>
or<br>
windows:<br>
python .\达盖尔.py<br>


环境准备：
=========
windows or Linux<br>
---------
pip install pyquery<br>
pip install requests<br>
pip install -U requests[socks]<br>


修改参数：<br>
=========
修改代理地址为自己SS或SSR监听的地址端口<br>
proxy={"http":"socks5h://127.0.0.1:1088","https":"socks5h://127.0.0.1:1088"}<br>
<br>
请合理设置线程数<br>
work_manager=ThreadManager(8)<br>
<br>
请修改需要爬取的主题分页数<br>
while offset<10: #主题列表分页数<br>
<br>

预编译二进制：
=========
压缩包：dagaier.zip，是windows下直接可双击执行的exe文件，<br>
使用时需要解压exe可执行文件出来，不要在zip压缩管理器内直接双击执行，免得爬虫运行完了找不到肉。<br>
然后启动你的SSR代理->选项设置->本地端口,填1088，因为程序内手写了通过本地socks5h://127.0.0.1:1088爬梯。<br>
如图：<br>
![image](https://github.com/cary-zhou/caoliu_1024_dagaier_spider/raw/master/snapshot/snap1.png)
<br>爬取到的资源放在exe同级目录的images文件夹下，每个帖子每个文件夹分开存放，文件夹名就是帖子标题名。<br>
