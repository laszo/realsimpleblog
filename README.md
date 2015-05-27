realsimpleblog
==============

A static blog site generator, written in Python. Write your weblog entries directly with your editor in Markdown.

一个特别简单（但是能用）的静态博客系统，使用markdown格式（特别好学）写博客，生成静态页面，托管在任何地方（比如Github Pages）！

如何使用
-------
1. 安装python环境，windows、linux、mac均可。并安装python库yaml、markdown、jinja2。

2. 下载realsimpleblog，点击如下连接：[下载zip包](https://github.com/laszo/realsimpleblog/archive/master.zip)，并解压。

3. 开始写博客。在content目录下，新建markdown类型的文件，使用你喜欢的编辑器写吧。如果你不熟悉markdown，可以参看[Markdown 语法说明 (简体中文版)](http://wowubuntu.com/markdown/)，或。[作业部落](https://www.zybuluo.com)提供了在线的markdown编辑器。我向你保证，markdown标记是最最简单易学的，花几分钟时间学会以后，物超所值。
如果你暂时不想写新文章，可以跳到第四步，因为content文件夹中已经附带了一篇“helloworld.markdown”。让你的新博客内容不会为空。

4. 修改博客标题。打开main.py文件，修改的第14行：
```
blogtitle = u'This is the realSimpleBlog.'
```
把 This is the realSimpleBlog. 改为你想要的标题。

4. 打开命令行终端，进入realsimpleblog目录，输入
```
python main.py
```
我们看到，一个新的静态站点已经生成了。可以打开目录中的index.html 查看博客的首页。

5. 启动本地http服务器，可以在本地预览站点。输入：
```
python -m Httpserver
```
然后打开：[http://127.0.0.1:8000/](http://127.0.0.1:8000/) 就可以看到你的博客。

6. 发布站点。你可以把站点发布到[GitHubPages](https://pages.github.com/)上面，或者其他任何可以托管静态页面的网站上。
