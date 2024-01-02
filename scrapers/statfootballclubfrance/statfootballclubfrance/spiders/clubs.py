import scrapy


CLASSNAME_REGION = "tpalmtr1"

class ClubsSpider(scrapy.Spider):
    name = "clubs"
    allowed_domains = ["statfootballclubfrance.fr"]
    start_urls = ["https://statfootballclubfrance.fr/clubs-foot-france-historique.php"]

    def parse(self, response):
        current_region = None
        for tabclubrow in response.xpath("//table[@class='tabclub']/tr"):
            if tabclubrow.xpath("./@class").get() == CLASSNAME_REGION:
                current_region = tabclubrow.xpath("./td/div/text()").get()
            if tabclubrow.xpath("./@class").get() is None:
                tds = tabclubrow.xpath("./td/text()").getall()
                clubname = tabclubrow.xpath("./td/a/text()").getall()
                clubref = tabclubrow.xpath("./td/a/@href").getall()
                try:
                    district=tds[1]
                except IndexError:
                    district="Paris"
                yield {
                    "ville": tds[0],
                    "district": district,
                    "club": clubname[0],
                    "ref": clubref[0],
                    "region": current_region
                }
