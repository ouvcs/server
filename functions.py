import flask
import requests
import os
import json
from markdownify import markdownify
from markdown import markdown
import datetime
from fuzzywuzzy.fuzz import WRatio

VK_OOVC = os.environ.get("vk_oovc")
VK_ADMIN = os.environ.get("vk_admin")
KEY = os.environ.get("key")
SECRET = os.environ.get("secret")
ADMIN = os.environ.get("admin")

def read_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.loads(f.read())

def write_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(content, ensure_ascii=False, indent=4))

def vk(message):
    return requests.get(f"https://api.vk.com/method/messages.send?access_token={VK_ADMIN}&random_id=0&message={message}&peer_id=2000000003&v=5.131").text

def render_template(content, render=False, type=".json", **kwargs):
    if render:
        return flask.render_template(content, **kwargs)
    else:
        if type == ".json":
            return flask.Response(response=json.dumps(content, ensure_ascii=False, indent=4), status=200, mimetype="application/json")
        elif type == ".css":
            return flask.Response(response=str(content), status=200, mimetype="text/css")
        else:
            return flask.Response(response=str(content), status=200, mimetype="text/plain")
    
class Account():
    id = "000000000"
    registry = False
    search_percent = 0
    account = {
        "moderation": False,
        "banned": False,
        "admin": False,
        "id": "000000000",
        "cid": "neizvestno",
        "vid": "neizvestno"
    }
    country = {
        "id": "000000000",
        "cid": "neizvestno",
        "flag": "/static/images/country/profile.png", 
        "name": "Неизвестно", 
        "group": "https://vk.com/vgovernments", 
        "goverment_type": "Неизвестный", 
        "goverment_form": "Неизвестный", 
        "ideology": "Неизвестна", 
        "political_type": "Неизвестный",
        "desc": "",
        "date": "00 00 0000",
        "add": "",
        "check": "query"
    }
    valute = {
        "id": "000000000",
        "vid": "neizvestno",
        "name": "Неизвестно",
        "photo": "/static/images/country/profile.png",
        "desc": "",
        "change": 1.0,
        "abbreviation": "NZV",
        "symbol": "",
        "add": "",
        "check": "query"
    }

    def __init__(self, id: str, search:str="", regitry_allowed=False):
        for d in os.listdir("./data/"):
            a = read_file(f"./data/{d}/account.json")
            if a["cid"] == id or a["vid"] == id or a["id"] == id:
                self.id = a["id"]

        if self.id == "000000000": self.id = id

        if self.id in os.listdir("./data/"):
            self.account = read_file(f"./data/{self.id}/account.json")

            self.country["id"] = self.account["id"]
            self.country["cid"] = self.account["cid"]
            self.valute["id"] = self.account["id"]
            self.valute["vid"] = self.account["vid"]

            self.country = {**self.country, **read_file(f"./data/{self.id}/country.json")}
            self.valute = {**self.valute, **read_file(f"./data/{self.id}/valute.json")}

            if search != "" and search != None:
                search = search.lower()
                searches_percents = [WRatio(search, self.account["id"].lower()), 
                                     WRatio(search, self.account["cid"].lower()), 
                                     WRatio(search, self.account["vid"].lower()),

                                     WRatio(search, self.country["name"].lower()), 
                                     WRatio(search, self.country["group"].lower()), 
                                     WRatio(search, self.country["date"].lower()),

                                     WRatio(search, self.valute["name"].lower()), 
                                     WRatio(search, self.valute["abbreviation"].lower()), 
                                     WRatio(search, self.valute["symbol"].lower())]
                
                self.search_percent = max(searches_percents)

        else:
            if regitry_allowed:
                self.account["id"] = self.id
                self.account["cid"] = self.id
                self.account["vid"] = self.id

                self.registry = True

        response = requests.get(f"https://api.vk.com/method/users.get?user_ids={ self.account['id'] }&fields=photo_200,screen_name&v=5.131&access_token={ VK_ADMIN }&lang=0").json()
        try:
            self.account["photo"] = response["response"][0]["photo_200"]
            self.account["screen_name"] = response["response"][0]["screen_name"]
            self.account["name"] = response["response"][0]["first_name"]+" "+response["response"][0]["last_name"]
        except:
            self.account["photo"] = "/static/images/defaults/profile.png"
            self.account["screen_name"] = "neizvestno"
            self.account["name"] = "Неизвестно"


    def write(self):
        if self.registry:
            os.mkdir(f"./data/{self.id}")

        self.country.pop("id")
        self.account["cid"] = self.country.pop("cid")
        self.valute.pop("id")
        self.account["vid"] = self.valute.pop("vid")
      
        self.account.pop("photo")
        self.account.pop("name")
        self.account.pop("screen_name")

        write_file(f"./data/{self.id}/account.json", self.account)
        write_file(f"./data/{self.id}/country.json", self.country)
        write_file(f"./data/{self.id}/valute.json", self.valute)

        self.country["id"] = self.account["id"]
        self.country["cid"] = self.account["cid"]
        self.valute["id"] = self.account["id"]
        self.valute["vid"] = self.account["vid"]