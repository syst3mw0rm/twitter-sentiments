import tornado.ioloop
import tornado.httpclient
import urllib
import json
import pika
import sys

textProcessingUrl = "http://api.text-processing.com/sentiment/"

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweets')

def handle_request(response):
	print response

_http_client = tornado.httpclient.AsyncHTTPClient()

def sentiment_analysis(ch, method, properties, text):
	parameters = {"text" : text}
	headers = {'Content-Type'   : 'application/x-www-form-urlencoded'}
	query = urllib.urlencode(parameters)
	print query

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
