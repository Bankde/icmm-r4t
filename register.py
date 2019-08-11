#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, g
import json
import os
import sqlite3
from teamspread import TeamSpread
from datetime import datetime, timezone, timedelta
from db import UserDB

DEFAULT_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


BIND_ADDRESS = os.environ.get('BIND_ADDRESS', 'localhost')
PORT = os.environ.get('PORT', 5000)
ENV_MODE = os.environ.get('ENV_MODE', 'production').lower()

GSHEET_CREDENTIAL_FILE = os.environ.get('GSHEET_CREDENTIAL_FILE', './data/credentials.json')
GSHEET_SPREADSHEET_KEY = os.environ.get('GSHEET_SPREADSHEET_KEY')
GSHEET_WORKSHEET = os.environ.get('GSHEET_WORKSHEET', 'team')

SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH', './data/users.db')

UI_TEMPLATE_TEAM_LIST_LINK = os.environ.get('UI_TEMPLATE_TEAM_LIST_LINK', 'https://www.icmm.run')
UI_TEMPLATE_BASE_URL = os.environ.get('UI_TEMPLATE_BASE_URL', None)

template_dir = os.path.abspath("./views")
app = Flask(__name__,  template_folder=template_dir, static_url_path="/static")
# Auto reload if a template file is changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

team_spread = TeamSpread(
    GSHEET_CREDENTIAL_FILE, 
    GSHEET_SPREADSHEET_KEY,
    GSHEET_WORKSHEET)

def get_db():
    """Function for get db inside Flask app.
    Must call this funtions inside app context and do not connect database before app run.
    Example:
        with app.app_context():
            db = get_db()
    """
    db = getattr(g, "_database", None)
    if db is None:
        UserDB.connect(SQLITE_DB_PATH)
        db = UserDB
    return db

@app.teardown_appcontext
def close_connection(exception):
    UserDB.close()

@app.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("./static", path)

@app.route("/")
def index_get():
    return render_template("index.html", 
        teamListLink=UI_TEMPLATE_TEAM_LIST_LINK,
        baseUrl=UI_TEMPLATE_BASE_URL)

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
        }, 
        teamListLink=UI_TEMPLATE_TEAM_LIST_LINK,
        baseUrl=UI_TEMPLATE_BASE_URL)

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
            users = UserDB.getUsersWithTeam()
            # - Upload team_data to spreadsheet
            team_dict = {}
            for user_team in users:
                firstname, lastname, team_id, first10k, team_name, timestamp = user_team
                if team_id not in team_dict:
                    # time format: '2018-11-18 02:29:13'
                    time_obj = datetime.strptime(timestamp, DEFAULT_TIME_FORMAT)
                    # Convert to BKK timezone
                    time_obj = time_obj + timedelta(hours=7)
                    team_dict[team_id] = {
                        "timestamp" : time_obj.strftime(DEFAULT_TIME_FORMAT),
                        "team_name" : team_name,
                        "members" : ["%s %s" % (firstname, lastname)]
                    }
                else:
                    team_dict[team_id]["members"].append("%s %s" % (firstname, lastname))
            # - Convert to spreadsheet format
            team_rows = []
            for idx, data in enumerate(team_dict.items()):
                # data is tuple of key and value.
                row = [idx + 1, data[1]["timestamp"], data[1]["team_name"], *data[1]["members"]]
                team_rows.append(row)
            team_spread.update_team(team_rows)

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
                }, 
                teamListLink=UI_TEMPLATE_TEAM_LIST_LINK,
                baseUrl=UI_TEMPLATE_BASE_URL)
        else:
            reason = "Something went wrong. Make sure you check the team before submitted."
            return render_template("result.html", 
                success=success, reason=reason, 
                teamListLink=UI_TEMPLATE_TEAM_LIST_LINK,
                baseUrl=UI_TEMPLATE_BASE_URL)

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
    return jsonify(data)

def load_json_config(config_path):
    config = None
    with open(config_path) as f:
        config = json.load(f)
    return config

def main():
    debug_flag = ENV_MODE != 'production'
    
    try:
        app.run(host=BIND_ADDRESS, port=PORT, debug=debug_flag)
    finally:
        # Caught an interrupt or some error.
        UserDB.close()

if __name__ == "__main__":
    main()
