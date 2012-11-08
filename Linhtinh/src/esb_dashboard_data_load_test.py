import thread
import threading
import time
import MySQLdb

#db=MySQLdb.connect(host="10.40.52.10",user="dba",passwd="uLU8dNQ2qP4f",db="esb_g8_dev")
#db=MySQLdb.connect(host="localhost",user="root",passwd="root",db="esb_g8_test")

exitFlag = 0

def insertdata(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        try:
            db=MySQLdb.connect(host="10.40.52.10",user="dba",passwd="uLU8dNQ2qP4f",db="esb_g8_dev")
            c=db.cursor()
            c.execute("INSERT INTO `requests` (`apiname`, `requestid`, `clientip`, `request_timestamp`, `status`) VALUES ('SaleOrder', '123123123111', '10.74.7.110', now(), '1')")
            db.commit()
        except:
            db.rollback()
            c.close
        counter -= 1

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        self.lock = threading.Lock()
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        
    def run(self):
        print "Starting " + self.name
        self.lock.acquire()
        insertdata(self.name, self.counter, 100)
        self.lock.release()
        print "Exiting " + self.name

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

           
