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

bthemes = Blueprint("bthemes", __name__, template_folder="templates")

@bthemes.route("/<id>")
def gettheme(id):
    with open("./themes/"+id, "r", encoding="utf8") as f:
        return render_template(f.read(), type=".css")