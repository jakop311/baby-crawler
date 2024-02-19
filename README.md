# baby-crawler
An easy crawler to crawl all the static urls in the website.
### How to use
First clone the repo.

`$ git clone https://github.com/jakop311/baby-crawler.git`

Install the requirements.

`$ python -m pip install -r requirements.txt`

#### Running the baby-crawler
##### Basic crawl
`$ python baby-crawler -u "URL of the website to crawl"`
##### Options
```
$ python baby-crawler.py -h                                                                           
usage: python web-crawler.py [-h] -u URL [-f] [-d {0,1,2}] [-s SLEEP] [-p [PROXY ...]]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     Url of the website
  -f, --fuzzable        Show fuzzable urls inside the website
  -d {0,1,2}, --depth {0,1,2}
                        Set the crawl depth (** Max is 2)
  -s SLEEP, --sleep SLEEP
                        Set time to sleep
  -p [PROXY ...], --proxy [PROXY ...]
                        Set up HTTP Proxy in the format: http proxy1(http://host:port/) https proxy2(https://host:port/)
```
##### Examples
```
$ python baby-crawler.py -u https://google.com/ -s 2 ##Sleep for 2 seconds
$ python baby-crawler.py -u https://scrapethissite.com/ -d 1 ##Crawl depth=1 
$ python baby-crawler.py -u https://example.com/ -f ##Output fuzzable urls
$ python baby-crawler.py -u https://example.com/ -p http http://localhost:8080 ##Set up HTTP Proxy
```

### To-Do
1. Output into csv files
2. Find a way to get dynamic urls
