from flask import Flask, render_template, request, flash, redirect, session
import mysql.connector
import os
from flask import flash

app = Flask(__name__)
###############-----------------sessions--------------------#################################

app = Flask(__name__)
app.secret_key = os.urandom(24)

###############------------------mysql---------------------##############################

conn = mysql.connector.connect(host="localhost", user="root", password="", database="login_validation")
cursor = conn.cursor()


###############-------------------HOME-------------------################################

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')


#############----------------REGISTER--------------------###################

@app.route('/register')
def register():
    return render_template('register.html')


###############-----------REGISTRATION--------------###############################

@app.route('/register_validation', methods=['POST'])
def register_validation():
    name = request.form.get('namereg')
    email = request.form.get('emailreg')
    password = request.form.get('passwordreg')

    if not len(password) >= 5:
        flash('Password must be at least 5 characters in length')
        return render_template('register.html')
    else:
        cursor.execute("INSERT INTO user (id,name,email,password) VALUES (NULL,%s,%s,%s)", (name, email, password))

        conn.commit()
        conn.close()

        return render_template('home.html')


##########----------------LOGIN-------------------##############################

@app.route('/')
def login():
    return render_template('login.html')


############----------------LOGIN_VALIDATION--------------------#######################

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s ", (email, password))
    users = cursor.fetchall()
    if len(users) > 0:
        session['user_id'] = users[0][0]
        flash('Logged in Successfully!')
        return redirect('/home')

    else:
        flash('Entered Details already exists or are  invalid ')
        return redirect('/')

###############------------------LOGOUT---------------#################################
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


###################------MAIN-----------############################

if __name__ == "__main__":
    app.run(debug=True)