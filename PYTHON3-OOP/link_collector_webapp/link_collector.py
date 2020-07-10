import os
os.environ['http_proxy']=''
from urllib.request import urlopen 
from urllib.parse import urlparse
import re 
import sys 
from queue import Queue

LINK_REGEX = re.compile("<a [^>]*href=['\"]([^'\"]+)['\"][^>]*>")

class LinkCollector: 
    def __init__(self, url):
        self.url = "http://" + urlparse(url).netloc
        self.collected_links = {}
        self.visted_links = set() 
    
    """
    def collect_links(self, path="/"):
        full_url = self.url + path 
        self.visted_links.add(full_url)
        page = str(urlopen(full_url, timeout=15).read())
        links = LINK_REGEX.findall(page) 
        links = {self.normalize_url(path, link) for link in links}
        self.collected_links[full_url] = links
        
        for link in links:
            self.collected_links.setdefault(link, set())

        unvisted_links = links.difference(self.visted_links)

        for link in unvisted_links:
            if link.startswith(self.url):
                self.collect_links(urlparse(link).path)
    """

    # modifying the above function with Queue to store that haven't been processed yet. 
    def collect_links(self):
        queue = Queue() 
        queue.put(self.url)
        while not queue.empty():
            url = queue.get().rstrip('/') 
            self.visted_links.add(url)
            page = str(urlopen(url, timeout=15).read())
            links = LINK_REGEX.findall(page)
            links = {self.normalize_url(urlparse(url).path, link) for link in links}
            self.collected_links[url] = links

            for link in links:
                self.collected_links.setdefault(link, set())
            unvisted_links = links.difference(self.visted_links)

            for link in unvisted_links:
                if link.startswith(self.url):
                    queue.put(link)



    def normalize_url(self, path, link):
        if link.startswith("http://"):
            return link 
        elif link.startswith("/"):
            return self.url + link 
        else:
            return self.url + path.rpartition('/')[0] + '/' + link.rstrip('/')


if __name__ == "__main__":
    collector = LinkCollector(sys.argv[1])
    collector.collect_links()
    for link, item in collector.collected_links.items():
        print(f"{link}: {item}")

