import scrapy

class SecurityWeekSpider(scrapy.Spider):
    name = "securityweek"
    allowed_domains = ["securityweek.com"]
    start_urls = ["https://www.securityweek.com/"]

    def parse(self, response):
        
        print(response.status)
        print(response.request.headers)
        
        articles = response.css("article.zox-art-wrap")
        for article in articles:
            title = article.css("div.zox-art-title h2::text").get()
            url = article.css("div.zox-art-title a::attr(href)").get()
            summary = article.css("p.zox-s-graph::text").get()
            date = article.css("time.post-date::attr(datetime)").get()

            yield {
                "title": title,
                "url": url,
                "summary": summary,
                "date": date,
                "source": "SecurityWeek",
            }

            # Optionnel : aller sur l'article complet si tu veux Trafilatura ensuite
            # yield response.follow(url, self.parse_article)
            

    # def parse_article(self, response):
    #     # Trafilatura ou analyse manuelle du contenu ici
    #     pass
