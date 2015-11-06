# -*- coding: utf-8 -*-
import scrapy


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com']
    start_urls = (
        'http://www.tripadvisor.com/Restaurants-g60763-zfn7102355-New_York_City_New_York.html',
    )

    def parse(self, response):
        # process each restaurant link
        urls = response.xpath('//h3[@class="title"]/a/@href').extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            request = scrapy.Request(
                absolute_url, callback=self.parse_restaurant)
            yield request

        # process next page
        next_page_url = response.xpath('//a[text()="Next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        request = scrapy.Request(absolute_next_page_url)
        yield request

    def parse_restaurant(self, response):
        name = response.xpath(
            '//div[@class="mapContainer"]/@data-name').extract_first()
        rating = response.xpath(
            '//img[@property="ratingValue"]/@content').extract_first()
        latitude = response.xpath(
            '//div[@class="mapContainer"]/@data-lat').extract_first()
        longitude = response.xpath(
            '//div[@class="mapContainer"]/@data-lng').extract_first()
        restaurant = {
            'name': name,
            'rating': rating,
            'latitude': latitude,
            'longitude': longitude,
            'url': response.url}
        yield restaurant
