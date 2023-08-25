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

bvalutes = Blueprint("bvalutes", __name__, template_folder="templates")

@bvalutes.route("/")
def valutes():
    response = []
    search = request.args.get("search")

    for d in os.listdir("./data/"):
        account = Account(d, search=search)
        if account.account["moderation"] or account.account["banned"] or account.valute["vid"] == "neizvestno":
            continue
        if search == None or account.search_percent >= 90:
            response.append(account.valute)
    return render_template(response)

@bvalutes.route("/valute/<id>/")
def valute(id):
    account = Account(id)
    if account.account["moderation"] or account.account["banned"]:
        abort(406)
    return render_template(account.valute)

@bvalutes.route("/preview/<id>/")
def valute_preview(id):
    account = Account(id)
    if not (account.account["moderation"] or account.account["banned"]):
        abort(404)
    return render_template(account.valute)

@bvalutes.route("/change/<id>")
def valute_change(id):
    account = Account(id)
    response = []

    if account.account["moderation"] or account.account["banned"]:
        abort(406)

    for d in os.listdir("./data/"):
        to = Account(d)
        if to.account["moderation"] or to.account["banned"] or to.account["id"] == account.account["id"]:
            continue

        response.append({"valute": to.valute, "change": round(account.valute["change"]/to.valute["change"], 4)})
    return render_template(response)

@bvalutes.route("/change/<id>/<tid>")
def valute_change_to(id, tid):
    account = Account(id)
    to = Account(tid)

    if account.account["moderation"] or account.account["banned"] or to.account["moderation"] or to.account["banned"]:
        abort(406)
    
    response = {"valute": account.valute, "to": to.valute}
    response["change"] = round(account.valute["change"]/to.valute["change"], 4)

    return render_template(response)