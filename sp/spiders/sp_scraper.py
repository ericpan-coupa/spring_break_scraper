import scrapy

class spSpider(scrapy.Spider):
    name = "breaks"

    def start_requests(self):
        urls = [
            'https://publicholidays.us/school-holidays/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        self.log("before")
        url_state = response.xpath('//td[@class="column-1"]/a/@href').extract() + \
                    response.xpath('//td[@class="column-2"]/a/@href').extract()
        self.log("after")
        self.log(url_state)
        for url in url_state:
            self.log("sdfa")
            self.log(url)
            yield scrapy.Request(url=url, callback=self.parse_state)

        self.log('scraped %s' % page)

    def parse_state(self, response):
        state = response.url.split("/")[-2]
        url_state = response.xpath('//td[@class="column-1"]/a/@href').extract() + \
                    response.xpath('//td[@class="column-2"]/a/@href').extract()
        for url in url_state:
            yield scrapy.Request(url=url, callback=self.parse_school, meta={'state': state})
        self.log('scraped %s' % state)

    def parse_school(self, response):
        school = response.url.split("/")[-2]
        state = response.meta.get('state')
        holiday_name = response.xpath("//td//span/text()").extract()
        holiday_date = [i.xpath('text()').extract() for i in response.xpath("//tr//td")]
        n_holiday = len(holiday_name)
        start_date = [i[0] if i else None for i in holiday_date[1::3]]
        end_date = [i[0] if i else None for i in holiday_date[2::3]]
        for i in range(n_holiday):
            item = {"state": state,
                    "school": school,
                    "holiday_name": holiday_name[i],
                    "start_date": start_date[i],
                    "end_date": end_date[i]}
            yield item
        self.log('scraped %s' % school)
