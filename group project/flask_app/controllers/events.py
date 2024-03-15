import os
from flask_app import app
from flask import render_template, redirect, flash, session, request
from flask_app.models.event import Event
from flask_app.models.user import User
from urllib.parse import unquote
from werkzeug.utils import secure_filename

from datetime import datetime
from urllib.parse import unquote
UPLOAD_FOLDER = 'flask_app/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import os
from werkzeug.exceptions import RequestEntityTooLarge

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from werkzeug.exceptions import HTTPException, NotFound
import urllib.parse



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/events')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id'],
    }
    userEvent=Event.get_event_by_creator()   
    return render_template('dashboard.html', loggedUser = User.get_user_by_id(data), userEvent=userEvent)

@app.route('/events/new')
def addEvent():
    if 'user_id' in session:
        return render_template('addEvent.html')
    
    return redirect('/')

@app.route('/event', methods=['POST'])
def createEvent():
    if 'user_id' not in session:
        return redirect('/')
    if not Event.validate_event(request.form):
        return redirect(request.referrer)
    image_file = request.files['image_upload']

    if image_file.filename == '':
        flash('No image selected', 'image_upload_error')
        return redirect(request.referrer)

    # Check if the file is an allowed image format (optional)
    if not allowed_file(image_file.filename):
        flash('Invalid image format. Please upload a valid image (png, jpg, jpeg)', 'image_upload_error')
        return redirect(request.referrer)

    # Generate a unique filename for the image
    filename = secure_filename(image_file.filename)
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = time + '_' + filename

    # Save the image to the uploads folder
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'location': request.form['location'],
        'date': request.form['date'],
        'event_time': request.form['event_time'],
        'price': request.form['price'],
        'image_path': filename,
        'user_id': session['user_id']
    }
    Event.create(data)

    return redirect('/')

@app.route('/comments/add/<int:id>', methods = ['POST'])
def createComment(id):
    if 'user_id' not in session:
        return redirect('/')
    if 'komenti' not in request.form:
        flash('Komenti eshte mandator', 'komenti')
    data = {
        'user_id':session['user_id'],
        'event_id': id,
        'komenti': request.form['komenti']
    }
    Event.addComment(data)
    return redirect(request.referrer)


@app.route('/event/delete/<int:id>')
def deleteEvent(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'id': id
    }
    user = User.get_user_by_user_id(data)
    event = Event.get_one_event_with_creator(data)
    if user['id'] == event['user_id']:
        Event.deletePostComments(data)
        Event.delete(data)
    return redirect(request.referrer)

@app.route('/buy/ticket')
def buyTicket():
    if 'user_id' not in session:
        return redirect('/')

    events = Event.get_all()
    return render_template('ticket.html', events = events)


@app.route('/buy/ticket', methods=['POST'])
def purchaseTicket():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'user_id': session['user_id'],
        'event_title': request.form['event_title'],
        'full_name': request.form['full_name'],
        'email': request.form['email'],
        'telephone_number': request.form['telephone_number'],
        'number_tickets': request.form['number_tickets']
    }
    Event.addTicket(data) 
    return redirect(request.referrer)


@app.route('/event/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id':session['user_id'],
        'event_id': id
    }
    user = User.get_user_by_user_id(data)
    event = Event.get_event_by_id(data)
    print(event)
    return render_template('event.html', event = event, loggedUser = user)


@app.route('/delete/comment/<int:id>')
def deleteComment(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id':session['user_id'],
        'id': id
    }
    user = User.get_user_by_user_id(data)
    komenti = Event.get_comment_by_id(data)
    if user['id'] == komenti['user_id']:
        Event.deleteComment(data)
    return redirect(request.referrer)