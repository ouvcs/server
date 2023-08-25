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

bcountries = Blueprint("bcountries", __name__, template_folder="templates")

@bcountries.route("/")
def countries():
    response = []
    search = request.args.get("search")

    for d in os.listdir("./data/"):
        account = Account(d, search=search)
        if account.account["moderation"] or account.account["banned"]:
            continue
        if search == None or account.search_percent >= 90:
            response.append(account.country)
    return render_template(response)

@bcountries.route("/country/<id>/")
def country(id):
    account = Account(id)
    if account.account["moderation"] or account.account["banned"]:
        abort(406)
    return render_template(account.country)

@bcountries.route("/preview/<id>/")
def country_preview(id):
    account = Account(id)
    if not (account.account["moderation"] or account.account["banned"]):
        abort(406)
    return render_template(account.country)