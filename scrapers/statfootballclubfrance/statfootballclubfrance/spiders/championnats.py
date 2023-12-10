import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

REGEX_DIVISION = re.compile(r"^.*/historique-championnat\-(?P<division>\w+)\.php$")
REGEX_SAISON = re.compile(r"^\d{4}\s*\-\s*(?P<saison>\d{4})$")


class ChampionnatsSpider(CrawlSpider):
    name = "championnats"
    allowed_domains = ["statfootballclubfrance.fr"]
    start_urls = [
        "https://www.statfootballclubfrance.fr/menuchampionnat.php"
    ]
    rules = [
        Rule(
            LinkExtractor(allow=("-ligue1.php", "-ligue2.php", "-national.php", "-cfa.php")),
            callback="parse",
        )
    ]

    def parse(self, response):
        niveau = None
        m = REGEX_DIVISION.match(response.request.url)
        if m:
            match m.groupdict()["division"]:
                case "ligue1":
                    niveau=1
                case "ligue2":
                    niveau=2
                case "national":
                    niveau=3
                case "cfa":
                    niveau=4
        for classement_row in response.xpath("//table/tr[@class='tpalmtr2' or @class='tpalmtr3']"):
            saison = classement_row.xpath("./td/a/text()").getall()
            try:
                s = REGEX_SAISON.match(saison[0])
                annee = int(s.groupdict()["saison"])
            except ValueError:
                s = REGEX_SAISON.match(saison[1])
                annee = int(s.groupdict()["saison"])
            if niveau==4 and annee < 1994:
                effective_niveau=3
            else:
                effective_niveau=niveau
            nombre = classement_row.xpath("./td/text()").getall()
            try:
                nb = int(nombre[0])
            except ValueError:
                nb = int(nombre[1])
            yield {
                "saison": annee,
                "niveau": effective_niveau,
                "nombre": nb,
            }
        