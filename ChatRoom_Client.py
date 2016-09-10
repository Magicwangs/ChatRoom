# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:12:24 2016

@author: MagicWang
"""
import select
import socket
import sys
import traceback
import thread


def recv_data(client_socket):
    while 1:
        #select在windows下不能监听stdin,只能采用多线程
        rlist=[client_socket]
        r_sockets,w_sockets,e_sockets=select.select(rlist,[],[])
        for s in r_sockets:
            #客户端socket可读，表示有数据可接收，或者断开连接了
            if s==client_socket:
                data=s.recv(RECV_BUFFER)
                #如果数据是空
                if not data:
                    print "\nDisconnected from chat server\n"
                    sys.exit()
                else:
                    print data
                    sys.stdout.flush()
                
def send_data(client_socket):
    while 1:
        msg=sys.stdin.readline()
        if msg=='<exit>\n':
            print "你将要下线！"
            client_socket.send(msg)
            sys.exit()
        else:        
            print '<你>说：{}'.format(msg)
            client_socket.send(msg)
            sys.stdout.flush()

if __name__=="__main__":
#    if(len(sys.argv)<3):
#        print 'Usage : python {} hostname port'.format(sys.argv[0])
#        sys.exit()
#    host=sys.argv[1]
#    port=int(sys.argv[2])
    host='127.0.0.1'
    port=7000
    RECV_BUFFER=4096

    try:
        client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.settimeout(2)
        client_socket.connect((host,port))
    except:
        traceback.print_exc()
        sys.exit()
    print 'Connected to remote host. Start sending messages'
    try:
        thread.start_new_thread(recv_data,(client_socket,))
        thread.start_new_thread(send_data,(client_socket,))
    except:
        traceback.print_exc()
        
    while 1:
        pass