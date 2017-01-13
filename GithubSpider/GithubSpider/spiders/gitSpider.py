from urllib import quote
import scrapy
from GithubSpider.items import GithubspiderItem, LangTypeItem

class GitSpider(scrapy.Spider):
    name = 'gitspider'
    count = 0

    def __init__(self):
       
        self.lang_list = ['Python', 'Pascal', 'Java', 'JavaScript', 'HTML', 'C++', 'C', 'C#', 'CSS',\
         'PHP', 'Perl', 'R', 'Haskell', 'Common Lisp', 'Lua', 'Objective-C', \
         'Swift', 'Ruby', 'Scheme', 'Shell', 'Tex', ]
         
        #self.lang_list = ['PHP']
        self.head = {'Connection':'keep-alive',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        

    def start_requests(self):
        for lang in self.lang_list:
            url_lang = quote(lang)
            url = 'https://github.com/search?l=' + url_lang + '&o=desc&q=' + url_lang+\
            '&s=stars&type=Repositories&utf8=%E2%9C%93'
            yield scrapy.Request(url, callback=self.parse, headers=self.head)

    def parse(self, response):

        self.count += 1
        
        #use chrome dev tools -'copy xpath' to get the xpath,it's easy though a little long
        lang_name = response.xpath('//*[@id="js-pjax-container"]/div[2]/div/div[1]/ul/li[1]/a/text()').extract()[1].strip()

        for repo in response.xpath('//li[@class="col-12 d-block width-full py-4 border-bottom public source"]'):
            #type of repo is Selector
            item = GithubspiderItem()
            item['lang_name'] = lang_name

            s_url = repo.xpath('div[1]/h3/a/@href').extract_first()
            item['url'] = 'https://github.com'+s_url
            item['repo_name'] = s_url[1:]
            #the extract() result of star_count and fork_count is a list contains a '\n' ,that is extract_first()
            item['star_count'] = repo.xpath('div[2]/a[1]/text()').extract()[1].strip()
            item['fork_count'] = repo.xpath('div[2]/a[2]/text()').extract()[1].strip()
            
            item['last_update'] = repo.xpath('div[2]/relative-time/@datetime').extract_first().strip()
            
            #must return an Item or Request object
            yield item

        next_page = response.xpath('//div[@id="js-pjax-container"]/div[2]/div/div[2]/div[2]/div/a[@class="next_page"]/@href').extract_first()
        
        #scrape 6 pages
        if next_page is not None and self.count < 6:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse, headers=self.head, cookies=self.cookie)
