# google-scholar-profiles-scrapy-spider

Python Scrapy spider that searches Google Scholar profiles for a particular profile id and extracts all search results from the product page. 
The spider will get all publications in the author page. The following are the fields the spider scrapes for the Google Scholar search results page:

- Title 
- Link
- Number of Citations
- Author
- Publisher
- Snippet
- date

This Google Scholar spider uses [Scraper API](https://www.scraperapi.com/) as the proxy solution. Scraper API has a free plan that allows you to make up to 1,000 requests per month which makes it ideal for the development phase, but can be easily scaled up to millions of pages per month if needs be.

To monitor the scraper, this scraper uses [ScrapeOps](https://scrapeops.io/). **Live demo here:** [ScrapeOps Demo](https://scrapeops.io/app/login/demo)

![ScrapeOps Dashboard](https://scrapeops.io/assets/images/scrapeops-promo-286a59166d9f41db1c195f619aa36a06.png)


## Using the Google Scholar Spider
Make sure Scrapy is installed use command below if required:

```
pip install scrapy
```
## Other Requirements 

```
pip install Selenium
pip install urllib
```
Set the profile id from google scholar page example below:
qjzD5CgAAAAJ
```
https://scholar.google.com/citations?hl=en&user=(qjzD5CgAAAAJ)&view_op=list_works&sortby=pubdate
```

### Setting Up ScraperAPI
Signup to [Scraper API](https://www.scraperapi.com/signup) and get your free API key that allows you to scrape 1,000 pages per month for free. Enter your API key into the API variable:
you can also use other API services but would need to modify the code according to that service parameters

```
API_KEY = '<YOUR_API_KEY>'

def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url
```

By default, the spider is set to have a max concurrency of 5 concurrent requests as this the max concurrency allowed on Scraper APIs free plan. 
If you have a plan with higher concurrency then make sure to increase the max concurrency in the `settings.py`. 1 concurrent request recommended for free plans. 

```
## settings.py

CONCURRENT_REQUESTS = 5
RETRY_TIMES = 5

# DOWNLOAD_DELAY
# RANDOMIZE_DOWNLOAD_DELAY
```

We should also set `RETRY_TIMES` to tell Scrapy to retry any failed requests (to 5 for example) and make sure that `DOWNLOAD_DELAY`  and `RANDOMIZE_DOWNLOAD_DELAY` aren’t enabled as these will lower your concurrency and are not needed with Scraper API.

### Integrating ScrapeOps
[ScrapeOps](https://scrapeops.io/) is already integrated into the scraper via the `settings.py` file. However, to use it you must:

Install the [ScrapeOps Scrapy SDK](https://github.com/ScrapeOps/scrapeops-scrapy-sdk) on your machine.

```
pip install scrapeops-scrapy
```

And sign up for a [free ScrapeOps account here](https://scrapeops.io/app/register) so you can insert your **API Key** into the `settings.py` file:

```
    ## settings.py
    
    ## Add Your ScrapeOps API key
    SCRAPEOPS_API_KEY = 'YOUR_API_KEY'
    
    ## Add In The ScrapeOps Extension
    EXTENSIONS = {
     'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
    }
    
    ## Update The Download Middlewares
    DOWNLOADER_MIDDLEWARES = { 
	'scrapeops_scrapy.middleware.retry.RetryMiddleware': 550, 
	'scrapy.downloadermiddlewares.retry.RetryMiddleware': None, 
    }
```
From there, our scraping stats will be automatically logged and automatically shipped to our dashboard.

### Running The Spider
To run the spider, use:
the python code in runner.py
```
python3 ./googlescholarSpider/runner.py
```
Original code is adapted from @ian-kerins
