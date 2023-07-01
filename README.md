# B站弹幕可视化分析


同济大学 2023 年《大数据与人工智能》期末大作业

本项目主要完成了以下工作：

1. 数据爬取与处理：爬取三个关于比亚迪的视频，并对获取的弹幕数据进行了去重等操作。最终，获得了29081 条有效数据。
2. 弹幕情感分析：利用 IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment 模型，对弹幕数据进行情感分析。该模型能够判断每条弹幕的情感倾向，表现为积极或消极，同时给出具体的情感得分。
3. 可视化分析：本项目一共绘制了五个图表，包括弹幕发送时间的折线图、不同态度的弹幕数量饼图、不同态度的弹幕分数核密度估计图、关键词词云图以及视频弹幕数量随时间变化的折线图。这五张图表能够直观地观察到弹幕数量变化的趋势、观众的情感态度分布、弹幕分数的分布等。

三个关于比亚迪的视频：

https://www.bilibili.com/video/BV11G4y127LW

https://www.bilibili.com/video/BV1nW4y1579E

https://www.bilibili.com/video/BV1UG411g7Hb

![image-20230603131245426](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/image-20230603131245426.png)

### 文件结构

```shell
.
├── IDEA-CCNL  # 存放与bert模型相关的文件
│   ├── config.json  
│   ├── pytorch_model.bin
│   └── vocab.txt
├── README.md
├── analysis.ipynb  # 情感分析和可视化
├── cn_stopwords.txt  # 中文停用词
├── data  # 爬取的数据，new_xxx 表示取重后的数据
│   ├── BV11G4y127LW.csv
│   ├── BV1UG411g7Hb.csv
│   ├── BV1nW4y1579E.csv
│   ├── new_BV11G4y127LW.csv
│   ├── new_BV1UG411g7Hb.csv
│   └── new_BV1nW4y1579E.csv
├── dm.proto  # 用于数据传输的协议
├── dm_pb2.py  # 由 dm.proto 编译生成的 python 文件
├── images  # 可视化结果图片
│   ├── video1
│   ├── video2
│   ├── video3
│   └── 截屏2023-06-02 18.19.34.png
├── mask.png  # 词云图模版
├── requirements.txt
├── spider.py  # 爬虫
```

## 运行指南

### 环境配置

```shell
# 创建一个 conda 环境
conda create -n transformer python=3.8
# 激活环境
conda activate transformer  

# 安装外部代码库
pip install -r requirements.txt
```

### 运行测试

项目 `spider.py` 文件包含爬虫代码，基于 `requests` 和 `lxml` 等库，直接运行下面指令进行爬取：

```shell
python ./spider.py
```

![截屏2023-06-03 13.09.01](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/%E6%88%AA%E5%B1%8F2023-06-03%2013.09.01.png)

红色方框内容需要自行输入。

项目 `analysis.ipynb` 文件包含情感分析和可视化分析代码，基于 `transformers` 和 `matplotlib` 等库，可以去文件内容查看具体内容。

## 效果

### 爬取过程

![截屏2023-06-02 18.19.34](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/%E6%88%AA%E5%B1%8F2023-06-02%2018.19.34.png)

### 爬取结果

![截屏2023-06-02 21.37.58](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/%E6%88%AA%E5%B1%8F2023-06-02%2021.37.58.png)

### 情感分析结果

图中最右边两列

![截屏2023-06-02 19.58.39](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/%E6%88%AA%E5%B1%8F2023-06-02%2019.58.39-20230603131300121.png)

### 可视化结果

弹幕增长趋势图

![f4a7ebd9-8db9-49d4-8d66-26814c1964e8](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/f4a7ebd9-8db9-49d4-8d66-26814c1964e8.png)



弹幕态度分布图

![aa118f01-c33c-4cc5-825d-d761ad6eee28](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/aa118f01-c33c-4cc5-825d-d761ad6eee28.png)

不同态度的弹幕分数分布图

![13eebd26-80c5-414c-a8c2-d874fbb35439](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/13eebd26-80c5-414c-a8c2-d874fbb35439.png)

词云图

![acd3826f-acc5-475d-afa5-69a2998504ac](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/acd3826f-acc5-475d-afa5-69a2998504ac.png)

以1min为间隔弹幕数量统计折线图

![bf885d4b-69d8-4941-8483-22f44199f70a](https://lei-1306809548.cos.ap-shanghai.myqcloud.com/Obsidian/bf885d4b-69d8-4941-8483-22f44199f70a.png)

## 鸣谢

[1]孙洋,冷冠男.基于BERT模型的网络舆情情感分析——以上海疫情为例[J].应用数学进展,2022,11(8):5053-5061

[2]Wang, Junjie et al. “Fengshenbang 1.0: Being the Foundation of Chinese Cognitive Intelligence.” *ArXiv* abs/2209.02970 (2022): n. pag.

[3]郑飏飏,徐健,肖卓.情感分析及可视化方法在网络视频弹幕数据分析中的应用[J].现代图书情报技术,2015,No.264(11):82-90.

[4]高旭.基于弹幕的视频高潮探测分析[J].电脑知识与技术,2020,16(06):209-210.DOI:10.14004/j.cnki.ckt.2020.0707.

[5]姚宗豪. 面向B站弹幕情感分析系统的设计和实现[D].山东大学,2021.DOI:10.27272/d.cnki.gshdu.2021.006956.

https://github.com/SocialSisterYi/bilibili-API-collect

