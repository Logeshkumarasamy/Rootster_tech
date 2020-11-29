import os
from flask import Flask,request,g,redirect,url_for,render_template,flash,session
import mysql.connector
from flask import jsonify
from datetime import datetime
from decimal import Decimal
import json


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="8344",
    database="employee",
)
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "Logesh"
app.config.from_envvar('FLASKR_SETTINGS',silent=True)

@app.route('/addEmp',methods=['GET','POST'])
def addEmp():
  if request.method=='POST':
    if request.form['action']=="add":
      mycursor = mydb.cursor()
      sql="insert into employee(Name,Address,Gender,JoinDate) values(%s, %s, %s, %s)"
      val=(request.form['name'],request.form['Address'],request.form['gender'],request.form['joindate'])
      mycursor.execute(sql,val)
      mydb.commit()
      flash(' Details added')
      return redirect(url_for('view'))
  return render_template('add.html')

@app.route('/editemp',methods=['GET','POST'])
def editemp():
  if request.method=='POST':
    if request.form['action']=="edit":
      mycursor = mydb.cursor()
      sql="update employee set Name='"+request.form['name']+"',Address='"+request.form['Address']+"',Gender='"+request.form['gender']+"',JoinDate='"+request.form['joindate']+"' where Id="+request.form['ID']
      mycursor.execute(sql)
      mydb.commit()
      flash(' Details updated')
      return redirect(url_for('view'))
  return render_template('dashboard.html')

@app.route('/addsalary',methods=['GET','POST'])
def addsalary():
    if request.method == 'POST':
        if request.form['action'] == "add":
            mycursor = mydb.cursor()
            sql = "insert into salary(employeeId,month,Salary) values(%s, %s, %s )"
            val = (request.form['EmployeeId'], request.form['month'], request.form['salary'])
            mycursor.execute(sql, val)
            mydb.commit()
            flash(' Details updated')
            return redirect(url_for('viewsalary')+'?Eid='+request.form['EmployeeId'])
    return render_template('salary.html')

@app.route('/Editsalary',methods=['GET','POST'])
def Editsalary():
    if request.method == 'POST':
        if request.form['action'] == "edit":
            mycursor = mydb.cursor()
            sql1 = "update salary set month='" + request.form['month'] + "',Salary='" + request.form['salary'] + "' where Id="+request.form['ID']
            mycursor.execute(sql1)
            mydb.commit()
            flash(' Details updated')
            return redirect(url_for('viewsalary')+'?Eid='+request.form['EmployeeId'])
    return render_template('salary.html')

@app.route('/',methods=['GET','POST'])
def view():
    db = mydb.cursor()
    if request.args.get('orderby'):
        orderby = request.args.get('orderby')
        db.execute('SELECT * from employee order by '+orderby+' desc;')
    else:
        db.execute('SELECT * from employee;')
    myresult = db.fetchall()
    return render_template('dashboard.html', entries=myresult)

@app.route('/viewid',methods=['GET','POST'])
def viewid():
    db = mydb.cursor()
    cur = db.execute('SELECT * from employee where Id='+request.form['id']+';')
    myresult = db.fetchall()
    return jsonify(myresult)

@app.route('/viewsalary',methods=['GET','POST'])
def viewsalary():
    employeeid=request.args.get('Eid')
    db = mydb.cursor()
    if request.args.get('orderby'):
        orderby = request.args.get('orderby')
        sql='SELECT * from salary where employeeId="'+employeeid+'" order by '+orderby+' desc'
        db.execute(sql)
    else:
        db.execute('SELECT * from salary where employeeId="'+employeeid+'"  ;')
    myresult = db.fetchall()
    mydb.commit()
    return render_template('salary.html', entries=myresult)

@app.route('/Employees',methods=['GET','POST'])
def Employees():
    db = mydb.cursor()
    if(request.args.get('Eid')):
        employeeid=request.args.get('Eid')
        orderby = request.args.get('orderby')
        sql='SELECT e.Id,e.name,min(s.salary),max(s.salary),SUM(s.salary),AVG(s.salary) , SYSDATE(), e.JoinDate, DATEDIFF( SYSDATE(), e.JoinDate )/365 FROM employee e JOIN salary s on s.employeeId=e.Id WHERE e.Id='+employeeid
    else:
        sql="SELECT e.Id,e.name,min(s.salary),max(s.salary),SUM(s.salary),AVG(s.salary) , SYSDATE(), e.JoinDate, DATEDIFF( SYSDATE(), e.JoinDate )/365 FROM employee e JOIN salary s on s.employeeId=e.Id GROUP by e.Id"
    db.execute(sql)
    myresult = db.fetchall()
    sql="select * from employee;"
    db.execute(sql)
    my = db.fetchall()
    mydb.commit()
    return render_template('Employees.html', entries=myresult,my=my)

