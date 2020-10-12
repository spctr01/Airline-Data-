import scrapy
import pandas as pd
import re


class LucasSpider(scrapy.Spider):
    name = 'lucas'

    data = pd.read_csv('spiders/data.csv')
    start_urls = data['url'].unique().tolist()


    def parse(self, response):
        company_name = response.xpath('//span[@class="multi-size-header__big"]/text()').extract_first()
        company_logo = response.xpath('//img[@class="business-unit-profile-summary__image"]/@src').extract_first()
        company_website = response.xpath('//a[@class="badge-card__section badge-card__section--hoverable company_website"]/@href').extract_first()
        comments = response.xpath("//p[@class='review-content__text']")
        comments = [comment.xpath('.//text()').extract() for comment in comments]
        comments = [[c.strip() for c in comment_list] for comment_list in comments]
        comments = [' '.join(comment_list) for comment_list in comments]

        ratings = response.xpath("//div[@class='star-rating star-rating--medium']//img/@alt").extract()
        ratings = [int(re.match('\d+', rating).group(0)) for rating in ratings]

        for comment, rating in zip(comments, ratings):
            yield {
                'comment': comment,
                'rating': rating,
                'url_website': response.url,
                'company_name': company_name,
                'company_website': company_website,
                'company_logo': company_logo
            }

        next_page = response.css('a[data-page-number=next-page] ::attr(href)').extract_first()
        if next_page is not None:
            request = response.follow(next_page, callback=self.parse)
            yield request
