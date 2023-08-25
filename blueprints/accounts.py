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

baccounts = Blueprint("baccounts", __name__, template_folder="templates")

@baccounts.route("/account/", defaults={"id": "000000000"})
@baccounts.route("/account/<id>/")
def account(id):
    return render_template(Account(id).account)

@baccounts.route("/full", defaults={"id": "000000000"})
@baccounts.route("/full/<id>/")
def account_full(id):
    account = Account(id)
    return render_template({"account": account.account, "country": account.country, "valute":account.valute})