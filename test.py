# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:47:35 2016

@author: MagicWang
"""
import threading
import time

a=3

def test():
    global a
    a=1
    print 'a=%d'%a

def main_thread():
    global a
    time.sleep(1)
    print a

if __name__=="__main__":
#    thread1=threading.Thread(target=test,args=())
#    thread2=threading.Thread(target=main_thread,args=())
#    thread2.start()
#    thread1.start()
#    while 1:
#        pass
    with open('ss.jpg','wb') as fw:
        fw.write('')
