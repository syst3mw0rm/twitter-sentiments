import Queue
import threading
import urllib2
import time
from BeautifulSoup import BeautifulSoup


hosts = [ "http://www.google.com", "http://www.greplin.com", "http://www.amazon.com", "http://apple.com", "http://www.techcrunch.com", "http://www.ibm.com" ]

queue = Queue.Queue()

class ThreadUrl(threading.Thread):

	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			host = self.queue.get()
			url = urllib2.urlopen(host)
			chunk = url.read()
			soup = BeautifulSoup(chunk)
			print soup.findAll(['title'])
			self.queue.task_done()


start = time.time()

def main():
	for i in range(5):
		t = ThreadUrl(queue)
		t.setDaemon(True)
		t.start()

	for host in hosts:
		queue.put(host)

	queue.join()

	
main()
print "Elapsed time : %s", (time.time() - start)


