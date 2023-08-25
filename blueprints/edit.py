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

bedit = Blueprint("bedit", __name__, template_folder="templates")

@bedit.route("/countries/")
def countries():
    args = dict(request.args)
    account = Account(args["id"], "", True)

    if KEY != args["key"]: abort(406)
    if hashlib.md5(str(args["id"]+args["cid"]+str(KEY)+str(SECRET)).encode()).hexdigest() != args["hash"]: abort(406)
      
    if account.account["banned"]: return render_template("Ваш аккаунт забанен.")
    if account.account["moderation"]: return render_template("Ваша страна на модерации.")

    account.account["moderation"] = True
    account.account["cid"] = args["cid"]
    account.country["name"] = args["name"]
    account.country["flag"] = args["flag"].replace("&amp;", "&")
    account.country["group"] = args["group"]
    account.country["goverment_type"] = args["goverment_type"]
    account.country["goverment_form"] = args["goverment_form"]
    account.country["ideology"] = args["ideology"]
    account.country["political_type"] = args["political_type"]
    account.country["desc"] = markdown(args["desc"])
    account.country["date"] = args["date"]

    account.write()

    vk(f"{request.remote_addr} county edit {account.account['id']}")

    if account.registry:
        return render_template("Ваша страна зарегестрирована.")
    else:
        return render_template("Ваша страна изменена.")

@bedit.route("/valutes/")
def valutes():
    args = dict(request.args)
    account = Account(args["id"])

    if KEY != args["key"]: abort(406)
    if hashlib.md5(str(args["id"]+args["vid"]+KEY+SECRET).encode()).hexdigest() != args["hash"]: abort(406)
      
    if account.account["banned"]: return render_template("Ваш аккаунт забанен.")
    if account.account["moderation"]: return render_template("Ваша страна на модерации.")
    if account.country["check"] == "query": return render_template("Ваша страна ещё не принята.")

    account.account["moderation"] = True
    account.account["vid"] = args["vid"]
    account.valute["name"] = args["name"]
    account.valute["photo"] = args["photo"]
    account.valute["desc"] = markdown(args["desc"])
    account.valute["symbol"] = args["symbol"]
    account.valute["abbreviation"] = args["abbreviation"]
    account.valute["change"] = args["change"]

    account.write()

    vk_log(f"{request.remote_addr} valute edit {account.account['id']}")

    return render_template("Ваша валюта изменена.")