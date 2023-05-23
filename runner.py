from scrapy.cmdline import execute

try :
    execute(
        [
        'scrapy',
        'crawl',
        'scholar'
        ]
    )
except SystemExit:

    pass