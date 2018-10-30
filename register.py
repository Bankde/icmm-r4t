from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index_get():
    return render_template("index.html")

@app.route("/confirm", methods=["POST"])
def index_post():
	user1 = request.form.get('user1')
	user2 = request.form.get('user2')
	user3 = request.form.get('user3')
	user4 = request.form.get('user4')
    return render_template("confirm.html", user1=user1, user2=user2, user3=user3, user4=user4)

@app.route("/success", methods=["POST"])
def index_post():
    return render_template("success.html", user1=user1, user2=user2, user3=user3, user4=user4)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1234)
