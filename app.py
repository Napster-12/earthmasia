from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length
import os

# -----------------------------
#   INTERNAL CONFIG CLASS
# -----------------------------
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    UPLOAD_FOLDER = 'static/uploads'


# -----------------------------
#   FLASK APP SETUP
# -----------------------------
app = Flask(__name__, static_folder='static', template_folder='templates')
app.config.from_object(Config)

# Ensure instance folder exists
os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

db = SQLAlchemy(app)


# -----------------------------
#   DATABASE MODEL
# -----------------------------
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)


# -----------------------------
#   CONTACT FORM
# -----------------------------
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField('Subject', validators=[Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])


# -----------------------------
#   CREATE TABLES AUTOMATICALLY
# -----------------------------
with app.app_context():
    db.create_all()


# -----------------------------
#   ROUTES
# -----------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
        )
        db.session.add(msg)
        db.session.commit()
        flash('Thanks — your message has been received. We will respond shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


# -----------------------------
#   RUN APP
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
