from flask import Flask, render_template, request, session
import ibm_db
import os

import mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=xst23649;PWD=bKigkwntEUnt56mj",'','')

app = Flask(__name__)
app.secret_key = "arun"
@app.route("/")
def home():
    return render_template("login.html")

@app.route('/login',methods = ['POST', 'GET'])
def login():
  if request.method == 'POST':

    email = request.form['email']
    password = request.form['password']
    sql ="SELECT * FROM registration WHERE email=? and password=?";
    stmt =ibm_db.prepare(conn,sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      session['response']= account['EMAIL']
      session['amount']=account['INTIAL_AMOUNT']
      session['name'] = account['NAME']
      return render_template('dashboard.html',account = session['response'])
    else:
        return render_template('login.html',msg="Incorrect Email and Password")
  return render_template('login.html')
@app.route('/registration')
def registration():
  return render_template('registration.html')
@app.route('/logging')
def logging():
  return render_template('login.html')
def registration():
  return render_template('registration.html')
@app.route('/register',methods = ['POST', 'GET'])
def register():
  if request.method=='POST':
    name = request.form['name']
    dob = request.form['dob']
    occupation = request.form['occupation']
    gender = request.form['gender']
    email = request.form['email']
    password = request.form['password']
    intial_amount = request.form['intial_amount']
    address = request.form['address']
    phone = request.form['number']
    sql = "SELECT * FROM registration WHERE email=?";
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      return render_template('login.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO registration(name,dob,occupation,gender,email,password,intial_amount,address,phone_number) VALUES (?,?,?,?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, dob)
      ibm_db.bind_param(prep_stmt, 3, occupation)
      ibm_db.bind_param(prep_stmt, 4, gender)
      ibm_db.bind_param(prep_stmt, 5, email)
      ibm_db.bind_param(prep_stmt, 6, password)
      ibm_db.bind_param(prep_stmt, 7, intial_amount)
      ibm_db.bind_param(prep_stmt,8,address)
      ibm_db.bind_param(prep_stmt,9,phone)
      ibm_db.execute(prep_stmt)
      insert_sql = "INSERT INTO expenses VALUES (?,0,0,0,0,0,0,0,0,?)"
      prep_stmt = ibm_db.prepare(conn,insert_sql)
      ibm_db.bind_param(prep_stmt,1,email)
      ibm_db.bind_param(prep_stmt, 2, intial_amount)
      ibm_db.execute(prep_stmt)
      insert_sql = "UPDATE expenses set balance=? WHERE email=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, intial_amount)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.execute(prep_stmt)
      return render_template('login.html',msg1="registered successfully",color="green")
@app.route('/profile')
def profile():
  sql = "SELECT * FROM registration WHERE email=?";
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt, 1, session['response'])
  ibm_db.execute(stmt)
  account = ibm_db.fetch_assoc(stmt)
  name = account['NAME']
  dob = account['DOB']
  occupation =account['OCCUPATION']
  gender = account['GENDER']
  email = account['EMAIL']
  password = account['PASSWORD']
  intial =account['INTIAL_AMOUNT']
  address = account['ADDRESS']
  phone =account['PHONE_NUMBER']
  return render_template('profile.html',name=name,dob=dob,occupation=occupation,gender=gender,email=email,password = password,intial=intial,address=address,phone=phone)
@app.route('/expenses')
def expenses():
  sql = "SELECT * FROM expenses WHERE email=?";
  stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(stmt, 1, session['response'])
  ibm_db.execute(stmt)
  account = ibm_db.fetch_assoc(stmt)
  medical = account['MEDICAL']
  education = account['EDUCATION']
  rent = account['RENT']
  food = account['FOOD']
  travel = account['TRAVEL']
  others = account['OTHERS']
  spend =account['TOTAL']
  balance = account['BALANCE']
  credit = account['CREDIT']
  return render_template('expenses.html',medical=medical,education=education,rent=rent,travel=travel,others=others,food=food,spend=spend,balance=balance,credit = credit)
@app.route('/expenditure',methods = ['POST','GET'])
def expenditure():
  def send_email(email,amount):
    from_email = Email('m.arunkumarmar12@gmail.com')
    to_email = To(email)
    subject = 'Personal expense tracker'
    content = Content("text/plain", f"your balance is {balance}".format(balance=amount))
    mail = Mail(from_email, to_email, subject, content)

    try:
      sg = SendGridAPIClient('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')
      response = sg.send(mail)
      print(response.status_code)
      print(response.body)
      print(response.headers)
    except Exception as e:
      print(e)
  def check_balance(amount):
      send_email(session['response'],amount)
  if request.method =='POST':
    amount = request.form['amount']
    type = request.form['type']
    sql = "SELECT * FROM expenses WHERE email=?";
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, session['response'])
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    total = int(account['MEDICAL'])+int(account['EDUCATION'])+int(account['RENT'])+int(account['TRAVEL'])+int(account['OTHERS'])+int(account['FOOD'])
    if type=="medical":
      balance = int(account['BALANCE']) - int(amount)
      amount =int (account['MEDICAL']) +int(amount)
      total = amount + int(account['EDUCATION']) +int(account['RENT']) +int(account['TRAVEL']) +int(account['OTHERS']) + \
              int(account['FOOD'])
      insert_sql = "UPDATE expenses SET medical=?,total=?,balance =? WHERE email=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt,1,amount)
      ibm_db.bind_param(prep_stmt,2,total)
      ibm_db.bind_param(prep_stmt,3,balance)
      ibm_db.bind_param(prep_stmt, 4, session['response'])
      ibm_db.execute(prep_stmt)
      sql = "SELECT * FROM expenses WHERE email=?";
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt, 1, session['response'])
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      medical = account['MEDICAL']
      education = account['EDUCATION']
      rent = account['RENT']
      food = account['FOOD']
      travel = account['TRAVEL']
      others = account['OTHERS']
      spend = account['TOTAL']
      balance = account['BALANCE']
      credit = account['CREDIT']
      check_balance(int(balance))
      return render_template('expenses.html', medical=medical, education=education, rent=rent, travel=travel,
                             others=others, food=food, spend=spend, balance=balance, credit=credit,msg="Updated successfully!")
    if type=="education":
      balance = int(account['BALANCE']) - int(amount)
      amount =int (account['EDUCATION'])  +int(amount)
      balance = int(account['BALANCE']) - amount
      total = amount +int(account['MEDICAL']) + int(account['RENT']) +int(account['TRAVEL']) +int(account['OTHERS']) + \
              int(account['FOOD'])
      insert_sql = "UPDATE expenses SET education=?,total=?,balance =? WHERE email=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt,1,amount)
      ibm_db.bind_param(prep_stmt,2,total)
      ibm_db.bind_param(prep_stmt, 3, balance)
      ibm_db.bind_param(prep_stmt, 4, session['response'])
      ibm_db.execute(prep_stmt)
      sql = "SELECT * FROM expenses WHERE email=?";
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt, 1, session['response'])
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      medical = account['MEDICAL']
      education = account['EDUCATION']
      rent = account['RENT']
      food = account['FOOD']
      travel = account['TRAVEL']
      others = account['OTHERS']
      spend = account['TOTAL']
      balance = account['BALANCE']
      credit = account['CREDIT']
      check_balance(int(balance))
      return render_template('expenses.html', medical=medical, education=education, rent=rent, travel=travel,
                             others=others, food=food, spend=spend, balance=balance, credit=credit,msg="Updated successfully!")
    if type=="rent":
      balance = int(account['BALANCE']) - int(amount)
      amount =int (account['RENT'])  +int(amount)
      total = amount + int(account['EDUCATION']) + int(account['MEDICAL']) + int(account['TRAVEL']) + int(account['OTHERS'] )+ \
              int(account['FOOD'])
      insert_sql = "UPDATE expenses SET rent=?,total=?,balance =? WHERE email=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt,1,amount)
      ibm_db.bind_param(prep_stmt,2,total)
      ibm_db.bind_param(prep_stmt, 3, balance)
      ibm_db.bind_param(prep_stmt, 4, session['response'])
      ibm_db.execute(prep_stmt)
      sql = "SELECT * FROM expenses WHERE email=?";
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt, 1, session['response'])
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      medical = account['MEDICAL']
      education = account['EDUCATION']
      rent = account['RENT']
      food = account['FOOD']
      travel = account['TRAVEL']
      others = account['OTHERS']
      spend = account['TOTAL']
      balance = account['BALANCE']
      credit = account['CREDIT']
      check_balance(int(balance))
      return render_template('expenses.html', medical=medical, education=education, rent=rent, travel=travel,
                             others=others, food=food, spend=spend, balance=balance, credit=credit,msg="Updated successfully!")
    if type=="travel":
      balance = int(account['BALANCE']) -int(amount)
      amount =int (account['TRAVEL'])+int(amount)
      total = amount + int(account['EDUCATION']) + int(account['RENT']) +int(account['MEDICAL']) +int(account['OTHERS']) + \
              int(account['FOOD'])
      insert_sql = "UPDATE expenses SET travel=?,total=?,balance =? WHERE email=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt,1,amount)
      ibm_db.bind_param(prep_stmt,2,total)
      ibm_db.bind_param(prep_stmt, 3, balance)
      ibm_db.bind_param(prep_stmt, 4, session['response'])
      ibm_db.execute(prep_stmt)
      sql = "SELECT * FROM expenses WHERE email=?";
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt, 1, session['response'])
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      medical = account['MEDICAL']
      education = account['EDUCATION']
      rent = account['RENT']
      food = account['FOOD']
      travel = account['TRAVEL']
      others = account['OTHERS']
      spend = account['TOTAL']
      balance = account['BALANCE']
      credit = account['CREDIT']
      check_balance(int(balance))
      return render_template('expenses.html', medical=medical, education=education, rent=rent, travel=travel,
                             others=others, food=food, spend=spend, balance=balance, credit=credit,msg="Updated successfully!")
    if type=="food":
      balance = int(account['BALANCE']) -int(amount)
      amount =int (account['FOOD'])+int(amount)
      total = amount + int(account['EDUCATION']) + int(account['RENT']) +int(account['TRAVEL']) + int(account['OTHERS']) + \
              int(account['MEDICAL'])
      insert_sql = "UPDATE expenses SET food=?,total=?,balance =? WHERE email=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt,1,amount)
      ibm_db.bind_param(prep_stmt,2,total)
      ibm_db.bind_param(prep_stmt, 3, balance)
      ibm_db.bind_param(prep_stmt, 4, session['response'])
      ibm_db.execute(prep_stmt)
      sql = "SELECT * FROM expenses WHERE email=?";
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt, 1, session['response'])
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      medical = account['MEDICAL']
      education = account['EDUCATION']
      rent = account['RENT']
      food = account['FOOD']
      travel = account['TRAVEL']
      others = account['OTHERS']
      spend = account['TOTAL']
      balance = account['BALANCE']
      credit = account['CREDIT']
      check_balance(int(balance))
      return render_template('expenses.html', medical=medical, education=education, rent=rent, travel=travel,
                             others=others, food=food, spend=spend, balance=balance, credit=credit,msg="Updated successfully!")
    if type=="others":
      balance = int(account['BALANCE']) -int(amount)
      amount =int (account['OTHERS']) +int(amount)
      total = amount + int(account['EDUCATION']) + int(account['RENT']) +int( account['TRAVEL']) +int(account['MEDICAL']) + \
              int(account['FOOD'])
      insert_sql = "UPDATE expenses SET others=?,total=?,balance =? WHERE email=?"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt,1,amount)
      ibm_db.bind_param(prep_stmt,2,total)
      ibm_db.bind_param(prep_stmt, 3, balance)
      ibm_db.bind_param(prep_stmt, 4, session['response'])
      ibm_db.execute(prep_stmt)
      sql = "SELECT * FROM expenses WHERE email=?";
      stmt = ibm_db.prepare(conn, sql)
      ibm_db.bind_param(stmt, 1, session['response'])
      ibm_db.execute(stmt)
      account = ibm_db.fetch_assoc(stmt)
      medical = account['MEDICAL']
      education = account['EDUCATION']
      rent = account['RENT']
      food = account['FOOD']
      travel = account['TRAVEL']
      others = account['OTHERS']
      spend = account['TOTAL']
      balance = account['BALANCE']
      credit = account['CREDIT']
      check_balance(int(balance))
      return render_template('expenses.html', medical=medical, education=education, rent=rent, travel=travel,
                             others=others, food=food, spend=spend, balance=balance, credit=credit,msg="Updated successfully!")
  return render_template('expenses.html')
