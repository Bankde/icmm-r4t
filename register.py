#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, g
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
config = None

def get_db():
    """Function for get db inside Flask app.
    Must call this funtions inside app context and do not connect database before app run.
    Example:
        with app.app_context():
            db = get_db()
    """
    db = getattr(g, '_database', None)
    if db is None:
        UserDB.connect(config["db"]["path"])
        db = UserDB
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("./static", path)

@app.route("/")
def index_get():
    return render_template("index.html")

@app.route("/confirm", methods=["POST"])
def confirm_post():
    team_name = request.form.get("teamName").strip()
    r1_firstname = request.form.get("r1FirstName").strip()
    r1_lastname = request.form.get("r1LastName").strip()
    r2_firstname = request.form.get("r2FirstName").strip()
    r2_lastname = request.form.get("r2LastName").strip()
    r3_firstname = request.form.get("r3FirstName").strip()
    r3_lastname = request.form.get("r3LastName").strip()
    r4_firstname = request.form.get("r4FirstName").strip()
    r4_lastname = request.form.get("r4LastName").strip()

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
    team_name = request.form.get("teamName").strip()
    r1_firstname = request.form.get("r1FirstName").strip()
    r1_lastname = request.form.get("r1LastName").strip()
    r2_firstname = request.form.get("r2FirstName").strip()
    r2_lastname = request.form.get("r2LastName").strip()
    r3_firstname = request.form.get("r3FirstName").strip()
    r3_lastname = request.form.get("r3LastName").strip()
    r4_firstname = request.form.get("r4FirstName").strip()
    r4_lastname = request.form.get("r4LastName").strip()

    user1={"firstname" : r1_firstname, "lastname" : r1_lastname}
    user2={"firstname" : r2_firstname, "lastname" : r2_lastname}
    user3={"firstname" : r3_firstname, "lastname" : r3_lastname}
    user4={"firstname" : r4_firstname, "lastname" : r4_lastname}
    with app.app_context():
        db = get_db()
        data = db.checkTeam(team_name, user1, user2, user3, user4)
        success = data["success"]

        if success:
            # Insert new team
            UserDB.insertTeam(team_name)
            team = UserDB.getTeamByTeamName(team_name)
            team_id = team[0]
            # Update teamId at 
            UserDB.updateTeamByUser(team_id, r1_firstname, r1_lastname)
            UserDB.updateTeamByUser(team_id, r2_firstname, r2_lastname)
            UserDB.updateTeamByUser(team_id, r3_firstname, r3_lastname)
            UserDB.updateTeamByUser(team_id, r4_firstname, r4_lastname)

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
    user1["firstname"] = user1["firstname"].strip()
    user1["lastname"] = user1["lastname"].strip()
    user2 = req_data["user2"]
    user2["firstname"] = user2["firstname"].strip()
    user2["lastname"] = user2["lastname"].strip()
    user3 = req_data["user3"]
    user3["firstname"] = user3["firstname"].strip()
    user3["lastname"] = user3["lastname"].strip()
    user4 = req_data["user4"]
    user4["firstname"] = user4["firstname"].strip()
    user4["lastname"] = user4["lastname"].strip()

    with app.app_context():
        db = get_db()
        data = db.checkTeam(team_name, user1, user2, user3, user4)
    resp = jsonify(data)
    return resp

def load_json_config(config_path):
    config = None
    with open(config_path) as f:
        config = json.load(f)
    return config

def main():
    global team_spread, config
    config = load_json_config(DEFAULT_CONFIG_PATH)
    server_conf = config["server"]
    spread_conf = config["spreadsheet"]

    team_spread = TeamSpread(
        spread_conf["credentials"], 
        spread_conf["spreadsheetKey"],
        spread_conf["worksheet"])

    debug_flag = False
    if "debug" in config["server"]:
        debug_flag = config["server"]["debug"]
    
    try:
        app.run(host=server_conf["bindAddress"], port=server_conf["port"], debug=debug_flag)
    finally:
        # Caught an interrupt or some error.
        UserDB.close()

if __name__ == "__main__":
    main()
