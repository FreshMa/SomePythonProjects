BOT_NAME = 'GithubSpider'

SPIDER_MODULES = ['GithubSpider.spiders']
NEWSPIDER_MODULE = 'GithubSpider.spiders'

#set the item pipelines,must be dict type
ITEM_PIPELINES = {'GithubSpider.pipelines.GithubspiderPipeline':1}
#not follow the bot policy
ROBOTSTXT_OBEY = False
