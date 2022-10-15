import wtforms
from flask import Flask, render_template, request

pap = Flask(__name__)
@pap.route("/",methods=["GET", "POST"])
def home():
    if request.method == "POST":
        posts=request.form
        return render_template("About1.html",posts=posts,title="IBM project")
    return render_template("Home1.html")

if __name__ == "__main__":
    pap.run(debug=True)