@app.route('/display')
def display():
  sql ="SELECT * FROM expenses WHERE email=?"
  prep_stmt = ibm_db.prepare(conn,sql)
  ibm_db.bind_param(prep_stmt,1,session['response'])
  ibm_db.execute(prep_stmt)
  account = ibm_db.fetch_assoc(prep_stmt)
  print(account)
  medical = int(int(account['MEDICAL']) / int(account['CREDIT']) * 100)
  education = int(int(account['EDUCATION']) / int(account['CREDIT']) * 100)
  rent = int(int(account['RENT']) / int(account['CREDIT']) * 100)
  travel = int(int(account['TRAVEL']) / int(account['CREDIT']) * 100)
  food = int(int(account['FOOD']) / int(account['CREDIT']) * 100)
  others = int(int(account['OTHERS']) / int(account['CREDIT']) * 100)
  spend = int(int(account['TOTAL']) / int(account['CREDIT']) * 100)
  balance = int(int(account['BALANCE']) / int(account['CREDIT']) * 100)
  print(medical,education,rent,travel,food,others,spend,balance)
  def color(var):
    if(var>70):
      return "red"
    elif(var>30):
      return "yellow"
    else:
      return "green"
  def fake(var):
    if(var>70):
      return "green"
    elif(var>30):
      return "yellow"
    else:
      return "red"
  medical_color = color(medical)
  education_color=color(education)
  rent_color=color(rent)
  travel_color = color(travel)
  food_color =color(food)
  others_color=color(others)
  spend_color=color(spend)
  balance_color = fake(balance)
  return render_template("display.html",medical_color =medical_color ,education_color=education_color,rent_color=rent_color,travel_color =travel_color ,food_color =food_color,others_color=others_color,spend_color=spend_color,balance_color =balance_color,account =account,medical=medical,education=education,rent=rent,travel=travel,others=others,food=food,spend=spend,balance=balance)
