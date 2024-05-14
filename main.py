import string
import random

from flask import Flask, request, render_template, redirect, session #type: ignore
from flask_mail import Mail, Message # type: ignore
import mysql.connector # type: ignore


app = Flask(__name__)
app.config.update(
     MAIL_SERVER='smtp.gmail.com',
     MAIL_PORT=465,
     MAIL_USE_SSL=True,
     MAIL_USERNAME='ayush.knowledge@gmail.com',
     MAIL_PASSWORD='tezfcrvpaaubxwxb'
 )
app.secret_key='ghjhjhq/213763fbf'
mail = Mail(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/signup')
def hello_world1():
    return render_template('signup.html')

@app.route('/signup1',methods=['POST'])
def signup1():
    email=request.form.get('email')
    psw=request.form.get('psw')
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
    cur = connection.cursor()
    query1="select * from user where email='{}'".format(email)
    cur.execute(query1)
    data=cur.fetchone()
    if(data==None):
        query2="insert into user(email,password) values('{}','{}')".format(email,psw)
        cur.execute(query2)
        connection.commit()
    else:
        return render_template('existAccount.html')
    return render_template('successRegister.html')

@app.route('/teachersignin01')
def teachersignin01():
    return render_template('teachersignin.html')

@app.route('/teachersignup')
def teacherhello_world1():
    return render_template('teacherSignup.html')

@app.route('/teachersignup1',methods=['POST'])
def teachersignup1():
    email=request.form.get('email')
    psw=request.form.get('psw')
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
    cur = connection.cursor()
    query1="select * from teacher where email='{}'".format(email)
    cur.execute(query1)
    data=cur.fetchone()
    if(data==None):
        query2="insert into teacher(email,password) values('{}','{}')".format(email,psw)
        cur.execute(query2)
        connection.commit()
        session['registered'] = True
    else:
        return render_template('existAccount.html')
    return render_template('teacherSuccessRegistration.html')

@app.route('/teachersignin0', methods=['POST'])
def teachersignin0():
    email = request.form.get('email')
    psw = request.form.get('psw')
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
    cur = connection.cursor()
    query1 = "select * from teacher where email='{}'".format(email)
    cur.execute(query1)
    data = cur.fetchone()
    if 'registered' in session:  # Check if the user just signed up
        session.pop('registered')  # Remove the 'registered' session variable
        session['email'] = email
        session['userid'] = data[0]
        return render_template('course_offerings.html', email=email)
    # print(data)
    elif data ==None:
        return render_template('notRegister.html')
    else:
        if psw == data[0]:
            session['email'] = email
            session['userid'] = data[2]
            connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
            cur = connection.cursor()
            query2 = "SELECT * FROM courses GROUP BY email"
            cur.execute(query2)
            data1 = cur.fetchall()
            print(data1)
            return render_template('teacherHome.html', data1=data1)
        else:
            return render_template('wrongPassword.html')

@app.route('/signin01')
def signin01():
    return render_template('signin.html')


@app.route('/signin0')
def hello1():
    return render_template('course_offerings.html')

@app.route('/signin0', methods=['POST'])
def signin0():
    email = request.form.get('email')
    psw = request.form.get('psw')
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
    cur = connection.cursor()
    query1 = "select * from user where email='{}'".format(email)
    cur.execute(query1)
    data = cur.fetchone()
    print(data)
    if data ==None:
        return render_template('notRegister.html')
    else:
        if psw == data[1]:
            session['email'] = email
            session['userid'] = data[2]
            return render_template('course_offerings.html', email=email)
        else:
            return render_template('wrongPassword.html')

@app.route('/UserHome')
def userhome():
    return render_template('userHome.html')

@app.route('/askemail')
def askemail():
    return render_template('askemail.html')


@app.route('/forgetpassword')
def forgetpassword():
    email = request.args.get('email')
    randomnumber = ''
    letter = string.digits
    for i in range(6):
        randomnumber = randomnumber + ''.join(random.choice(letter))
    print(randomnumber)
    body = 'Your forget password OTP is ' + randomnumber
    msg = Message(subject='Forget Password Email ', sender='ayush.knowledge@gmail.com',recipients=[email], body=body)
    msg.cc = [email]
    mail.send(msg)
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234",port='3306')
    cur = connection.cursor()
    query2 = "select * from user where email='{}'".format(email)
    cur.execute(query2)
    data = cur.fetchone()
    if data == None:
        return render_template('notRegister.html')
    query1 = "update user set otp ='{}' where email= '{}'".format(randomnumber, email)
    cur.execute(query1)
    connection.commit()
    return render_template('updatepassword.html', email=email)

@app.route('/updatepassword')
def updatepassword():
    email = request.args.get('email')
    otp = request.args.get('otp')
    pwd = request.args.get('pwd')
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
    cur = connection.cursor()
    query1 = "select * from user where email='{}'".format(email)
    cur.execute(query1)
    data = cur.fetchone()
    if int(data[2])==int(otp):
        query2 = "update user set password ='{}' where email= '{}'".format(pwd,email)
        cur.execute(query2)
        connection.commit()
        return render_template('passwordUpdatePage.html')
    else:
        return render_template('wrongOTP.html',email=email)

@app.route('/enroll',methods=['post'])
def enroll():
    courseid=request.form.get('courseID')
    title = request.form.get('title')
    credit = request.form.get('credit')
    email = session['email']
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
    cur = connection.cursor()
    query1="select * from courses where courseid={} and email='{}'".format(courseid,email)
    cur.execute(query1)
    data = cur.fetchone()
    if data==None:
        if 'email' in session:
            email = session['email']
            query = "insert into courses(email,courseid,title,credit,Progress) values('{}','{}','{}','{}','{}')".format(email,courseid,title,credit,0)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            return redirect('/courses')
        else:
            return redirect('/signin0')
    else:
        return render_template('alreadyEnrolled.html')

@app.route('/saveP',methods=['post'])
def saveP():

    data = request.json
    percentage = data.get('percentage')
    courseid = data.get('cid') 
    email = session['email']
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')

    if 'email' in session:
        email = session['email']
        query = "UPDATE courses SET progress = {} WHERE courseid = {} AND email = '{}'".format(percentage, courseid, email)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        return redirect('/{}'.format(courseid))
    else:
        return redirect('/signin0')

@app.route('/courses')
def myCourses():
    if 'userid' in session:
        email=session['email']
        connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234",port='3306')
        cur = connection.cursor()
        query1 = "select * from courses where email='{}'".format(email)
        cur.execute(query1)
        data=cur.fetchall()
        return render_template('userHome.html',data=data)

@app.route('/doubts')
def doubts():
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234",port='3306')
    cur = connection.cursor()
    query1 = "select * from doubtse "
    cur.execute(query1)
    data=cur.fetchall()
    return render_template('doubt.html',data=data)

@app.route('/doubts',methods=['post'])
def doubts1():
    email = session['email']
    question = request.form.get('doubt')
    connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234", port='3306')
    cur = connection.cursor()
    query = "insert into doubtse(email,question) values('{}','{}')".format(email, question)
    cur.execute(query)
    connection.commit()
    return redirect('/doubts')

@app.route('/UnEnroll')
def deleteUrl():
    if 'email' in session:
        courseid = request.args.get('courseid')
        email = session['email']
        print(email)
        print('courseid')
        connection = mysql.connector.connect(host="localhost", database="test1", user="root", password="project@1234",port='3306')
        cur = connection.cursor()
        query1 = "delete from courses where courseid={} and email='{}'".format(courseid,email)
        cur.execute(query1)
        connection.commit()
        return redirect('/courses')
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/1111')
def C():
    return render_template('c.html')

@app.route('/2222')
def java():
    return render_template('java.html')

@app.route('/3333')
def python():
    return render_template('python.html')

@app.route('/4444')
def dbms():
    return render_template('dbms.html')

@app.route('/5555')
def cpp():
    return render_template('cpp.html')


@app.route('/C-Introduction')
def c1():
    return render_template('c-introduction.html')

@app.route('/C-DecisionMaking')
def c2():
    return render_template('c-decision.html')

@app.route('/C-ProgramStructure')
def c3():
    return render_template('c-program.html')

@app.route('/C-Variable')
def c4():
    return render_template('c-variable.html')

@app.route('/C-Function')
def c5():
    return render_template('c-function.html')

@app.route('/C-Array')
def c6():
    return render_template('c-array.html')

@app.route('/C-String')
def c7():
    return render_template('c-string.html')


@app.route('/C-Quiz')
def c8():
    return render_template('CQuiz.html')

@app.route('/C-Quiz',methods=['post'])
def c9():
    score = 0
    ans = []
    for i in range(1,11):
        ans.append(request.form.get('Q'+str(i)))
    ansKey = ['B','A','A','B','C','A','A','A','B','A']
    for i in range(0,10):
        if(ans[i] == ansKey[i]):
            score= score+1
    print(score)
    return str(score*10)

@app.route('/C++-Introduction')
def cpp1():
    return render_template('cppIntro.html')

@app.route('/C++-Comment')
def cpp2():
    return render_template('cppComment.html')

@app.route('/C++-DataTypes')
def cpp3():
    return render_template('cppDataTypes.html')

@app.route('/C++-Variable')
def cpp4():
    return render_template('cppvariable.html')

@app.route('/C++-Math')
def cpp5():
    return render_template('cppMath.html')

@app.route('/C++-Input')
def cpp6():
    return render_template('cppInput.html')

@app.route('/C++-String')
def cpp7():
    return render_template('cppString.html')

@app.route('/C++-Switch')
def cpp8():
    return render_template('cppSwitch.html')

@app.route('/C++-Quiz')
def cpp9():
    return render_template('cppQuiz.html')

@app.route('/C++-Quiz',methods=['post'])
def cpp10():
    score = 0
    ans = []
    for i in range(1,11):
        ans.append(request.form.get('Q'+str(i)))
    ansKey = ['B','A','B','A','B','A','B','A','B','A']
    for i in range(0,10):
        if(ans[i] == ansKey[i]):
            score= score+1
    print(score)
    return str(score*10)

@app.route('/Python-Array')
def python1():
    return render_template('pyArray.html')

@app.route('/Python-Dictionary')
def python2():
    return render_template('pyDictionary.html')

@app.route('/Python-Function')
def python3():
    return render_template('pyFunction.html')

@app.route('/Python-Lambda')
def python4():
    return render_template('pyLambda.html')

@app.route('/Python-List')
def python5():
    return render_template('pyList.html')

@app.route('/Python-Set')
def python6():
    return render_template('pySet.html')

@app.route('/Python-String')
def python7():
    return render_template('pyString.html')

@app.route('/Python-Tuple')
def python8():
    return render_template('pyTuple.html')

@app.route('/Python-Quiz')
def python9():
    return render_template('pyQuiz.html')

# @app.route('/Python-Quiz',methods=['post'])
# def python10():
#     score = 0
#     ans = []
#     for i in range(1,11):
#         ans.append(request.form.get('Q'+str(i)))
#     ansKey = ['B','A','B','A','B','A','B','A','B','A',]
#     for i in range(0,10):
#         if(ans[i] == ansKey[i]):
#             score= score+1
#     print(score)
#     return str(score*10)

@app.route('/Java-Introduction')
def Java1():
    return render_template('c-introduction.html')

@app.route('/Java-DecisionMaking')
def Java2():
    return render_template('c-decision.html')

@app.route('/Java-ProgramStructure')
def Java3():
    return render_template('c-program.html')

@app.route('/Java-Variable')
def Java4():
    return render_template('c-variable.html')

@app.route('/Java-Function')
def Java5():
    return render_template('c-function.html')

@app.route('/Java-Array')
def Java6():
    return render_template('c-array.html')

@app.route('/Java-String')
def Java7():
    return render_template('c-string.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/back-to-video')
def back():
    return render_template('course_offerings.html')

if __name__ == '__main__':
    app.run()
