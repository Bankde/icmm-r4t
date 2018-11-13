#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify
import json
import os
import sqlite3
from teamspread import TeamSpread
from db import UserDB

DEFAULT_CONFIG_PATH = "./config.json"

template_dir = os.path.abspath("./views")
app = Flask(__name__,  template_folder=template_dir, static_url_path="/static")
# Auto reload if a template file is changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

team_spread = None

@app.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("./static", path)

@app.route("/")
def index_get():
    return render_template("index.html")

@app.route("/confirm", methods=["POST"])
def confirm_post():
    team_name = request.form.get("teamName")
    r1_firstname = request.form.get("r1FirstName")
    r1_lastname = request.form.get("r1LastName")
    r2_firstname = request.form.get("r2FirstName")
    r2_lastname = request.form.get("r2LastName")
    r3_firstname = request.form.get("r3FirstName")
    r3_lastname = request.form.get("r3LastName")
    r4_firstname = request.form.get("r4FirstName")
    r4_lastname = request.form.get("r4LastName")

    return render_template("confirm.html",
        teamName=team_name,
        user1={
            "firstname" : r1_firstname,
            "lastname" : r1_lastname,
        },
        user2={
            "firstname" : r2_firstname,
            "lastname" : r2_lastname,
        },
        user3={
            "firstname" : r3_firstname,
            "lastname" : r3_lastname,
        },
        user4={
            "firstname" : r4_firstname,
            "lastname" : r4_lastname,
        })

@app.route("/result", methods=["POST"])
def result_post():
    team_name = request.form.get("teamName")
    r1_firstname = request.form.get("r1FirstName")
    r1_lastname = request.form.get("r1LastName")
    r2_firstname = request.form.get("r2FirstName")
    r2_lastname = request.form.get("r2LastName")
    r3_firstname = request.form.get("r3FirstName")
    r3_lastname = request.form.get("r3LastName")
    r4_firstname = request.form.get("r4FirstName")
    r4_lastname = request.form.get("r4LastName")

    user1={"firstname" : r1_firstname, "lastname" : r1_lastname}
    user2={"firstname" : r2_firstname, "lastname" : r2_lastname}
    user3={"firstname" : r3_firstname, "lastname" : r3_lastname}
    user4={"firstname" : r4_firstname, "lastname" : r4_lastname}
    data = checkTeam(team_name, user1, user2, user3, user4)
    success = data["success"]

    if success:
        # Update teamName
        UserDB.updateTeamByUser(team_name, r1_firstname, r1_lastname)
        UserDB.updateTeamByUser(team_name, r2_firstname, r2_lastname)
        UserDB.updateTeamByUser(team_name, r3_firstname, r3_lastname)
        UserDB.updateTeamByUser(team_name, r4_firstname, r4_lastname)

        # TODO: 
        # - Read and prepare team_data
        # - Upload team_data to spreadsheet
        # team_spread.update_team(team_data)

        return render_template("result.html",
            success=success,
            teamName=team_name,
            user1={
                "firstname" : r1_firstname,
                "lastname" : r1_lastname,
            },
            user2={
                "firstname" : r2_firstname,
                "lastname" : r2_lastname,
            },
            user3={
                "firstname" : r3_firstname,
                "lastname" : r3_lastname,
            },
            user4={
                "firstname" : r4_firstname,
                "lastname" : r4_lastname,
            })
    else:
        reason = "Something went wrong. Make sure you check the team before submitted."
        return render_template("result.html", success=success, reason=reason)

@app.route("/api/check", methods=["POST"])
def api_check_post():
    req_data = request.json
    team_name = req_data["teamName"]
    user1 = req_data["user1"]
    user2 = req_data["user2"]
    user3 = req_data["user3"]
    user4 = req_data["user4"]

    data = checkTeam(team_name, user1, user2, user3, user4)
    resp = jsonify(data)
    return resp

def load_json_config(config_path):
    config = None
    with open(config_path) as f:
        config = json.load(f)
    return config

def main():
    global team_spread
    config = load_json_config(DEFAULT_CONFIG_PATH)
    server_conf = config["server"]
    spread_conf = config["spreadsheet"]

    team_spread = TeamSpread(
        spread_conf["credentials"], 
        spread_conf["spreadsheetKey"],
        spread_conf["worksheet"])

    UserDB.connect(config["db"]["path"])
    try:
        app.run(host=server_conf["bindAddress"], port=server_conf["port"])
    finally:
        # Caught an interrupt or some error.
        UserDB.close()

if __name__ == "__main__":
    main()
