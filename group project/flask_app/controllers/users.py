from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_bcrypt import Bcrypt
from flask_app.models.event import Event
from flask_app.models.user import User
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/events')
    return redirect('/logout')

@app.route('/register')
def registerPage():
    if 'user_id' in session:
        return redirect('/events')
    return render_template('register.html')


@app.route('/register', methods = ['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    if not User.validate_userRegister(request.form):
        return redirect(request.referrer)
    user = User.get_user_by_email(request.form)
    if user:
        flash('This account already exists', 'emailRegister')
        return redirect(request.referrer)
    data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    session['user_id'] = User.create(data)
    return redirect('/')


@app.route('/login')
def loginPage():
    if 'user_id' in session:
        return redirect('/events')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_user_by_email(request.form)
    if not user:
        flash('This email does not exist.', 'email')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'password')
        return redirect(request.referrer)
    session['user_id'] = user['id']
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/useraccount')
def profile():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': session['user_id']
    }
    
    logged_user = User.get_user_by_id(data)
    event = Event.geteventsByCreator(data)
    if isinstance(event, bool):
        event = []
    
    return render_template('userinfo.html', loggedUser=logged_user, event=event)

@app.route('/edit/user', methods = ['POST'])
def edit():
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_userUpdate(request.form):
        return redirect(request.referrer)
    
    data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        
        'id': session['user_id']
    }
    User.update(data)
    flash('User succesfully updated', 'updateSucces')
    return redirect(request.referrer)
