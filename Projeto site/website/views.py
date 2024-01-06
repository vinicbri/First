from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required , current_user
from .models import Note, db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if not note:
            flash('Anotação muito curta')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota criada')

    return render_template("home.html", user=current_user)

