from scrapy.cmdline import execute

try:
    execute(
        [
            'scrapy',
            'runspider',
            'scraper.py',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass
