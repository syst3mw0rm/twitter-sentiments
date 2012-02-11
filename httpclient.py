import tornado.ioloop
import tornado.httpclient
import urllib

url = "http://search.twitter.com/search.json?"

parameters = [ ('q', '#facebook') , ('since', '136536013832069120') ]

query = urllib.urlencode(parameters)

url += query

def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body

_http_client = tornado.httpclient.AsyncHTTPClient()

def make_request():
	_http_client.fetch(url, handle_request)


io_loop = tornado.ioloop.IOLoop.instance()

schedule = tornado.ioloop.PeriodicCallback(make_request, 100)
schedule.start()
io_loop.start()
