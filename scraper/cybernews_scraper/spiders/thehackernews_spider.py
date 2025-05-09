import scrapy

class TheHackerNewsSpider(scrapy.Spider):
    name = "thehackernews"
    allowed_domains = ["thehackernews.com"]
    start_urls = ["https://thehackernews.com/"]

    def parse(self, response):
        # Extraire les articles de la page d'accueil
        for article in response.css("div.body-post.clear"):
            title = article.css("h2.home-title::text").get()
            url = article.css("a.story-link::attr(href)").get()
            
            # Extraire la date et la catégorie
            date = article.css("span.h-datetime::text").get()
            category = article.css("span.h-tags::text").get()
            
            # Extraire la description
            description = article.css("div.home-desc::text").get()
            if description:
                description = description.strip()
            
            # Extraire l'image
            image_url = article.css("div.home-img img::attr(data-src)").get()
            
            yield {
                "title": title,
                "url": url,
                "date": date,
                "category": category,
                "description": description,
                "image_url": image_url
            }
            
            # Suivre le lien pour extraire le contenu complet
            yield scrapy.Request(url, callback=self.parse_article)
    
    def parse_article(self, response):
        """Analyse le contenu d'un article complet"""
        title = response.css("h1.story-title a::text").get()
        # Extraire le corps de l'article
        content = ""
        paragraphs = response.css("div.articlebody p::text").getall()
        if paragraphs:
            content = "\n".join([p.strip() for p in paragraphs if p.strip()])
        
        # Extraire la date et l'auteur
        date = response.css("span.author::text").get()
        author = response.css("span.author::text").getall()
        if len(author) > 1:
            author = author[1]
        else:
            author = None
            
        # Extraire les tags
        tags = response.css("div.tags a::text").getall()
        
        yield {
            "title": title,
            "url": response.url,
            "date": date,
            "author": author,
            "content": content,
            "tags": tags
        }