@app.route('/report2',methods=['GET','POST'])
def report2():
    db = mydb.cursor()
    if(request.args.get('Eid')):
        employeeid=request.args.get('Eid')
        orderby = request.args.get('orderby')
        sql='SELECT e.Id,e.name,min(s.salary),max(s.salary),SUM(s.salary),AVG(s.salary) , SYSDATE(), e.JoinDate, DATEDIFF( SYSDATE(), e.JoinDate )/365 FROM employee e JOIN salary s on s.employeeId=e.Id WHERE e.Id='+employeeid
    else:
        sql="SELECT e.Id,e.name,min(s.salary),max(s.salary),SUM(s.salary),AVG(s.salary) , SYSDATE(), e.JoinDate, DATEDIFF( SYSDATE(), e.JoinDate )/365 FROM employee e JOIN salary s on s.employeeId=e.Id GROUP by e.Id"
    db.execute(sql)
    myresult = db.fetchall()
    test=[]
    for row in myresult:
        ch=0
        testlist = []
        for val in row:
            ch+=1
            if ch==5:
                testlist.append(int(val))
            elif ch==6:
                testlist.append(int(val))
            elif ch==9:
                testlist.append(int(val))
            else:
                testlist.append(val)
        test.append(testlist)
    sql="select * from employee;"
    db.execute(sql)
    my = db.fetchall()
    mydb.commit()
    return jsonify(salary=test,employee=my)

@app.route('/employeefliter',methods=['GET','POST'])
def employeefliter():
    db = mydb.cursor()
    today = datetime.today()
    dt=str(today.strftime("%Y"))+"-"+str(today.strftime("%m"))
    start=dt
    end=dt
    if request.method == 'POST':
        if request.form['action'] == "fliter":
            start=request.form['startmonth']
            end=request.form['endmonth']
            employeeid=request.args.get('Eid')
            orderby = request.args.get('orderby')
            sql='SELECT Id,month,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` WHERE month<="'+ end +'" and month >="'+ start +'" GROUP by month'
            db.execute(sql)
            myresult = db.fetchall()
            sql = "SELECT Id,employeeId,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` WHERE month<='"+end +"' and month >='"+start +"' GROUP by employeeId"
            db.execute(sql)
            my = db.fetchall()
    else:
        sql='SELECT Id,month,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` GROUP by month'
        db.execute(sql)
        myresult = db.fetchall()
        sql = "SELECT Id,employeeId,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` GROUP by employeeId"
        db.execute(sql)
        my = db.fetchall()
    mydb.commit()
    return render_template('employeefliter.html', entries=myresult,my=my,end=end,start=start)

@app.route('/report1',methods=['GET','POST'])
def report1():
    db = mydb.cursor()
    today = datetime.today()
    dt=str(today.strftime("%Y"))+"-"+str(today.strftime("%m"))
    start=dt
    end=dt
    if request.method == 'POST':
        if request.form['action'] == "fliter":
            start=request.form['startmonth']
            end=request.form['endmonth']
            employeeid=request.args.get('Eid')
            orderby = request.args.get('orderby')
            sql='SELECT Id,month,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` WHERE month<="'+ end +'" and month >="'+ start +'" GROUP by month'
            db.execute(sql)
            myresult = db.fetchall()
            sql = "SELECT Id,employeeId,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` WHERE month<='"+end +"' and month >='"+start +"' GROUP by employeeId"
            db.execute(sql)
            my = db.fetchall()
    else:
        sql='SELECT Id,month,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` GROUP by month'
        db.execute(sql)
        myresult = db.fetchall()
        sql = "SELECT Id,employeeId,sum(salary),MIN(salary),max(salary),AVG(salary) FROM `salary` GROUP by employeeId"
        db.execute(sql)
        my = db.fetchall()
    mydb.commit()
    return render_template('employeefliter.html', entries=myresult,my=my,end=end,start=start)

@app.route('/viewidsalary',methods=['GET','POST'])
def viewidsalary():
    db = mydb.cursor()
    cur = db.execute('SELECT * from salary where Id='+request.form['id']+';')
    myresult = db.fetchall()
    return jsonify(myresult)

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=='POST':
        db=mydb.cursor()
        cur=db.execute('delete from salary where employeeId = '+ (request.form['Id']) )
        cur=db.execute('delete from employee where id = '+ (request.form['Id']) )
        mydb.commit()
        flash('Sucessfully Deleted')
    return jsonify("Sucessfully Deleted")

@app.route('/deletesalary',methods=['GET','POST'])
def deletesalary():
    if request.method=='POST':
        db=mydb.cursor()
        cur=db.execute('delete from salary where Id = '+ (request.form['Id']) )
        mydb.commit()
        flash('Sucessfully Deleted')
    return jsonify("Sucessfully Deleted")

if __name__=='__main__':
 app.run(debug=True)
