import tornado.ioloop
import tornado.httpclient
import urllib
import json
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='tweets',type='fanout')
channel.queue_declare(queue='tweets')
channel.queue_bind(exchange='tweets',
                   queue='tweets')



url = "http://search.twitter.com/search.json?"

since_id = ""

def handle_request(response):
    global since_id
    if response.error:
        print "Error:", response.error
    else:
        json_object = json.loads(response.body)
        since_id = json_object["max_id"]
        print "1" #response.body
        # Let's push it into rabbitmq queue - twitter-sentiments
        channel.basic_publish(exchange='tweets',
                      routing_key='',
                      body=message)


_http_client = tornado.httpclient.AsyncHTTPClient()

def make_request():
	parameters = [ ('q', '#facebook'), ('rpp',100), ('include_entities', 'true'),
			   ('since_id', since_id) ]
	query = urllib.urlencode(parameters)
	print query
	_http_client.fetch(url+query, handle_request)


io_loop = tornado.ioloop.IOLoop.instance()

schedule = tornado.ioloop.PeriodicCallback(make_request, 1000)
schedule.start()
io_loop.start()
