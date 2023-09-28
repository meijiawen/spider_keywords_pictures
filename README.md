
原项目1：[关键字爬虫](https://github.com/Maryin-c/KeywordSpider_pictures_videos)

原项目2：[b站视频评论爬虫](https://github.com/Ghauster/BilibiliCommentScraper)

## 爬取各网站图片

2023.09.25 调试完成b站专栏图片、b站视频url、知乎问答文章图片的爬取

2023.09.28 用ocr提取爬取到的图片

### 1.环境配置

* !! python3.9 !!
* pip install -r requirements.txt
* 如果安装requirements报错，可以按照报错提示安装

* ocr识别安装
您的机器安装的是CUDA9或CUDA10，请运行以下命令安装
`python3 -m pip install paddlepaddle-gpu -i <https://mirror.baidu.com/pypi/simple>`

您的机器是CPU，请运行以下命令安装
`python3 -m pip install paddlepaddle -i <https://mirror.baidu.com/pypi/simple>`

### 2.基本设置

* settings.py文件中可以对存储路径、爬取页数、是否下载视频等进行设置

### 3.关键词设置

* 在'全部记录.xlsx'的表格'sheet2'中设置关键词组合，可以直接参照样例设置
* 每行第一格为关键词组合的名称（字典key），每行的其余格为当前组合每次爬取使用的关键词（字典value）
* 程序每次运行需要指定爬取的行，程序会对该行的每个格依次进行爬取，每个格中可以设置多个关键词，用空格分隔

### 4.爬取说明

* 对于涉及鼠标滚轮滑动翻页的任务，程序运行时电脑不能处理其他事务，因为需要模拟鼠标滚轮滑动，鼠标必须位于selenium打开的网页之中
* 对于微信公众号，可以在settings.py中设置快代理的隧道代理IP服务，默认为空，若不设置在爬取量较大时可能会被封IP
* 视频下载可以在settings.py中设置，请慎重选择，受网速限制可能很慢
* 可以下载bilibili与Youtube视频，抖音视频下载请使用其他项目如<https://github.com/JoeanAmier/TikTokDownloader>，快手视频无法下载

### 5.结果说明

* '全部记录.xlsx'的表格'sheet1'中记录爬取到的每条结果的详细信息
* '全部记录.xlsx'的表格'sheet3'中对所有爬取结果中出现的tag进行统计
* 图片存储在settings.py设置的各个文件夹下

## 爬取b站视频评论

1. 将要爬取评论的视频 URL 列表放入名为 video_list.txt 的文件中，每行一个 URL。
2. 参数设定

* 若要修改最大滚动次数（默认45次，预计最多爬取到920条一级评论），请在代码中修改参数MAX_SCROLL_COUNT的值。注意，滚动次数过多，加载的数据过大，网页可能会因内存占用过大而崩溃。
* 若要设定最大二级评论页码数（默认为150页），请在代码中修改参数max_sub_pages的值（若想无限制，请设为max_sub_pages = None）。建议设定一个上限以减少内存占用，避免页面崩溃。

4. 运行代码：`python Bilicomment.py`。代码使用selenium爬取数据。
5. 根据看到"请登录，登录成功跳转后，按回车键继续..."提示后，请登录 Bilibili。登录成功并跳转后，回到代码，按回车键继续。
6. 等待爬取完成。每个视频的评论数据将保存到以视频 ID 命名的 CSV 文件中， CSV 文件位于代码文件同级目录下。
7. 输出的 CSV 文件将包括以下列：'一级评论计数', '隶属关系'（一级评论/二级评论）, '被评论者昵称'（如果是一级评论，则为“up主”）, '被评论者ID'（如果是一级评论，则为“up主”）, '昵称', '用户ID', '评论内容', '发布时间', '点赞数'。
![爬取字段示例](/image/output_sample.png)
7. 输出的 CSV 文件是utf-8编码，若**乱码**，请检查编码格式（可以先用记事本打开查看）。
8. 如果有视频因为错误被跳过，将会被记录在代码同级文件夹下的video_errorlist.txt中。

## ocr提取图片文字

`python ocr.py`