@app.route('/addBalance')
def addBalance():
  sql = "SELECT * FROM expenses WHERE email=?"
  prep_stmt = ibm_db.prepare(conn, sql)
  ibm_db.bind_param(prep_stmt, 1, session['response'])
  ibm_db.execute(prep_stmt)
  account = ibm_db.fetch_assoc(prep_stmt)
  return render_template('addBalance.html',balance=account['BALANCE'],total=account['TOTAL'],credit=account['CREDIT'])
@app.route('/adder',methods = ['POST','GET'])
def adder():
  if request.method=="POST":
    balance1 = request.form['money']
    sql = "SELECT * FROM expenses WHERE email =?";
    prep_stmt = ibm_db.prepare(conn,sql)
    ibm_db.bind_param(prep_stmt,1,session['response'])
    ibm_db.execute(prep_stmt)
    account = ibm_db.fetch_assoc(prep_stmt)
    balance = int(balance1) +int(account['BALANCE'])
    credit=int(balance1)+int(account['CREDIT'])
    insert_sql = "UPDATE expenses SET balance =?,credit=? WHERE email=?"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, balance)
    ibm_db.bind_param(prep_stmt, 2, credit)
    ibm_db.bind_param(prep_stmt,3,session['response'])
    ibm_db.execute(prep_stmt)
    return render_template("thanks.html",msg="Balance added successfully")
@app.route('/dashboard')
def dashboard():
  return render_template('dashboard.html')
if __name__=="__main__":
    app.run(debug=True)