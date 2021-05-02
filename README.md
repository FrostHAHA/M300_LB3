 ># **M300**  - LB3 
![Docker](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.brianweet.com%2Fassets%2Fdocker-blog-1%2Fdocker-logo.png&f=1&nofb=1) 
![Git](https://duckduckgo.com/i/d11b358b.png)
<br><br>

---


## Sections
- [Introduction](#introduction)
- [Description](#description)
- [app.py file](#app.pyfile)
- [Requirements](#requirements)
- [Dockerfile](#dockerfile)
- [Compose file](#composefile)
- [Links](#links)

# Introduction

This repository is made for my LB, which contains my small Docker project, which will be described in this document.
<br><br>

# Description
 
 The purpose of this repository is to create a Python web application running on Docker Compose. This application will keep a counter on how many times the site has been opened (http://localhost:5000/)
<br><br>


 # Code

## app.pyFile
```
## this file is used to count the number of times the localhost has been opened (http://localhost:5000/) , 
## everytime it is reopened, it will add a +1 to the counter. We can test this by refreshing the site

import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello Mr. Berger, this site has been seen {} times, try refreshing it!.\n'.format(count)
    
```

I used Redis for this project, it is the hostname and the container on the application's network. The default port for Redis is 6379
<br>
The function of this file is to count the number of times this site has been visited/refreshed.
<br><br>


## Requirements

This little txt File will be used to tell Docker what to install in its File, it has two simple names of things we need

```
flask
redis
```
<br>

## Dockerfile

```
# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
```

This Dockerfile builds an image starting with Python 3.7. Then it sets the working directory to /code and the variables used by the flash command. 
Other dependencies will be installed with gcc. 
<br>
The next step is to read the requirements.txt file that is in the directory, this file contains two Python depencencies that will be installed.
<br>
 Afterwards the metadata will be added to the image to tell the container to open the port 5000, the one that we will be using to open the local host site.
 <br>
And to finish it off it copies the current directory ```.```in the project to the workdir ```.``` in the image, then sets the default command for the container to ```flask run```.
<br>


<br>

## ComposeFile

```
version: "3.9"
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      FLASK_ENV: development
  redis:
    image: "redis:alpine"
```
This file defines the services ```web``` and ```redis```. 
<br>
The ```web``` service uses an image built from the ```Dockerfile ``` in the directory. Then it binds the container and the host machine on the port ```5000```, which happens to be the default port for the Flash web server.
At the beginning I did not have volumes, but I added it on the host, which is mount on /code inside the container, this allows me to modify the code whenever I want without having to take everything down and start it up again. ```Environment``` also helps with this, telling ```flask run``` to run in dev. mode, reloading the code whenever it is changed to reflect these changes.
<br>
And as for the ```redis``` service, it uses a public image pulled from Docker Hub registry.

<br>

 # Links

- [Kapitel 10](https://github.com/mc-b/M300/tree/master/10-Toolumgebung)
- [Kapitel 20](https://github.com/mc-b/M300/tree/master/20-Infrastruktur)
- [Kapitel 30](https://github.com/mc-b/M300/tree/master/30-Container)
- [Kapitel 35](https://github.com/mc-b/M300/tree/master/35-Sicherheit)


 <br><br>
