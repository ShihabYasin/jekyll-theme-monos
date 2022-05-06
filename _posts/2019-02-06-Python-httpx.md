---
layout: post 
title: Python-FTP
date: 2019-02-06 16:20:23 +0900 
category: Python 
tag: Python FTP 
---

## The [httpx](https://pypi.org/project/httpx/) allows to create both synchronous and asynchronous HTTP requests.


### 1. httpx GET request example:
```python
#!/usr/bin/python
import httpx 
r = httpx.get('http://google.com', params ={}) # Send query parameters as params dict if need
print(r.text)

```

### 2. httpx POST form request example: 
```python
#!/usr/bin/python
import httpx 
payload = {'name': 'Marry', 'occupation': 'software dev'}
r = httpx.post('https://httpbin.org/post', data=payload)
print(r.text)
```

### 3. Getting stream data:
```python
#!/usr/bin/python
import httpx

url = 'https://download.freebsd.org/ftp/releases/amd64/amd64/ISO-IMAGES/12.0/FreeBSD-12.0-RELEASE-amd64-mini-memstick.img'
with open('FreeBSD-12.0-RELEASE-amd64-mini-memstick.img', 'wb') as f:
    with httpx.stream('GET', url) as r:
        for chunk in r.iter_bytes():
            f.write(chunk)
```
### 4. Asynchronous GET request(multiple) example:
```python
#!/usr/bin/python
import httpx
import asyncio

async def get_async(url):
    async with httpx.AsyncClient() as client:
        return await client.get(url)
urls = ["http://webcode.me", "https://httpbin.org/get"]
async def launch():
    resps = await asyncio.gather(*map(get_async, urls))
    data = [resp.text for resp in resps]
    
    for html in data:
        print(html)
asyncio.run(launch())
```

### 5.  Asynchronous POST form request example:
```python
#!/usr/bin/python

import httpx
import asyncio

async def main():

    data = {'name': 'Marry', 'occupation': 'engineer'}

    async with httpx.AsyncClient() as client:
        r = await client.post('https://httpbin.org/post', data=data)
        print(r.text)

asyncio.run(main())

```
### 6. Python httpx async POST JSON request example:
```python
#!/usr/bin/python

import httpx
import asyncio

async def main():

    data = {'int': 123, 'boolean': True, 'list': ['a', 'b', 'c']}

    async with httpx.AsyncClient() as client:
        r = await client.post('https://httpbin.org/post', json=data)
        print(r.text)

asyncio.run(main())
```

### 7. Asynchronous stream request:
```python
#!/usr/bin/python

import httpx
import asyncio

url = 'https://download.freebsd.org/ftp/releases/amd64/amd64/ISO-IMAGES/12.0/FreeBSD-12.0-RELEASE-amd64-mini-memstick.img'
async def main():
    with open('FreeBSD-12.0-RELEASE-amd64-mini-memstick.img', 'wb') as f:

        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as r:
                
                async for chunk in r.aiter_bytes():
                    f.write(chunk)

asyncio.run(main())
```

