import flask
from flask import Flask, redirect, abort, session, request
from werkzeug.exceptions import HTTPException
import requests
import os
import json
from markdownify import markdownify
from markdown import markdown
import datetime
from fuzzywuzzy.fuzz import WRatio
import hashlib
from functions import *

from blueprints.countries import bcountries
from blueprints.valutes import bvalutes
from blueprints.accounts import baccounts
from blueprints.admin import badmin
from blueprints.geo import bgeo
from blueprints.themes import bthemes
from blueprints.edit import bedit
from blueprints.utils import butils

app = Flask(__name__)

app.register_blueprint(bcountries, url_prefix="/countries")
app.register_blueprint(bvalutes, url_prefix="/valutes")
app.register_blueprint(baccounts, url_prefix="/accounts")
app.register_blueprint(badmin, url_prefix="/admin")
app.register_blueprint(bgeo, url_prefix="/geo")
app.register_blueprint(bthemes, url_prefix="/themes")
app.register_blueprint(bedit, url_prefix="/edit")
app.register_blueprint(butils, url_prefix="/utils")

@app.route("/")
def index():
    return render_template(f"This page not allowed to requests.")

@app.route("/check/")
def check():
    if "ip" in request.args:
        log = read_file("logs.json")
        log.append(f"{{{str(datetime.datetime.now())}}} {request.args.get('ip')} check")
        write_file("logs.json", log)

        return render_template("Checked.")
    else:
        return render_template("/check.html", True)

@app.route("/ips/")
def ips():
    ips = read_file("ips.json")

    return render_template(ips)
   

app.run(host="0.0.0.0", port=5000)