from datetime import datetime
import scrapy
from model.models import Article
from model.repositories.website_repository import WebsiteRepository
from model.repositories.article_repository import ArticleRepository


class francopresse(scrapy.Spider):
    website = WebsiteRepository.get_by_libelle("francopresse")
    name = website.libelle
    
    def start_requests(self):
        urls = [
            self.website.link
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(f'\033[95mStart {self.website.libelle}\033[0m')
        print(response.css('article a').getall())
        for article in response.css('article').getall():
            print(article.css("a::attr(href)").get())
            yield scrapy.Request(url=article.css("a::attr(href)").get(), callback=self.parse_article)
          
        
    def parse_article(self, response):
        print(f'\033[95mStart {self.website.libelle}\033[0m')
        title = response.css("h1.full-article__title::text").get()
        print("title: ", title)
        link = response.url
        print("link: ", link)
        description ="".join(response.css('article p::text').getall())
        print("description: ", description)
        
        if(ArticleRepository.get_by_link(link)):
            print(f'\nWarning: article ignored(already exists): {title}({link})')
        else:
            article = Article(title=title, link=link, description=description, created_at=f"{datetime.now().date()}",
                            website_id=self.website.id)
            ArticleRepository.store(article)
            print(f'\nSuccess: article saved: {title}({link})')
        print(f'\nEnd {self.website.libelle} with link:', f'{response.url}\n')
        # nextLink = response.css('a[rel="next"]::attr(href)').get()
        # if nextLink:
        #     yield scrapy.Request(url=nextLink, callback=self.parse)
        print(f'\033[91mEnd {self.website.libelle}\033[0m')
