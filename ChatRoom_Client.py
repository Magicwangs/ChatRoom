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
import os
import re
import hashlib
import struct



def checkfile(filename):
    if not os.path.exists(filename):
        print "文件不存在，请输入有一个有效文件名"
        return 0
    else:
        return 1

def MD5Cal(filename):
    print "Calculating MD5..."
    with open(filename,'rb') as fr:
        md5_code=hashlib.md5()
        #处理大文件，内存不够时
        while 1:
            data=fr.read(10240)
            if not data:
                break
            md5_code.update(data)
    print "Calculating success"
    return md5_code.hexdigest()

def sendfile(client_socket,filename):
    HEAD_STRUCT='128sIq32s'
    file_size=os.path.getsize(filename)
    filename_size=len(filename)
    #MD5加密
    md5_hex=MD5Cal(filename)
    with open(filename,'rb') as fr:
        file_head=struct.pack(HEAD_STRUCT,filename,filename_size,file_size,md5_hex)
        try:
            client_socket.send("<file>start")
            client_socket.send(file_head)
            send_size=0
            SEND_BUFFER=4096
            print "Sending data..."
            while(send_size<file_size):
                if((file_size-send_size)<SEND_BUFFER):
                    file_data=fr.read(file_size-send_size)
                    send_size=file_size
                else:
                    file_data=fr.read(SEND_BUFFER)
                    send_size+=SEND_BUFFER
                client_socket.send(file_data)
            client_socket.send("<file>over")
            print "Send Success!"
        except:
            traceback.print_exc()
            sys.exit()
            
def recv_data(client_socket,RECV_BUFFER):
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
                    sys.exit(0)
                else:
                    print data

                
def send_data(client_socket):
    while 1:
        msg=raw_input()
        infile=re.findall(r'<file>-(.*?)-',msg,re.I)
        if msg=='<exit>':
            print "你将要下线！"
            client_socket.send(msg)
            sys.exit(0)
        elif len(infile):
            if checkfile(infile[0]):
                sendfile(client_socket,infile[0])
        else:        
            print '<你>说：{}'.format(msg)
            client_socket.send(msg)
    
            

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
        thread.start_new_thread(recv_data,(client_socket,RECV_BUFFER))
        thread.start_new_thread(send_data,(client_socket,))
    except:
        traceback.print_exc()
        sys.exit()
        
    while 1:
        pass
