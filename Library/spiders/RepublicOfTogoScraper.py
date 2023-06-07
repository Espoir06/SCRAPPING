from datetime import datetime
import scrapy
from model.models import Article
from model.repositories.website_repository import WebsiteRepository
from model.repositories.article_repository import ArticleRepository


class RepublicOfTogoScraper(scrapy.Spider):
    name = "republicoftogo_scraper"

    def start_requests(self):
        urls = [
            "https://www.republicoftogo.com/"  # URL du site Republic of Togo
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print('\033[92mStart scraping Republic of Togo\033[0m')

        for article in response.css("article.post"):
            title = article.css("h2.entry-title a::text").get()
            print('\033[92mTitle:\033[0m', title)

            link = article.css("h2.entry-title a::attr(href)").get()
            print('\033[92mLink:\033[0m', link)

            description = article.css("div.entry-content p::text").get()
            print('\033[92mDescription:\033[0m', description)

            if ArticleRepository.get_by_link(link):
                print(f'\nWarning: Article ignored (already exists): {title} ({link})')
            else:
                article = Article(title=title, link=link, description=description, created_at=f"{datetime.now().date()}",
                                website_id=self.website.id)
                ArticleRepository.store(article)
                
                print(f'\nSuccess: Article saved: {title} ({link})')

        print('\033[92mEnd scraping Republic of Togo with link:\033[0m', response.url)

