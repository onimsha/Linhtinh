import logging
import random
import threading
import time
import MySQLdb


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )
                    
class Counter(object):
    def __init__(self, start=0):
        #self.lock = threading.Lock()
        self.value = start
    def increment(self):
        logging.debug('Waiting for lock')
        #self.lock.acquire()
#        try:
#            logging.debug('Acquired lock')
        self.value = self.value + 1
        #finally:
         #   self.lock.release()
def worker(a):
    for i in range(1000):
        pause = random.random()
        logging.debug('Sleeping %0.02f', pause)
        time.sleep(pause)
        try:
            db=MySQLdb.connect(host="10.40.52.10",user="dba",passwd="uLU8dNQ2qP4f",db="esb_g8_dev")
            c=db.cursor()
            c.execute("INSERT INTO `requests` (`apiname`, `requestid`, `clientip`, `request_timestamp`, `status`) VALUES ('SaleOrder', '123123123111', '10.74.7.110', now(), '1')")
            db.commit()
        except:
            db.rollback()
            c.close
        a.increment()
    logging.debug('Done')

counter = Counter()
for i in range(10):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()

logging.debug('Waiting for worker threads')
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
logging.debug('Counter: %d', counter.value)