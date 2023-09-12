from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

from io import StringIO
import PIL.Image
import base64

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/addpart', methods=['GET', 'POST'])
@login_required
def addpart():
    if request.method == 'POST': 
        #note = request.form.get('note')#Gets the note from the HTML 
        name = str(request.form.get('name'))
        model = str(request.form.get('model'))
        amount = request.form.get('amount')
        image = request.files["image"]

        base64_bytes = base64.b64encode(image.read())
        base64_string = base64_bytes.decode()

        if len(name) < 1:
            flash('Name is too short!', category='error') 
        if len(model) < 1:
            flash('model is too short!', category='error') 
        else:
            new_note = Note(data=base64_string, name=name, model=model, amount=amount, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Part added!', category='success')

    return render_template("addpart.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})