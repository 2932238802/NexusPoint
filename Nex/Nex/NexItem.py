# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NexItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    爬取格式
    """
    
    # boss 姓名
    boss_name = scrapy.Field()
    
    # 工作名字
    job_name = scrapy.Field()
    
    # 工资
    job_salary = scrapy.Field()
    
    # 工作标签
    job_labs = scrapy.Field()
    
    # 技能
    skills = scrapy.Field()
    
    # job
    job_exper = scrapy.Field()
    
    # 学历
    job_degree = scrapy.Field()
    
    # 公司位置
    area_district = scrapy.Field()
    business_location = scrapy.Field()
    
    # 品牌名字
    brand_name = scrapy.Field()
