import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class RottentomatoesSpider(CrawlSpider):
    name = "rottentomatoes"
    allowed_domains = ["rottentomatoes.com"]
    # start_urls = ["https://www.rottentomatoes.com/top/bestofrt/?year=2020"]

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.rottentomatoes.com/top/bestofrt/?year=2020",
            headers={"User-Agent": self.user_agent},
        )

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//table[@class='table']/tr/td[3]/a"),
            callback="parse_item",  # never use "parse" it will break
            follow=True,
            process_request="set_user_agent",
        ),
        Rule(
            # LinkExtractor will automatically search for @hrdf, so don't add @href in xpath
            LinkExtractor(restrict_xpaths="//ul[@class='dropdown-menu']/li/a"),
            process_request="set_user_agent",
        ),
        # can't set pagination at RULE1, because it will try immediately visit the next page
        # the first page will skipped
    )

    def set_user_agent(self, request, spider):
        request.headers["User-Agent"] = self.user_agent
        return request

    # def parse(self, response):
    #     rows = response.xpath("//h3[@class='lister-item-header']/a/@href").extract()
    #     for row in rows:
    #         link = "https://www.rottentomatoes.com" + row
    #         yield scrapy.Request(url=link, callback=self.parse_item)

    def parse_item(self, response):
        # print(response.url)
        yield {
            "title": response.css("h1.mop-ratings-wrap__title ::text").extract_first(),
            "critics_consensus": response.css(
                "p.mop-ratings-wrap__text--concensus ::text"
            ).extract(),
            # i['average_grade'] = response.xpath("(//div[@class='score_details__big-text'])[2]/span/text()").extract()
            # i['average_grade'] = response.css('#js-audience-score-info ::text').extract()[1]
            "amount_reviews": response.xpath(
                "normalize-space(//small[@class='mop-ratings-wrap__text--small']/text())"
            ).extract(),
            "approval_percentage": response.xpath(
                "normalize-space((//span[@class='mop-ratings-wrap__percentage'])[1]/text())"
            ).extract(),
            "date": response.xpath(
                "normalize-space((//div[@class='meta-value']//time)[1]/text())"
            ).extract(),
            "url": response.css(".posterImage ::attr(data-src)").extract(),
            # "link": "".join(url)
            # i["images"] = {link: i["title"]}
            "user-agent": response.request.headers["User-Agent"],
        }
