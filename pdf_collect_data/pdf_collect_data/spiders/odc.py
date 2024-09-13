""" Scrap all the PDF Link from ODC Website """

import scrapy
from scrapy.http import HtmlResponse
from jsonl_format.jsonl_formatter import get_warc_headers

from pdf_scrapper.data_parser import DataParser
from utils.visited_url import get_visited_url, update_visited


class OdcPdfSpider(scrapy.Spider, DataParser):
    """
    ODC PDF Spider

    Attributes
    ----------
    name: str
        Name of the spider for calling when start clrawling.
    """
    name = "odc_pdf"

    def __init__(self) -> None:
        """
        Class Constructor

        Attributes
        ----------
        visited_url: set
            Keep tract all the visited article URL to prevent look back on the next time.
        domain: str
            Base URL of ODC website
        """
        super().__init__()
        self.visited_urls = get_visited_url("visited_odc_pdf.txt")
        self.domain = "https://data.opendevelopmentcambodia.net"

    def start_requests(self):
        """
        Start Request Page

        Yield
        -----
            Yield request object URL to spider engine to execute `parse` method.
        """
        # pylint: disable=C0301
        url = self.domain + "/km/dataset/?odm_language_list=km&res_format=PDF&q=&sort=score+desc%2C+metadata_modified+desc"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):  # pylint: disable=W0221,C0301
        """
        Spider Parser

        Parameter
        ---------
        response: HtmlResponse
            Response object from the URL request.

        Yields
        ------
        Dict
            An item data get from `parse_article` method.
        Request object
            An resquest object follow to next page.
        """

        for data in response.css("li.dataset-item"):
            pdf_link = self.domain + data.xpath("div/h3/a/@href").get()

            if pdf_link not in self.visited_urls:
                yield scrapy.Request(pdf_link, callback=self.article_parse)

            else:
                self.logger.info(f"Already visitted URL: {pdf_link}")

        next_page = response.css("ul.pagination a:contains('»')::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def article_parse(self, response):
        """
        Parse PDF page to json object

        Parameters
        ----------
        response: response object
            Page response to the document page.

        Yield
        ------
        Dictionary of the content in URL.
        """
        self.visited_urls.add(response.url)
        update_visited("visited_odc_pdf.txt", response.url)

        additional_info = response.css(".additional-info > .table > tbody")
        additional_data = self.get_additional_info(additional_info)

        pdf_metadata = self.to_file_metadata(
            title=response.css(".module-content > h1::text").get().strip(),
            category=response.css(".toolbar > ol > li ~ li > a::text").get().strip(),
            file_link=response.css(".resource-url-analytics::attr(href)").getall(),
            additional_info=additional_data
        )

        article_data = self.to_json_item(
            content=response.css(".notes > p::text").get(),
            warc_headers=get_warc_headers(response.url),
            metadata=None,  # got some error with fasttext, so we use None by default.
            file_metadata=pdf_metadata
        )

        yield article_data

    @staticmethod
    def get_additional_info(addictional_info: HtmlResponse) -> dict:
        """
        Parse PDF additional information

        Parameter
        ----------
        addictional_info: HtmlResponse
            Addional information table from the PDF page.

        Return
        -------
        Metadata `dict` of PDF meta data.
        """
        metatdata = {}

        for info in addictional_info:
            rows = info.xpath("tr")
            for row in rows:
                label = row.xpath("th//text()").get()
                value = [text.strip() for text in row.xpath("td//text()").getall() if text.strip()]
                if len(value) <= 1:
                    value = "".join(value)

                metatdata[label] = value

        return metatdata
