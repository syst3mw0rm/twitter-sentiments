# --coding: utf-8 --
import tornado.ioloop
import tornado.httpclient
import urllib
import json
import pika
import sys
import _mysql
import MySQLdb
from django.utils.encoding import smart_str


textProcessingUrl = "http://text-processing.com/api/sentiment/"

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweets')

conn = MySQLdb.connect('localhost', 'root', 'rootroot', 'twitter')

class Handler():
	def __init__(self, tweet, query):
		self.tweet = tweet
		self.cur = conn.cursor()
		self.query = smart_str(query)

	def handle_request(self, response):
		#print response.body
		response_json = json.loads(response.body)
		#print response.headers
		#print self.tweet["text"]
		#print "got response"
		self.cur.execute("""INSERT INTO sentiments (id, query, tweet, pos, neg, neutral, label) values ( '%s', '%s', '%s' ,%s, %s, %s, '%s')""" % (self.tweet["id"], self.query, self.tweet["text"], response_json["probability"]["pos"], response_json["probability"]["neg"], response_json["probability"]["neutral"], response_json["label"] ));




_http_client = tornado.httpclient.AsyncHTTPClient()

def sentiment_analysis(ch, method, properties, json_body):
	json_object = json.loads(json_body)
        tweets = json_object["results"]
	headers = {'Content-Type'   : 'application/x-www-form-urlencoded'}
	q = json_object["query"]
	#print tweets
	for tweet in tweets:
		tweet["text"] = smart_str(tweet["text"])
		parameters = {"text" : tweet["text"] }
		#print tweet["text"]
		headers = {'Content-Type'   : 'application/x-www-form-urlencoded'}
		obj = Handler(tweet, q)
		query = urllib.urlencode(parameters)
		#print query
		req_obj = tornado.httpclient.HTTPRequest(textProcessingUrl, 
							 method = 'POST',
							 body = query,
							 headers = headers)
		_http_client.fetch(req_obj, obj.handle_request)


def consume_tweet():
	channel.basic_consume(sentiment_analysis,
        	              queue='tweets',
                	      no_ack=True)

io_loop = tornado.ioloop.IOLoop.instance()

schedule = tornado.ioloop.PeriodicCallback(consume_tweet, 1000)
schedule.start()
io_loop.start()
