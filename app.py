import os
from flask import Flask,request,jsonify,g,redirect,url_for,render_template,flash,session
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="8344",
    database="employee",
)

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "Lokesh"
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

@app.route('/',methods=['GET','POST'])
def view():
    db = mydb.cursor()
    if request.args.get('orderby'):
        orderby = request.args.get('orderby')
        db.execute('SELECT * from employee order by '+orderby+' desc;')
    else:
        db.execute('SELECT * from employee;')
    myresult = db.fetchall()
    return jsonify(entries=myresult)

if __name__=='__main__':
 app.run(debug=True)
