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

badmin = Blueprint("badmin", __name__, template_folder="templates")

@badmin.route("/")
def admin():
    return render_template("/admin.html", True)

@badmin.route("/send/", methods=["GET", "POST"])
def admin_send():
    if request.form["admin"] == ADMIN:
        account = Account(request.form["fid"])
        action = ""

        if account.account["id"] != "000000000" and account.account["id"] != "-111111111":
            if request.form["type-action"] == "country":
                if request.form["country-action"] == "check-query": account.country["check"] = "query"
                elif request.form["country-action"] == "check-no": account.country["check"] = "no"
                elif request.form["country-action"] == "check-partial": account.country["check"] = "partial"
                elif request.form["country-action"] == "check-full": account.country["check"] = "full"

                action = request.form["country-action"]
            elif request.form["type-action"] == "valute":
                if request.form["valute-action"] == "check-query": account.valute["check"] = "query"
                elif request.form["valute-action"] == "check-no": account.valute["check"] = "no"
                elif request.form["valute-action"] == "check-partial": account.valute["check"] = "partial"
                elif request.form["valute-action"] == "check-full": account.valute["check"] = "full"

                action = request.form["valute-action"]
            elif request.form["type-action"] == "account":
                if request.form["account-action"] == "mod": account.account["moderation"] = True
                elif request.form["account-action"] == "ban": account.account["banned"] = True
                elif request.form["account-action"] == "admin": account.account["admin"] = True
                elif request.form["account-action"] == "unmod": account.account["moderation"] = False
                elif request.form["account-action"] == "unban": account.account["banned"] = False
                elif request.form["account-action"] == "unadmin": account.account["admin"] = False

                action = request.form["account-action"]
            elif request.form["type-action"] == "specific":
                if request.form["specific-action"] == "country-no": 
                    account.account["moderation"] = False
                    account.country["check"] = "no"
                elif request.form["specific-action"] == "country-partial": 
                    account.account["moderation"] = False
                    account.country["check"] = "partial"
                elif request.form["specific-action"] == "country-full": 
                    account.account["moderation"] = False
                    account.country["check"] = "full"
                elif request.form["specific-action"] == "valute-no": 
                    account.account["moderation"] = False
                    account.valute["check"] = "no"
                elif request.form["specific-action"] == "valute-partial": 
                    account.account["moderation"] = False
                    account.valute["check"] = "partial"
                elif request.form["specific-action"] == "valute-full": 
                    account.valute["moderation"] = False
                    account.valute["check"] = "full"

                action = request.form["specific-action"]

            account.write()

            log = read_file("logs.json")
            log.append(f"{{{str(datetime.datetime.now())}}} {request.form['type-action']} {action} {request.form['id']}")
            write_file("logs.json", log)
          
            return render_template("admin_send.html", True, ret="Done: "+vk(f"{request.form['type-action']} {action} {request.form['id']}"))
        else:
            return render_template("admin_send.html", True, ret="Wrong ID")
    else:
        return render_template("admin_send.html", True, ret="Wrong admin password")