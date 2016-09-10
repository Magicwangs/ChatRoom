# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 15:28:18 2016

@author: MagicWang
"""
import socket
import select
import sys
import traceback

#broadcast chat messages
def broadcast_data(sock,message,server_socket,CONNECTION_LIST):
    for s in CONNECTION_LIST:
        #排除服务器和本机
        if s!=server_socket and s!=sock:
            try:
                s.send(message)
            except:
                #print except error
                traceback.print_exc()
                s.close()
                CONNECTION_LIST.remove(s)

#close client
def close_client_socket(sock,server_socket,CONNECTION_LIST):
    #getpeername():获取socket的host和port
    clienthost,clientport=sock.getpeername()
    broadcast_data(sock,'[{}:{}]已经下线\n'.format(clienthost,clientport),server_socket,CONNECTION_LIST)
    #控制台输出    
    print '客户端[{}:{}]已经下线了\n'.format(clienthost,clientport)
    #控制台刷新
    sys.stdout.flush()
    sock.close()
    CONNECTION_LIST.remove(s)
    

if __name__=="__main__":
    ADDRESS=('127.0.0.1',7000)
    RECV_BUFFER=4096
    CONNECTION_LIST=[]
    try:
        #AF_UNIX用于同一台机器上的进程间通信，AF_INET对于IPV4协议的TCP和UDP
        #SOCK_STREAM:面向连接TCP；SOCK_DGRAM无连接UDP
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #socket option:当socket关闭后，本地端用于该socket的端口号立刻就可以被重用
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(ADDRESS)
        #最大连接数为1
        server_socket.listen(10)
    except:
        print 'Socket Create ERROR!'
        sys.exit()
    #add server_socket
    CONNECTION_LIST.append(server_socket)
    #多客户端聊天，不能采用堵塞的accept(),可以通过select轮询
    while 1:
        #r_sockets中有两种情况：
        #一是服务端socket可读，表示有新的客户端连接到聊天室
        #二是客户端socket可读，表示聊天室里有某个客户端在发言
        r_sockets,w_sockets,e_sockets=select.select(CONNECTION_LIST,[],[])
        for s in r_sockets:
            #如果聊天列表中的服务器端socket可读，则把socket接受得到的客户端socket添加到连接列表中。
            if s==server_socket:
                clientsock,clientaddr=s.accept()
                CONNECTION_LIST.append(clientsock)
                try:
                    broadcast_data(clientsock,'[{}:{}]进入房间\n'.format(*clientsock.getpeername()),server_socket,CONNECTION_LIST)
                    print '当前聊天室人数：{}\n'.format(len(CONNECTION_LIST)-1)
#                    sys.stdout.flush()
                except:
                    traceback.print_exc()
            #如果聊天列表中的客户端socket可读，则把socket中的数据取出（即发言记录）分发给连接列表中的其它客户端socket
            else:
                try:
                    data=s.recv(RECV_BUFFER)
                    if data:
                        #如果客户端输入<exit>就退出
                        if data=='<exit>\n':
                            close_client_socket(s,server_socket,CONNECTION_LIST)
                        else:
                            clienthost, clientport = s.getpeername()
                            msg='<{}:{}>说:{}'.format(clienthost, clientport, data)
                            broadcast_data(s,msg,server_socket,CONNECTION_LIST)
                except:
                    traceback.print_exc()
                    close_client_socket(s,server_socket,CONNECTION_LIST)
                    continue
    server_socket.close()
                    