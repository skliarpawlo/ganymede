from HTMLParser import HTMLParser
import re

class HTMLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        t = re.compile("(\s|\u00A0)+")
        d = t.sub(' ', d).strip()
        if len(d) > 0 :
            self.fed.append(d + "\n")
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()