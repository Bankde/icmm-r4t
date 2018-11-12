#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify
import json
import os
import sqlite3
from teamspread import TeamSpread

DEFAULT_CONFIG_PATH = "./config.json"

users_db = "users.db"

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

def setMsgData(data, index, msg):
    if index == 0:
        key = "member1"
    elif index == 1:
        key = "member2"
    elif index == 2:
        key = "member3"
    elif index == 3:
        key = "member4"
    else:
        assert(0)
    data[key] = msg
    return data

def checkTeam(teamName, user1, user2, user3, user4):
    userList = [(user1["firstname"],user1["lastname"]) , (user2["firstname"],user2["lastname"]) ,
                (user3["firstname"],user3["lastname"]) , (user4["firstname"],user4["lastname"])]

    data = {"member1": "notInit", "member2": "notInit", "member3": "notInit", "member4": "notInit"}

    conn = sqlite3.connect(users_db)
    c = conn.cursor()

    # Check teamName
    values = (teamName, )
    c.execute("""SELECT teamName FROM users WHERE teamName = ?""", values)
    all_data = c.fetchall()
    if len(all_data) != 0:
        data["teamName"] = "Team name's already existed"
    else:
        data["teamName"] = "Ok"

    userSet = set()
    userNotFirst10k = []

    for index in range(0,4):
        if userList[index][0] == "" or userList[index][1] == "":
            setMsgData(data, index, "Field cannot be empty")
            continue
        if userList[index] in userSet:
            setMsgData(data, index, "Duplicate name found")
            continue
        userSet.add(userList[index])

        values = (userList[index][0], userList[index][1], )
        c.execute("SELECT firstname, lastname, teamName, first10k FROM users WHERE (firstname = ? AND lastname = ?)", values)
        all_data = c.fetchall()

        if len(all_data) == 0:
            setMsgData(data, index, "User not found")
            continue

        if len(all_data) > 1:
            print("Error: found duplicate data in database %s %s" % (userList[index][0], userList[index][1]))
            assert(0)

        firstname = all_data[0][0]
        lastname = all_data[0][1]
        team = all_data[0][2]
        isFirst10k = all_data[0][3]

        if not(team == "" or team == None):
            setMsgData(data, index, "Already registered")
            continue

        if isFirst10k == 0:
            userNotFirst10k.append(index)

        setMsgData(data, index, "Ok")

    conn.close()

    # Not enough first10k
    if len(userNotFirst10k) > 2:
        for index in userNotFirst10k:
            setMsgData(data, index, "This user ran 10k before")

    if data["teamName"] == "Ok" and \
       data["member1"] == "Ok" and \
       data["member2"] == "Ok" and \
       data["member3"] == "Ok" and \
       data["member4"] == "Ok":
        data["success"] = True
    else:
        data["success"] = False

    return data


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
        conn = sqlite3.connect(users_db)
        c = conn.cursor()

        # Check teamName
        values = (team_name, r1_firstname, r1_lastname, r2_firstname, r2_lastname,
            r3_firstname, r3_lastname, r4_firstname, r4_lastname)
        c.execute("""UPDATE users SET teamName=? WHERE (firstname=? AND lastname=?) OR (firstname=? AND lastname=?)
            OR (firstname=? AND lastname=?) OR (firstname=? AND lastname=?)""", values)
        conn.commit()
        conn.close()

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
    
    app.run(host=server_conf["bindAddress"], port=server_conf["port"])

if __name__ == "__main__":
    main()
