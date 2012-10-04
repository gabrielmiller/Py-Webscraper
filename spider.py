# Web scraper
# This script will scrape an entire webpage and store it in a database
# It will scan for links on the page and scan each of them.
# Based on the number of links to a page, a page will gain a higher rank

import urllib2
import time
#import psycopg2
import urlparse

URLDir = []
#for num of hops, each element of urlDir refers to a list of urls at that hop from the seed
#URLDir[1] refers to all urls 1 hop from the seed, while urlDir[5] refers to all urls 5 hops from the seed

class URL():
    def __init__(self, URL, hop=0):
        self.URL = URL
        self.hop = hop

    def grabPage(self):
        try:
            self.request = urllib2.urlopen(self.URL)
            self.page = self.request.read()[:]
            self.pageheaders = self.request.headers.__dict__
        except urllib2.HTTPError:
            print "\n HTTP Error occurred. This page was thrown out."
            self.error = True
    def findHref(self):
        #while loop chops href attributes from page and appends their references to URLDir to be crawled

        while ("href=\"" in self.page):
            offset1 = self.page.find("href=\"")
            offset2 = self.page.find("\"", offset1+6)

            newURL = urlparse.urljoin(self.URL,self.page[offset1+6:offset2])

            URLDir.append(URL(URL=newURL,hop=self.hop+1))

            self.page = self.page[:offset1] + self.page[offset2+1:]

def main():
    while 1:
        input = raw_input("Enter a seed url >> ")
        """
        try:
            if (type(input) == str) & (input[:7] == "http://"):
                break
            else:
                print "Your input must be a string that begins with http://"
        except IndexError: #in case input was left blank
            print "Your input must be a string that begins with http://"
        except:
            print "An unexpected error occurred. Please try again. \nYour input must be a string that begins with http://"
        """ 

        #input = "http://localhost/~batman/"
        input = "http://buttbox:8002/~gabe/"
        break
    seedURL = input[:]

    while 1:
        input = raw_input("Enter a maximum number of webpages to crawl >> ")
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
    print "seedURL: \t"+seedURL+"\nmaxFrontiers: \t"+str(maxFrontiers)+"\nmaxHops: \t"+str(maxHops)
    print 50*"#"

    URLDir.append(URL(seedURL))

    def URLProcess(input):
        input.grabPage()
        if "error" not in dir(input):
            input.findHref()
        #time.sleep(1)
        print "hop="+str(input.hop), "instance="+str(input), "len(URLDir)="+str(len(URLDir)), "URL="+input.URL

    for index, item in enumerate(URLDir):
        if urlparse.urlparse(item.URL)[1] != "buttbox:8002":   #local testing
            continue
        if (index > maxFrontiers):
            break
        if (item.hop > maxHops):
            break
        print "Page "+str(index),
        URLProcess(item)

    print 50*"#"

    input = raw_input("Press enter to exit")

if __name__ == "__main__":
    main()


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
