# Web scraper
# This script will scrape an entire webpage and store it in a database
# It will scan for links on the page and scan each of them.
# Based on the number of links to a page, a page will gain a higher rank

import urllib2
import time
import psycopg2
import urlparse

URLDir = []
#for num of hops, each element of urlDir refers to a list of urls at that hop from the seed
#URLDir[1] refers to all urls 2 hops from the seed, while urlDir[5] refers to all urls 6 hops from the seed
hop = 0
frontier = 0

class URL():
    def __init__(self, URL):
        self.URL = URL
        #URLDir[hop].append(URL)

    def grabPage(self):
        try:
            self.request = urllib2.urlopen(self.URL)
            self.page = self.request.read()
        except ValueError:
            print "That URL couldn't be interpreted. Results of that href were thrown out."
            self.error = True
        except:
            print "An unknown error occurred"
        #self.pageheaders = self.request.headers.__dict__

    def writeDB(self, URL, title, hitsinternal, hitsexternal, hops, meta, date):
        pass

    def readDB(self, URL, title, hitsinternal, hitsexternal, hops, meta, date):
        pass

    def findHref(self):
        global hop
        # while loop chops href attributes from page and appends their references to urlList to be crawled
        while ("href=\"" in self.page):
            offset1 = self.page.find("href=\"")
            offset2 = self.page.find("\"", offset1+6)
            if (offset1 == -1) | (offset2 == -1):
                break
                #No more href attributes found
            else:
                newURL = self.page[offset1+6:offset2]

            if newURL[:6] !="http://":
                newURL = self.URL+newURL
            try:
                URLDir[hop+1].append(URL(newURL))
            except IndexError:
                URLDir.append([])
                URLDir[hop+1].append(URL(newURL))
            except:
                print "An unknown error occurred"
            self.page = self.page[:offset1] + self.page[offset2+1:]

def main():
    global hop, frontier
    while 1:
        input = raw_input("Enter a seed url >> ")
        """
        try:
            if (type(input) == str) & (input[:7] == "http://") & (input[-1] == "/"):
                break
            else:
                print "Your input must be a string that begins with http:// and ends with /"
        except IndexError:
            print "Your input must be a string that begins with http:// and ends with /"
        except:
            print "An unexpected error occurred. Please try again. \nYour input must be a string that begins with http:// and ends with /"
        """ 
        input = "http://localhost/~batman/"
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

    seed = URL(seedURL)
    URLDir.append(seed)

    def URLProcess(input):
        global frontier
        if type(input)==list:
            for item in input:
                print item, item.URL
                item.grabPage()
                frontier = frontier+1
                if item.error in locals():
                    item.findHref()
                time.sleep(1)
        else:
            print input, input.URL
            input.grabPage()
            frontier = frontier+1
            input.findHref()
            time.sleep(1)

    #def URLGrab(input):
    #    for item in input:
    #        if type(item)==list:
    #            URLGrab(item)
    #        else:
    #            URLprocess(item)

    while ((maxHops>hop) & (maxFrontiers>frontier)):
        print "hop is "+str(hop)
        URLProcess(URLDir[hop])
        time.sleep(1)
        hop = hop+1

    #URLGrab(URLDir[:maxHops+1])

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
