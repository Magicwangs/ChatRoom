# ChatRoom
ChatRoom For Experiment

## Function of setsockopt()
[Python中文文档——socket](http://python.usyiyi.cn/translate/python_278/library/socket.html)
假如端口被socket使用过，并且利用`socket.close()`来关闭连接，但此时端口还没有释放，要经过一个TIME_WAIT的过程之后才能使用，这是TNN的相当烦银的，为了实现端口的马上复用，可以通过设置`setsockopt()`函数来达到目的。
在`bind()`绑定前调用`setsockopt()`允许套接字地址重用

具体设置参数可以参看[这里](http://www.cnblogs.com/xiaowuyi/archive/2012/08/06/2625509.html)
setsockopt(level,optname,value)
level定义了哪个选项将被使用。通常情况下是SOL_SOCKET，意思是正在使用的socket选项。
optname参数提供使用的特殊选项,SO_REUSEADDR意思是当socket关闭后，本地端用于该socket的端口号立刻就可以被重用。通常来说，只有经过系统定义一段时间后，才能被重用。
value为1表示启用

## About select Module
Waiting for I/O completion
select同时监控多个sockets、文件、管道,直到它们变成可读可写或发生通讯错误

select(rlist, wlist, xlist[, timeout])
rlist: wait until ready for reading；
wlist: wait until ready for writing；
xlist:wait for an “exceptional condition”--ERROR
select()

返回的3个列表和输入类似：readable，writable，exceptional。
readable有3种可能：对于用来侦听连接主服务器socket，表示已准备好接受一个到来的连接；对于已经建立并发送数据的链接，表示有数据到来；如果没数据到来，表示链接已经关闭。
writable的情况：连接队列中有数据，发送下一条消息。如果队列中无数据，则从output队列中删除。
socket有错误，也要从output队列中删除。

Select的第四个参数可以设置超时。超时时，select()返回3个空列表。
[select — Waiting for I/O completion](http://python.usyiyi.cn/translate/python_278/library/index.html)
[python模块介绍- select 等待I/0完成](http://my.oschina.net/u/1433482/blog/191211)


## Reference
[用Python实现聊天室的一些感想](http://tonnie17.github.io/2015/12/11/chatroom/)
[Python Socket 编程——聊天室示例程序](http://www.cnblogs.com/hazir/p/python_chat_room.html)
