from flask import Flask, render_template, request, jsonify, json
import os

template_dir = os.path.abspath("./views")
app = Flask(__name__,  template_folder=template_dir, static_url_path="/static")
# Auto reload if a template file is changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("./static", path)

@app.route("/")
def index_get():
    return render_template("index.html")

@app.route("/confirm", methods=["POST"])
def confirm_post():
    team_name = request.form.get("teamName")
    user1 = request.form.get("user1")
    user2 = request.form.get("user2")
    user3 = request.form.get("user3")
    user4 = request.form.get("user4")
    return render_template("confirm.html", teamName=team_name, user1=user1, user2=user2, user3=user3, user4=user4)

@app.route("/result", methods=["POST"])
def result_post():
    # Force success
    team_name = request.form.get("teamName")
    if team_name :
        # For simulate success and failure
        success = True
    else:
        success = False
        
    if success:
        user1 = request.form.get("user1")
        user2 = request.form.get("user2")
        user3 = request.form.get("user3")
        user4 = request.form.get("user4")
        return render_template("result.html", success=success, teamName=team_name, user1=user1, user2=user2, user3=user3, user4=user4)
    else:
        reason = "This is reason."
        return render_template("result.html", success=success, reason=reason)

@app.route("/api/check", methods=["POST"])
def api_check_post():
    req_data = request.json
    team_name = req_data["teamName"]
    user1 = req_data["user1"]
    user2 = req_data["user2"]
    user3 = req_data["user3"]
    user4 = req_data["user4"]

    print("Team name:", team_name)
    if "fail" in team_name:
        data = {
            "success" : False,
            "teamName" : "Duplicate",
            "member1" : "Not Found",
            "member2" : "Registered",
            "member3" : "10K",
            "member4" : "NO10K"
        }
    else:
        data = {
            "success" : True,
            "teamName" : "Ok",
            "member1" : "10K",
            "member2" : "10K",
            "member3" : "NO10K",
            "member4" : "NO10K"
        }
    resp = jsonify(data)
    return resp
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234)
