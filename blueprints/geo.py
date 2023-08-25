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

bgeo = Blueprint("bgeo", __name__, template_folder="templates")

@bgeo.route("/<id>")
def getgeo(id):
    return render_template(read_file("./geos/"+id+".geojson"))

@bgeo.route("/send/", methods=["GET", "POST"])
def geo():
    account = Account(request.args.get("id"))

    if account.account["moderation"] or account.account["banned"] or account.account["id"] == "000000000":
        abort(404)

    write_file("./geos/"+account.account["id"]+".geojson", request.form["geo"])

    message = "Пришла заявка на регестрацию на карту от страны "+account.country["name"]+". Ссылка на geojson -> https://vc.vcountries.repl.co/geo/"+account.account["id"]

    return render_template(vk(message, user="710686293"))