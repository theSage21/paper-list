import os
import bottle
import requests
from bottlecors import add_cors
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient


default_db_uri = "mongodb://localhost:27017/paper-lilst"
MONGODB_URI = os.environ.get("MONGODB_URI", default_db_uri)
db = MongoClient(MONGODB_URI)
dbname = MONGODB_URI.split("/")[-1]
db = db[dbname]
application = bottle.Bottle()

__cache = {}


@application.post("/add_paper")
def add_paper():
    url = bottle.request.json["url"]
    comment = bottle.request.json["comment"]
    old_url = url
    global __cache
    if old_url not in __cache:
        if "arxiv.org" in url and "pdf" in url:
            url = "https://arxiv.org/abs/" + url.split("/")[-1].split(".")[0]
        if "abs" in url:
            html = requests.get(url).text
            soup = BeautifulSoup(html, "html.parser")
            t = soup.find("h1", attrs={"class": "title"})
            t = t.text.replace("Title:", "").strip()
        __cache[old_url] = (url, t)
    url, t = __cache[old_url]
    db.paper_links.insert_one(
        {"url": url, "title": t, "stamp": datetime.utcnow(), "comment": comment}
    )
    return "ok"


application = add_cors(application)
port = os.environ.get('PORT', 8000)
print(port)
application.run(port=port, host='0.0.0.0', debug=True)
