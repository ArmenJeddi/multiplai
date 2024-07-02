from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from models import db, DueDiligence, Contact
from forms import DueDiligenceForm, ContactForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    due_diligence_form = DueDiligenceForm()
    contact_form = ContactForm()
    
    if due_diligence_form.validate_on_submit() and due_diligence_form.submit_due_diligence.data:
        pdf_file = due_diligence_form.pdf.data
        filename = secure_filename(pdf_file.filename)
        pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        due_diligence = DueDiligence(
            fullname=due_diligence_form.fullname.data,
            email=due_diligence_form.email.data,
            pdf=filename,
            description=due_diligence_form.description.data,
            date_of_submission=datetime.utcnow()
        )
        db.session.add(due_diligence)
        db.session.commit()
        return redirect(url_for('index'))
    
    if contact_form.validate_on_submit() and contact_form.submit_contact.data:
        contact = Contact(
            fullname=contact_form.fullname.data,
            email=contact_form.email.data,
            question=contact_form.question.data,
            date_of_submission=datetime.utcnow()
        )
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', due_diligence_form=due_diligence_form, contact_form=contact_form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'multiplai' and form.password.data == 'kinghenrythe1st':
            session['logged_in'] = True
            return redirect(url_for('view_submissions'))
        else:
            return render_template('login.html', form=form, error='Invalid Credentials')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/view_submissions')
def view_submissions():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    due_diligence_submissions = DueDiligence.query.all()
    contact_submissions = Contact.query.all()
    return render_template('view_submissions.html', due_diligence_submissions=due_diligence_submissions, contact_submissions=contact_submissions)

if __name__ == '__main__':
    app.run(debug=True)
