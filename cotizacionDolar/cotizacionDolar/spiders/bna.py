import scrapy


class BnaSpider(scrapy.Spider):
    name = "bna"
    allowed_domains = ["www.bna.com.ar"]
    start_urls = ["https://www.bna.com.ar/Personas"]

    def parse(self, response):
        dolar = response.xpath('//td/text()').getall()

        yield {
            'dolar': dolar,
        }