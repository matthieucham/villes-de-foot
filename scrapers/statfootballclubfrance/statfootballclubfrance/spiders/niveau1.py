import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

REGEX_YEAR = re.compile(r"^.*\-(?P<annee>\d+)\-classement\.php$")


class Niveau1Spider(CrawlSpider):
    name = "niveau1"
    allowed_domains = ["statfootballclubfrance.fr"]
    start_urls = [
        "https://www.statfootballclubfrance.fr/historique-championnat-ligue1.php"
    ]
    rules = [
        Rule(
            LinkExtractor(allow=("ligue-1", "division-1", "division-nationale")),
            callback="parse",
        )
    ]

    def parse(self, response):
        year = None
        m = REGEX_YEAR.match(response.request.url)
        if m:
            year = m.groupdict()["annee"]
        for classement_row in response.xpath("//table/tr[@class='trclas1']/td[@class='tdclas2']"):
            ref = classement_row.xpath("./a/@href").getall()
            club = classement_row.xpath("./a/text()").getall()
            yield {
                "ref": ref[0],
                "club": club[0],
                "niveau": 1,
                "annee": year
            }
        