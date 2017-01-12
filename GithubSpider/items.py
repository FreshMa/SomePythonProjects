# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy import Item
from scrapy import Field

class GithubspiderItem(Item):

    lang_name = Field()
    repo_name = Field()
    url = Field()
    star_count = Field()
    fork_count = Field()
    last_update = Field()
 
