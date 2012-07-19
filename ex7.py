# Web scraper
# This script will scrape an entire webpage and store it in a database
# It will scan for links on the page and scan each of them.
# Based on the number of links to a page, a page will gain a higher rank

import urllib2
import time
import psycopg2

class url():
    def __init__(self, url):
        self.url = url

    def writeDB(self, url, title, hitsinternal, hitsexternal, hops, meta, date):
        pass

    def readDB(self, url, title, hitsinternal, hitsexternal, hops, meta, date):
        pass

    def scanpage(self):
        self.page = urllib2.request(url)

    def findhref(self):
        while 1:
            offset1 = self.page.find("href=\"")+6
            offset2 = self.page.find("\"", offset1)
            href.append(self.page[offset1:offset2])
"""
def main():
    while 1:
        input = raw_input("Enter a seed url >> ")
        try:
            if (type(input) == str) & (input[:7] == "http://") & (input[-1] == "/"):
                break
            else:
                print "Your input must be a string that begins with http:// and ends with /"
        except IndexError:
            print "Your input must be a string that begins with http:// and ends with /"
        except:
            print "An unexpected error occurred"

    seedURL = input[:]

    while 1:
        input = raw_input("Enter a maximum number of webpages to crawl >> ")
        # if ((type(input) == int) & (input > 0)):
        try:
            if (int(input) > 0):
                break
            else:
                print "You must enter a number greater than 0"
        except:
            print "You must enter a number greater than 0"

    maxFrontiers = int(input)

    while 1:
        input = raw_input("Enter a maximum number of links beyond the seed >> ")
        try:
            if (int(input) > 0):
                break
            else:
                print "You must enter a number greater than 0"
        except:
            print "You must enter a number greater than 0"
    maxHops = int(input[:])

    print 50*"#"
    print "seedURL is "+seedURL+"\nmaxFrontiers is "+str(maxFrontiers)+"\nmaxHops is "+str(maxHops)
    print 50*"#"

    input = raw_input("Press enter to exit")

if __name__ == "__main__":
    main()
"""

"""
database schema:
    table: websites
    url:    varchar(255)
    inside_hitcounts: int(16)
    outside_hitcounts: int(16)
    title:  varchar(255)
    meta:   varchar(1024)
    page:   varchar(65536)
    date:   datetime
"""
