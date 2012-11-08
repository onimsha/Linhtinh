# -*- coding: utf-8 -*-
import logging
import random
import threading
import time
import MySQLdb
import xmlrpclib
import sys

def openerp():
    
    dbname='beshop_dev'
    username='admin'
    pwd='devadminvng@123'
    
    
    sock_common = xmlrpclib.ServerProxy('http://10.40.52.13:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)
    sock = xmlrpclib.ServerProxy('http://10.40.52.13:8069/xmlrpc/object')
    
    order_info={
        'picking_policy' : 'one',
        'order_policy' : 'manual',
        'state' : 'manual',
        'pricelist_id' : 1,    
        'shipped' : False,
        'invoice_quantity' : 'order',
        #'add_disc' : 20,
        'vng_payment_type' : 'DAB_ATM',    
        'vng_remain_amount' : 0    
        #'vng_disc_amt' : 30000
    }
    
    orderline1={
        'product_uom_code' : 'PCE',    
        'price_unit' : 789000,
        'product_uom_qty' : 1,    
        'name' : 'Xe Ben',    
        'default_code' : '1001059000004',      
        #'vng_discount_amount':530000
        #'discount':30  
    }
    """
    orderline2={
        'product_uom_code' : 'PCE',    
        'price_unit' : 99000,
        'product_uom_qty' : 1,    
        'name' : 'Xe taxi vàng New York',    
        'default_code' : '10212',      
        #'vng_discount_amount':530000
        'discount':20  
    }
    """
    line = [orderline1]#,orderline2,orderline3,orderline4]
    order = {
        'info' : order_info,
        'line' : line
    }
    
    customer_info= {    
        'name' : 'Nguyễn Bá',
        'fe_cus_id' : 210, 
        'zing_id' : 'nbd',  
        'phone' : '012234521369', 
        'mobile' : '083652147',  
        'email' : 'nbd@yahoo.com.vn',   
        'fax' : '853214697711',    
    }
    
    payment = {    
        'fe_add_id' : 322,    
        'name' : 'Nguyễn Bá',
        'type' : 'contact',    
        'street' : '245/235',
        'street2' : 'Nguyễn Trãi',    
        'city_code' : '79',
        'district_code' : '2',
        'phone' : '012234521369',
        'email' : 'nbd@yahoo.com.vn',
    }
    
    shipping = {    
        'fe_add_id' : 324,    
        'name' : 'Nguyễn Lê',
        'type' : 'delivery',    
        'street' : '6666666666666',
        'street2' : 'Bùi Đình Túy',    
        'city_code' : '79',
        'district_code' : '2',
    }
    
    customer = {
         'info' : customer_info,
         'address' : [payment,shipping]     
    }
    
    
    result = sock.execute(dbname, uid, pwd, 'gateway', 'requestMethod', 'shop123', 'esb_import_data', [order, customer])
    print result
    
    
openerp()

#class Counter(object):
#    def __init__(self, start=0):
#        #self.lock = threading.Lock()
#        self.value = start
#    def increment(self):
#        logging.debug('Waiting for lock')
#        #self.lock.acquire()
##        try:
##            logging.debug('Acquired lock')
#        self.value = self.value + 1
#        #finally:
#         #   self.lock.release()
#def worker(a):
#    pause = random.random()
#    logging.debug('Sleeping %0.02f', pause)
#    time.sleep(pause)
#    try:
#        openerp()     
#    except:
#        e = sys.exc_info()[0]
#        print e
#    a.increment()
#    logging.debug('Done')
#
#counter = Counter()
#for i in range(10):
#    t = threading.Thread(target=worker, args=(counter,))
#    t.start()
#
#logging.debug('Waiting for worker threads')
#main_thread = threading.currentThread()
#for t in threading.enumerate():
#    if t is not main_thread:
#        t.join()
#logging.debug('Counter: %d', counter.value)
