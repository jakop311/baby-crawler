import requests
import argparse
from bs4 import BeautifulSoup
import time
import sys

class Crawler:
    
    def __init__(self, url, fuzzable=False, depth=0, sleep=1, proxy=None):
        self.url = url
        self.domain = url.split("/")[2]
        self.to_visit = set()
        self.to_visit.add(self.url)
        self.visited = set()
        self.fuzz_list = set()
        self.new_to_visit = self.to_visit.copy()
        self.fuzzable = fuzzable
        self.depth = depth
        self.sleep = sleep
        self.proxy = proxy
        
    def crawl(self):
        for current_depth in range(self.depth+2):
            while self.new_to_visit:
                url = self.new_to_visit.pop()
                if not self.visited.add(url):
                    self.retrieve(url)
            self.new_to_visit.update(self.to_visit - self.visited)
        
        if self.fuzzable:
            self.fuzz()
            print()
            print("[*] Fuzzable")
            print()
            for link in self.fuzz_list:
                print(f"[~] {link}")

    def fuzz(self):
        for link in self.visited:
            if "?" in link:
                self.fuzz_list.add(link)
    

    def retrieve(self, url):
        try:
            response = requests.get(url, proxies=self.proxy, allow_redirects=True)
            soup = BeautifulSoup(response.text, "lxml")
            self.visited.add(url)
            print(f"[+]: {url}")
        
            for link in soup.find_all("a", href=True):
                if link["href"].startswith("/"):
                    self.to_visit.add(self.url + link["href"])
                elif "http" in link["href"]:
                    if self.domain in link["href"]:
                        self.to_visit.add(link["href"])
                    else: 
                        continue
                elif link["href"].startswith("/")==False and self.domain not in link["href"]:
                    self.to_visit.add("http://" + self.domain + "/" + link["href"])
                else: 
                    continue
        except Exception as e:
            print(f"[-] Error retrieving {url}: {e}")
            
               

def main():
    
    # Arguments
    parser = argparse.ArgumentParser(prog="python baby-crawler.py")
    parser.add_argument("-u", "--url", help="Url of the website", dest="url", required=True)
    parser.add_argument("-f", "--fuzzable", help="Show fuzzable urls inside the website", dest="fuzzable", action="store_true")
    parser.add_argument("-d", "--depth", help="Set the crawl depth (** Max is 2)", type=int, choices=range(0,3), dest="depth")
    parser.add_argument("-s", "--sleep", help="Set time to sleep", dest="sleep", type=int, default=1)
    parser.add_argument("-p", "--proxy", help="Set up HTTP Proxy in the format: http proxy1(http://host:port/) https proxy2(https://host:port)", dest="proxy", nargs="*") 
    args = parser.parse_args()
    
    if "http" not in args.url and "https" not in args.url:
        if "http:" in args.url:
            args.url = "http://" + args.url
        elif "https:" in args.url:
            args.url = "https://" + args.url
        else: 
            pass
    if args.proxy:
        if len(args.proxy)%2 != 0:
            print("[-] Proxy configuration error. Please ensure you're providing them in pairs")
            sys.exit()
    
        proxy = {}
        for i in range(0, len(args.proxy), 2):
            proxy[args.proxy[i]] = args.proxy[i+1]
    else:
        proxy = None
    
    crawler = Crawler(args.url, args.fuzzable, args.depth, args.sleep, proxy)
    crawler.crawl()

main()
