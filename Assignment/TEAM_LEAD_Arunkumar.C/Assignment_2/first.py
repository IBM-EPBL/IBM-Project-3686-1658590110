from flask import Flask, render_template

app = Flask(__name__)
title="flask"
posts = [
    {"id": 211419104024,
     "name": "Arun",
     "age": 12,
     "degree": "B.E",
     "Dept": "CSE"
     },
    {"id": 211419104001,
     "name": "Aakash",
     "age": 19,
     "degree": "B.E",
     "Dept": "MECH"
     },
    {"id": 211419104020,
     "name": "Arun.c",
     "age": 11,
     "degree": "B.E",
     "Dept": "ECE"
     }, {
        "id": 211419104024,
        "name": "Ashritha",
        "age": 11,
        "degree": "B.E",
        "Dept": "CSE"
    },
{
        "id": 211419104024,
        "name": "Bala",
        "age": 11,
        "degree": "B.E",
        "Dept": "CSE"
    },
{
        "id": 211419104029,
        "name": "GokulNath",
        "age": 90,
        "degree": "B.E",
        "Dept": "CSE"
    }
]


@app.route('/index')
def index():
    return render_template("home.html",posts=posts,title=title)
@app.route('/')
def decorate():
    return '''
    <h1>   HELLO IBM MEMBERS </h1>
    <a href="http://127.0.0.1:5000/index">Click here</a>
    '''
@app.route('/about')
def about():
    return render_template("about.html",title=title)
if __name__ == "__main__":
    app.run(debug=True)
