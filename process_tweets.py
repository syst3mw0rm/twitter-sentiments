import tornado.ioloop
import tornado.httpclient
import urllib
import json
import pika
import sys
from django.utils.encoding import smart_str

textProcessingUrl = "http://text-processing.com/api/sentiment/"

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweets')

def handle_request(response):
	print response.body
	print response.headers
	#print "got response"

_http_client = tornado.httpclient.AsyncHTTPClient()

def sentiment_analysis(ch, method, properties, json_body):
	json_object = json.loads(json_body)
        tweets = json_object["results"]
	headers = {'Content-Type'   : 'application/x-www-form-urlencoded'}
	#print tweets
	for tweet in tweets:
		text = smart_str(tweet["text"])
		parameters = {"text" : text}
		#print tweet["text"]
		headers = {'Content-Type'   : 'application/x-www-form-urlencoded'}
		query = urllib.urlencode(parameters)
		#print query
		req_obj = tornado.httpclient.HTTPRequest(textProcessingUrl, 
							 method = 'POST',
							 body = query,
							 headers = headers)
	
		_http_client.fetch(req_obj, handle_request)

def consume_tweet():
	channel.basic_consume(sentiment_analysis,
        	              queue='tweets',
                	      no_ack=True)

io_loop = tornado.ioloop.IOLoop.instance()

schedule = tornado.ioloop.PeriodicCallback(consume_tweet, 1000)
schedule.start()
io_loop.start()
