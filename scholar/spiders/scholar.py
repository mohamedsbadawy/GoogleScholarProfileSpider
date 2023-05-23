import scrapy
from urllib.parse import urlencode
# from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_url(url):
    API_KEY = 'API_KeY'
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url
class ExampleSpider(scrapy.Spider):
    name = 'scholar'
    custom_settings = {
        'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv', 'encoding': 'utf-8'}},
        }
    # allowed_domains = ['api.scraperapi.com']
    def start_requests(self):
        # user id the between parentheses in this example https://scholar.google.com/citations?hl=en&user=(yGBA604AAAAJ)&view_op=list_works&sortby=pubdate
        queries = ['qjzD5CgAAAAJ']
        for query in queries:
            url = f'https://scholar.google.com/citations?hl=en&user={query}&view_op=list_works&sortby=pubdate'
                        # Set up Selenium WebDriver
            driver = webdriver.Chrome()  # Replace with the appropriate WebDriver for your browser
            driver.get(url)
            results = []  # List to store the results
            x_path = '//*[@id="gsc_bpf_more"]'
            button = driver.find_elements(By.XPATH, x_path)
            button= button[0]
            pages = []
            while button:
                time.sleep(2)
                button.click()
                print('Clicked')
                # No more buttons to click, save the response
                elements = driver.find_elements(By.XPATH,'//*[@id="gsc_a_nn"]')
                pages.append(elements[0].text)
                print(pages)
                Stop = []
                if len(pages) > 1:
                    for page in range(len(pages)):
                        if pages[page] == pages[page-1]:
                            results.append(driver.page_source)
                            Stop = "True"
                    if Stop == "True":
                        break
            # Close the WebDriver
            with open("./data/response.html", "w", encoding="utf-8") as file:
                file.write("".join(results))
            driver.quit()
            yield scrapy.Request(url = "file:///./data/response.html", callback=self.discoverPapersURLs, meta={'position': 0})
    def discoverPapersURLs(self, response):
        links = response.xpath('//*[@class = "gsc_a_at"]//@href').getall()
        global citations
        citations = response.xpath('//*[@class ="gsc_a_ac gs_ibl"]//text()').getall()
        for res in links:            
            #PaperRelativeURL = res.xpath('//@href').get()
            paperUrl = f'https://scholar.google.com{res}'
            yield scrapy.Request(url=get_url(paperUrl), callback=self.parse_paper_data)
                    ## Get All Pages
    def parse_paper_data(self, response):
        link = response.xpath('//*[@class = "gsc_oci_title_link"]//@href').get()
        citation = response.xpath('//*[@style="margin-bottom:1em"]//a//text()').get()
        title = response.xpath('//meta[@property="og:title"]/@content').get("").strip()
        snippet = [snippets.strip() for snippets in response.xpath('//*[@class = "gsh_csp"]//text()').getall()]
        details_auth_journal = response.xpath('//*[@class="gs_scl"]//*[@class="gsc_oci_value"]/text()').getall()
        if len(details_auth_journal)>2:
            Authors = details_auth_journal[0]
            Date = details_auth_journal[1]
            Journal = details_auth_journal[2]
        else:
            Authors = details_auth_journal
        yield {'title': title, 
               'Authors' :Authors, 
               'link': link, 
               'snippet': snippet, 
               'Date' : Date, 
               'Journal':Journal,
               'citations' : citation,
               }
