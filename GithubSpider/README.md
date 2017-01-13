##过程记录
- 安装scrapy
- 创建项目GithubSpider

        scrapy startproject GithubSpider
- 写对应代码

    - 继承了scrapy.Spider类的主方法
    
    - 定义Item,pipeline
    
    - 修改settings.py
- 运行

        scrapy crawl gitspider
  
##注意事项
- 爬虫速率需要控制，在每个lang_list迭代前都要确保sleep一定的时间
- 目前pipeline的处理是放到文件中，以后可以改为保存到Mongodb数据库中
