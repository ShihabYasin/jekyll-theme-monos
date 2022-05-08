---
layout: post 
title: Python-FTP
date: 2019-02-05 16:20:23 +0900 
category: Python 
tag: Python FTP 
---


## Python FTP 
###  Connect to FTP servers ( e.g: Debian FTP server), list directories, download and upload files

### Python [ftplib](https://pypi.org/project/pyftpdlib/)   

Python ftplib is a module that implements the client side of the FTP protocol. It contains an FTP client class and some helper functions.
Let's work work with ```ftp.debian.org``` FTP server.
 

### 1. Get the connection and get list of available files: 
```python
#!/usr/bin/python3
import ftplib
with ftplib.FTP('ftp.debian.org') as ftp:    
    try:
        ftp.login()  
        files = []
        ftp.dir(files.append)
        print(files)            
    except ftplib.all_errors as e:
        print('FTP error:', e)
```


### 2. Getting size of text file: 

```python
#!/usr/bin/python3
import ftplib 
with ftplib.FTP('ftp.debian.org') as ftp: 
    try:
        ftp.login()  
        size = ftp.size('debian/README')
        print(size)
    except ftplib.all_errors as e:
        print('FTP error:', e) 
```

### 3. Download Text File: 


```python
#!/usr/bin/python3

import ftplib 
import os
with ftplib.FTP('ftp.debian.org') as ftp:
    file_orig = '/debian/README'
    file_copy = 'README'    
    try:
        ftp.login()  
        
        with open(file_copy, 'w') as fp:           
            res = ftp.retrlines('RETR ' + file_orig, fp.write)            
            if not res.startswith('226 Transfer complete'):                
                print('Download failed')
                if os.path.isfile(file_copy):
                    os.remove(file_copy)          
    except ftplib.all_errors as e:
        print('FTP error:', e)         
        if os.path.isfile(file_copy):
            os.remove(file_copy)
```

### 4. Uploading Text File:
```python
#!/usr/bin/python3
import ftplib 
with ftplib.FTP('ftp.example.com') as ftp:    
    filename = 'README'    
    try:    
        ftp.login('user7', 's$cret')          
        with open(filename, 'rb') as fp:            
            res = ftp.storlines("STOR " + filename, fp)            
            if not res.startswith('226 Transfer complete'):            
                print('Upload failed')
    except ftplib.all_errors as e:
        print('FTP error:', e)
```


