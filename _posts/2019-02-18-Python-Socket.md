---
layout: post
title: Python-Socket
date: 2019-02-18 16:20:23 +0900
category: Python
tag: Python
---




<html lang="en">

<head>

</head>

<body>

<header>



</header>

<div class="container">


<div class="content">

<h1>Python Socket</h1>



<p>
Python Socket tutorial shows how to do Python network programming with sockets.
Socket programming is low-level. The goal of this tutorial is to introduce
network programming including these low-level details. There are higher-level Python
APIs such as Twisted that might be better suited.
</p>


<p>
In programming, a <dfn>socket</dfn> is an endpoint of a communication between
two programs running on a network. Sockets are used to create a connection
between a client program and a server program.
</p>



<p>
Python's <code>socket</code> module provides an interface to the Berkeley sockets API.
</p>

<div class="note">
<strong>Note:</strong> In networking, the term socket has a different meaning.
It is used for the combination of an IP address and a port number.
</div>


<h2>Network protocols</h2>

<p>
TCP/IP is a suite of protocols used by devices to communicate over the Internet
and most local networks. TCP is more reliable, has extensive error checking, and
requires more resources. It is used by services such as HTTP, SMTP, or FTP. UDP
is much less reliable, has limited error checking, and requires less resources.
It is used by services such as VoIP.
</p>

<p>
The <code>socket.SOCK_STREAM</code> is used to create a socket for TCP and
<code>socket.SOCK_DGRAM</code> for UDP.
</p>

<h2>Address families</h2>

<p>
When we create a socket, we have to specify its address family. Then
we can only use addresses of that type with the socket.
</p>

<ul>
<li>AF_UNIX, AF_LOCAL - Local communication</li>
<li>AF_INET - IPv4 Internet protocols</li>
<li>AF_INET6 - IPv6 Internet protocols</li>
<li>AF_IPX - IPX - Novell protocols</li>
<li>AF_BLUETOOTH - Wireless bluetooth protocols</li>
<li>AF_PACKET - Low level packet interface</li>
</ul>

<p>
For the <code>AF_INET</code> address family, a pair (host, port) is specified.
The <code>host</code> is a string representing either a hostname in
Internet domain notation like <code>example.com</code> or an IPv4 address like
<code>93.184.216.34</code>, and port is an integer.
</p>

<!-- <p>
Datagram socket is a socket for sending and receiving datagram packets.
A datagram packet is represented by <code>DatagramPacket</code> class.
Each packet sent or received on a datagram socket is individually
addressed and routed. Multiple packets sent from one machine to another may
be routed differently, and may arrive in any order.
</p> -->

<h2>Python get IP address</h2>

<p>
With <code>gethostbyname</code>, we get the IP address of the host.
</p>

<div class="codehead">get_ip.py</div>
<pre class="code">
#!/usr/bin/env python

import socket

ip = socket.gethostbyname('example.com')
print(ip)
</pre>

<p>
The example prints the IP address of <code>example.com</code>.
</p>

<pre class="compact">
$ ./get_ip.py
93.184.216.34
</pre>


<h2>Python UDP socket example</h2>

<p>
UDP is a communication protocol that transmits independent packets over the
network with no guarantee of arrival and no guarantee of the order of delivery.
One service that used UDP is the Quote of the Day (QOTD).
</p>

<div class="codehead">qotd_client.py</div>
<pre class="code">
#!/usr/bin/env python

import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

message = b''
addr = ("djxmmx.net", 17)

s.sendto(message, addr)

data, address = s.recvfrom(1024)
print(data.decode())
</pre>

<p>
The example creates a client program that connects to a QOTD service.
</p>

<pre class="compact">
import socket
</pre>

<p>
We import the <code>socket</code> module.
</p>

<pre class="compact">
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
</pre>

<p>
A datagram socket for IPv4 is created.
</p>

<pre class="compact">
message = b''
</pre>

<p>
We send an empty message; the QOTD service works by sending arbitrary
data to the socket; it simply responds with a quote. To communicate over
TCP/UDP, we use binary strings.
</p>

<pre class="compact">
addr = ("djxmmx.net", 17)
</pre>

<p>
We provide the address and the port.
</p>

<pre class="compact">
s.sendto(message, addr)
</pre>

<p>
We send data with the <code>sendto</code> method.
</p>

<pre class="compact">
data, address = s.recvfrom(1024)
</pre>

