import scrapy


class BrickSetSpider(scrapy.Spider):
    name = "nasa_scrape"
    start_urls = [
        'https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html']

    def parse(self, response):
        TABLE_SELECTOR = './/tr[text()]'
        self.logger.info("Visited %s", response.url)
        res = response.xpath(TABLE_SELECTOR)
        # self.logger.info("res %s", res)
        # TODO: get the first row's columns values for further display
        firstRowColsHead = res[0].css('th *::text').extract()
        # self.logger.info("firstRowColsHead %s", firstRowColsHead)

        for planet in res[1:]:
            # self.logger.info("planet %s", planet)
            ROW_HEAD_SELECTOR = 'th *::text'
            ROW_COL_SELECTOR = 'td *::text'
            selectedRowsHead = planet.css(ROW_HEAD_SELECTOR)
            selectedCols = planet.css(ROW_COL_SELECTOR)
            # self.logger.info("selectedRowsHead %s", selectedRowsHead)
            self.logger.info("selectedCols %s", selectedCols)

            rowColsIndexes = [0, 1, 2]
            for rowHead in selectedRowsHead:
                for col in selectedCols:
                    for idx in rowColsIndexes:
                        yield {
                            'property_name': ''+rowHead.extract()+'/'+firstRowColsHead[idx],
                            'value': col.extract()
                        }
