import flask
from flask import Blueprint, redirect, abort, session, request
import requests
import os
import json
from markdownify import markdownify
from markdown import markdown
import datetime
from fuzzywuzzy.fuzz import WRatio
import hashlib
from functions import *

butils = Blueprint("butils", __name__, template_folder="templates")

@butils.route("/id/", defaults={"id": ""})
@butils.route("/id/<id>")
def utils_id(id):
    response = ""
    if id != "":
        response = requests.get(f"https://api.vk.com/method/users.get?user_ids={ id }&fields=nickname,maiden_name,screen_name,photo_200&v=5.131&access_token={ VK_ADMIN }&lang=0").json()
        if "response" in response:
            response = response["response"][0]
        else:
            response = {"id": ""}
    return render_template(response)
    
