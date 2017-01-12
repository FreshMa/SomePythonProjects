# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class GithubspiderPipeline(object):

    def process_item(self, item, spider):
    '''
    store the items into the respective file
    '''
        lang = item['lang_name']
        print 'lang name%s'%lang
        line = json.dumps(dict(item))
        filename = lang+'.txt'

        with open(filename,'a') as f:
            f.write(line+'\n')

        return item
