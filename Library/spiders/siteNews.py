from datetime import datetime
import scrapy
from model.models import Article
from model.repositories.website_repository import WebsiteRepository
from model.repositories.article_repository import ArticleRepository


class siteNews(scrapy.Spider):
    website = WebsiteRepository.get_by_libelle("siteNews")
    name = website.libelle
    
    def start_requests(self):
        urls = [
            self.website.link
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(f'\033[95mStart {self.website.libelle}\033[0m')
        
        for div in response.css("div.grid-item-inner"):
           
            title = div.css("h4::text").get()
            print('\033[92mTitle:\033[0m', title)
            link = div.css("a::attr(href)").get()
            print('\033[92mLink:\033[0m', link)
            description = div.css("p::text").get()
            print('\033[92mDescription:\033[0m', description)
            
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
