import os
import webapp2
import jinja2
import time
#import spider.local
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class scrapeData(db.Model): #db schema
    title = db.StringProperty()
    text = db.TextProperty()
    scrapeDate = db.DateTimeProperty(auto_now_add=True)
    ancestor = db.StringProperty()
    rank = db.IntegerProperty()

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        y = jinja_env.get_template(template)
        return y.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

class MainPage(Handler):
    def render_page(self, error="", **kwargs):
        scrapeData = db.GqlQuery("SELECT * FROM scrapeData") # SEARCH THROUGH ITEMS
        #scrapeData = "test"
        currentTime = time.strftime('%B %d, %H:%M:%S')
        self.render("search.html", scrapeData=scrapeData, error=error, time=currentTime, **kwargs)

    def get(self):
        query = self.request.get('query')
        self.render_page(query=query)

    def post(self):
        error = "This website does not accept post requests."
        self.render("search.html", error=error)

class Junk(Handler):
    def get(self):
        title="test title"
        text="test text"
        x = scrapeData(title=title, text=text)
        x.put()
        scrapeData = db.GqlQuery("SELECT * FROM scrapeData") # SEARCH THROUGH ITEMS
        self.render("search.html", scrapeData=scrapeData, error="dummy data!")

class Spider(Handler):
    def get(self, error="", query=""):
        self.render("spider.html", error=error, query=query)

#insert data
#x = scrapeData(title=title, text=text, parent=parent, rank=rank)
#x.put()
#query data
#db.GqlQuery("SELECT * FROM scapeData ORDER BY rank DESC")

app = webapp2.WSGIApplication([('/', MainPage), ('/test', Junk), ('/spider', Spider)], debug=True)