<p>
UDP sockets use <code>recvfrom</code> to receive data. Its paremeter is the
buffer size. The return value is a pair (data, address) where data is a byte
string representing the data received and address is the address of the socket
sending the data.
</p>

<pre class="compact">
print(data.decode())
</pre>

<p>
We print the decoded data to the terminal.
</p>

<pre class="compact">
$ ./qotd_client.py
"Oh the nerves, the nerves; the mysteries of this machine called man!
Oh the little that unhinges it, poor creatures that we are!"
Charles Dickens (1812-70)
</pre>

<p>
This is a sample output.
</p>

<h2>Python TCP socket example</h2>

<p>
The are servers that provide current time. A client simply connects to the
server with no commands, and the server responds with a current time.
</p>

<div class="note">
<strong>Note:</strong> Time servers come and go, so we might
need to find a working server on https://www.ntppool.org/en/.
</div>

<br>

<div class="codehead">time_client.py</div>
<pre class="code">
#!/usr/bin/env python

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

host = "time.nist.gov"
port = 13

s.connect((host, port))
s.sendall(b'')
print(str(s.recv(4096), 'utf-8'))
</pre>

<p>
The example determines the current time by connecting to a time
server's TCP socket.
</p>

<pre class="explanation">
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
</pre>

<p>
A TCP socket for IPv4 is created.
</p>

<pre class="explanation">
host = "time.nist.gov"
port = 13
</pre>

<p>
This is the host name and the port number of a working time server.
</p>

<pre class="explanation">
s.connect((host, port))
</pre>

<p>
We connect to the remote socket with <code>connect</code>.
</p>

<pre class="explanation">
s.sendall(b'')
</pre>

<p>
The <code>sendall</code> method sends data to the socket. The socket must be
connected to a remote socket. It continues to send data from bytes until either
all data has been sent or an error occurs.
</p>

<pre class="explanation">
print(str(s.recv(4096), 'utf-8'))
</pre>

<p>
We print the received data. The <code>recv</code> method receives up to
buffersize bytes from the socket. When no data is available, it blocks until at
least one byte is available or until the remote end is closed. When the remote
end is closed and all data is read, it returns an empty byte string.
</p>


<h2>Python Socket HEAD request</h2>

<p>
A HEAD request is a GET request without a message body. The header of
a request/response contains metadata, such as HTTP protocol version or
content type.
</p>

<div class="codehead">head_request.py</div>
<pre class="code">
#!/usr/bin/env python

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

s.connect(("webcode.me" , 80))
s.sendall(b"HEAD / HTTP/1.1\r\nHost: webcode.me\r\nAccept: text/html\r\n\r\n")
print(str(s.recv(1024), 'utf-8'))
</pre>

<p>
In the example, we send a HEAD request to <code>webcode.me</code>.
</p>

<pre class="explanation">
s.sendall(b"HEAD / HTTP/1.1\r\nHost: webcode.me\r\nAccept: text/html\r\n\r\n")
</pre>

<p>
A head request is issued with the <code>HEAD</code> command followed by the
resource URL and HTTP protocol version. Note that the <code>\r\n</code> are
mandatory part of the communication process. The details are described
in <a href="https://tools.ietf.org/html/rfc7231">RFC 7231</a> document.
</p>

<pre class="compact">
$ head_request.py
HTTP/1.1 200 OK
Server: nginx/1.6.2
Date: Sun, 08 Sep 2019 11:23:25 GMT
Content-Type: text/html
Content-Length: 348
Last-Modified: Sat, 20 Jul 2019 11:49:25 GMT
Connection: keep-alive
ETag: "5d32ffc5-15c"
Accept-Ranges: bytes
</pre>



<h2>Python Socket GET request</h2>

<p>
The HTTP GET method requests a representation of the specified resource.
Requests using GET should only retrieve data.
</p>

<div class="codehead">get_request.py</div>
<pre class="code">
#!/usr/bin/env python

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

s.connect(("webcode.me" , 80))
s.sendall(b"GET / HTTP/1.1\r\nHost: webcode.me\r\nAccept: text/html\r\nConnection: close\r\n\r\n")

while True:

data = s.recv(1024)

if not data:
break

print(data.decode())
</pre>

<p>
The example reads the home page of the <code>webcode.me</code> using a
GET request.
</p>

<pre class="explanation">
s.sendall(b"GET / HTTP/1.1\r\nHost: webcode.me\r\nAccept: text/html\r\nConnection: close\r\n\r\n")
</pre>

