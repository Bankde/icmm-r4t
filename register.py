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
    print("Header:", request.headers["Content-Type"])
    req_data = json.dumps(request.json)
    print(request.data)
    print(request.json)

    data = {
        "hello"  : "world",
        "number" : 3,
        "result" : "OK"
    }
    resp = jsonify(data)
    return resp
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234)
