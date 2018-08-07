# caoliu_1024_dagaier_spider
爬取草榴论坛"达盖尔的旗帜"分类下的主题图片<br>


运行：
=========
linux:<br>
python ./达盖尔.py<br>
or<br>
windows:<br>
python .\达盖尔.py<br>


环境准备：
=========
windows：<br>
---------
pip install pyquery<br>
pip install -U requests[socks]==2.12.0<br>

linux:<br>
---------
pip install pyquery<br>
pip install requests[socks]<br>


修改参数：<br>
=========
请修改为自己SS or SSR监听的端口<br>
proxy={"http":"socks5://127.0.0.1:1088","https":"socks5://127.0.0.1:1088"}<br>
<br>
请合理设置线程数<br>
work_manager=ThreadManager(8)<br>
<br>
请修改需要爬取的主题分页数<br>
while offset<10: #主题列表分页数<br>
<br>