<p>
For the HTTP 1.1 protocol, the connections may be persistent by default. This is why we
send the <code>Connection: close</code> header.
</p>

<pre class="explanation">
while True:

data = s.recv(1024)

if not data:
break

print(data.decode())
</pre>

<p>
We use a while loop to process the received data. If no error occurs,
<code>recv</code> returns the bytes received. If the connection has
been gracefully closed, the return value is an empty byte string.
The <code>recv</code> is a blocking method that blocks until it is
done, or a timeout is reached or another exception occurs.
</p>

<pre class="compact">
$ ./get_request.py
HTTP/1.1 200 OK
Server: nginx/1.6.2
Date: Sun, 08 Sep 2019 11:39:34 GMT
Content-Type: text/html
Content-Length: 348
Last-Modified: Sat, 20 Jul 2019 11:49:25 GMT
Connection: keep-alive
ETag: "5d32ffc5-15c"
Access-Control-Allow-Origin: *
Accept-Ranges: bytes

&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
&lt;meta charset="UTF-8"&gt;
&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
&lt;title&gt;My html page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;

&lt;p&gt;
Today is a beautiful day. We go swimming and fishing.
&lt;/p&gt;

&lt;p&gt;
Hello there. How are you?
&lt;/p&gt;

&lt;/body&gt;
&lt;/html&gt;
</pre>



<h2>Echo client server example</h2>

<p>
An echo server sends the message from the client back. It is a
classic example used for testing and learning.
</p>

<div class="codehead">echo_server.py</div>
<pre class="code">
#!/usr/bin/env python

import socket
import time

with socket.socket() as s:

host = 'localhost'
port = 8001

s.bind((host, port))
print(f'socket binded to {port}')

s.listen()

con, addr = s.accept()

with con:

while True:

data = con.recv(1024)

if not data:
break

con.sendall(data)
</pre>

<p>
The echo server sends the client message back to the client.
</p>

<pre class="explanation">
host = 'localhost'
port = 8001
</pre>

<p>
The server runs on localhost on port 8001.
</p>

<pre class="explanation">
s.bind((host, port))
</pre>

<p>
The <code>bind</code> method establishes the communication endpoint.
It binds the socket to the specified address. The socket must not already be bound.
(The format of address depends on the address family.)
</p>

<pre class="explanation">
s.listen()
</pre>

<p>
The <code>listen</code> method enables a server to accept connections. The
server can now listen for connections on a socket. The <code>listen</code>
has a <code>backlog</code> parameter. It specifies the number of unaccepted
connections that the system will allow before refusing new connections.
The parameter is optional since Python 3.5. If not specified, a default backlog
value is chosen.
</p>

<pre class="explanation">
con, addr = s.accept()
</pre>

<p>
With <code>accept</code>, the server accepts a connection. It blocks and waits
for an incoming connection. The socket must be bound to an address and listening
for connections. The return value is a pair (con, addr) where con is a new
socket object usable to send and receive data on the connection, and addr is
the address bound to the socket on the other end of the connection.
</p>

<p>
Note that the <code>accept</code> creates a new socket for communication with
a client, which is a different socket from the listening socket.
</p>

<div class="codehead">echo_client.py</div>
<pre class="code">
#!/usr/bin/env python

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

host = "localhost"
port = 8001

s.connect((host, port))
s.sendall(b'hello there')
print(str(s.recv(4096), 'utf-8'))
</pre>

<p>
The client sends a message to the echo server.
</p>

<h2>Asynchronous server example</h2>

<p>
In order to improve the performance of a server, we can use the
<code>asyncio</code> module.
</p>

<div class="codehead">async_server.py</div>
<pre class="code">
#!/usr/bin/env python

# from threading import current_thread

import asyncio


async def handle_client(reader, writer):

data = (await reader.read(1024))

writer.write(data)
writer.close()


loop = asyncio.get_event_loop()
loop.create_task(asyncio.start_server(handle_client, 'localhost', 8001))
loop.run_forever()
</pre>

<p>
We can now test the performance of the blocking and non-blocking servers.
</p>

<pre class="compact">
$ ab -c 50 -n 1000 http://localhost:8001/
</pre>

<p>
For instance, we can test the performance with the Apache benchmarking tool.
In our case, the command sends 1000 requests, 50 at a time.
</p>





</div> <!-- content -->

<div class="rtow">


</div>

</div> <!-- container -->

<footer>


</footer>

</body>
</html>
