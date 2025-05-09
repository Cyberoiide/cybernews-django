import scrapy
import trafilatura


class CyberSecurityNewsSpider(scrapy.Spider):
    name = "cybersecuritynews"
    allowed_domains = ["cybersecuritynews.com"]
    start_urls = ["https://cybersecuritynews.com/"]

    def parse(self, response):
        # Récupère tous les liens vers les articles de la page
        article_links = response.css("div.td_module_10 h3.entry-title a::attr(href)").getall()
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        # Pagination
        next_page = response.css("a.td_ajax_load_more_js::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        content = trafilatura.extract(response.text)
        if not content:
            self.logger.warning(f"❌ Failed to extract content for {response.url}")
            return

        yield {
            "title": response.css("h1.entry-title::text").get(),
            "url": response.url,
            "author": response.css(".td-post-author-name a::text").get(),
            "content": content,
            "summary": response.css("meta[name='description']::attr(content)").get(default="")[:500],
            "tags": "",  # tu pourras améliorer ça plus tard si besoin
            "score": 0,
            "source": {
                "name": "CyberSecurity News",
                "domain": "https://cybersecuritynews.com",
                "favicon": "https://cybersecuritynews.com/favicon.ico"
            }
        }