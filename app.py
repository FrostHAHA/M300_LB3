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